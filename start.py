import logging
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import pymysql

from Monitor_DM import DM
from Monitor_FWD import FWD
from Monitor_MY import MY


class Runner:

    thread_local = threading.local()
    threadPool = ThreadPoolExecutor(max_workers=100, thread_name_prefix="ticket_monitor_")

    @staticmethod
    def create_cursor():
        connect = pymysql.Connect(
            host="localhost",
            port=3306,
            user="root",
            passwd="123456",
            db="db_name",
            charset='utf8'
        )
        return connect.cursor()

    def get_cursor(self):
        if not hasattr(self.thread_local, 'cursor'):
            self.thread_local.cursor = self.create_cursor()
        return self.thread_local.cursor

    def loop_monitor(self, monitor_obj) -> None:
        cursor = self.get_cursor()
        cursor.execute(f"select monitor_end_time from ticket_order_monitor_show where monitor_end_time > CURRENT_TIMESTAMP and show_id = '{monitor_obj.performId}'")
        end_time = cursor.fetchone()[0]
        while end_time > datetime.now():
            try:
                monitor_obj.proxy = monitor_obj.proxy_data
                can_buy_list = monitor_obj.monitor()
                if can_buy_list and monitor_obj.last_alert_time + 30 <= time.time():
                    monitor_obj.last_alert_time = time.time()
                    monitor_obj.send_replenish_alert(monitor_obj.show_info.get("show_name"))
            except Exception as e:
                logging.info(f"发生错误：{e}")
                time.sleep(5)
            finally:
                time.sleep(1)

    def start(self):
        task_list = list()
        cursor = self.create_cursor()
        cursor.execute(f"select show_id, platform from ticket_order_monitor_show where monitor_end_time > CURRENT_TIMESTAMP")
        for show in cursor.fetchall():
            monitor = None
            performId, platformId = show
            if platformId == 0:
                monitor = DM(performId)
            elif platformId == 1:
                monitor = MY(int(performId))
            elif platformId == 2:
                monitor = FWD(int(performId))
            if monitor:
                task_list.append(monitor)
            else:
                return
        for task in task_list:
            self.threadPool.submit(self.loop_monitor, task)
        self.threadPool.shutdown(wait=True)


if __name__ == '__main__':
    runner = Runner()
    runner.start()
