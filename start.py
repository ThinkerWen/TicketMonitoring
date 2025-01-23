import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Union

from Monitor_DM import DM
from Monitor_FWD import FWD
from Monitor_MY import MY
from Monitor_PXQ import PXQ
from email_notifier import EmailNotifier


def get_task(show: dict) -> Union[DM, MY, FWD, PXQ, None]:
    if show.get("platform") == 0:
        return DM(show)
    elif show.get("platform") == 1:
        return MY(show)
    elif show.get("platform") == 2:
        return FWD(show)
    elif show.get("platform") == 3:
        return PXQ(show)
    else:
        return None


class Runner:
    def __init__(self):
        self.email_notifier = EmailNotifier()
        self.threadPool = ThreadPoolExecutor(max_workers=100, thread_name_prefix="ticket_monitor_")

    def loop_monitor(self, monitor: Union[DM, MY, FWD, PXQ], show: dict) -> None:
        while datetime.strptime(show.get("deadline"), "%Y-%m-%d %H:%M:%S") > datetime.now():
            try:
                if monitor.monitor():
                    info = f"{monitor.show_info.get('platform')} {show.get('show_name')} 已回流，请及时购票！"
                    # Get show identifier
                    show_id = f"{monitor.show_info.get('platform')}_{show.get('show_name')}"
                    
                    # Send email notification if enough time has passed
                    if self.email_notifier.should_send(show_id):
                        logging.info(f"->发送邮件提醒:{show.get('show_name')}")
                        subject = f"Ticket Alert: {show.get('show_name')}"
                        self.email_notifier.send_notification(show_id, subject, info)

                    logging.info(info)
                    monitor.bark_alert(info)
            except Exception as e:
                logging.info(f"发生错误：{e}")
            finally:
                time.sleep(1)

    def start(self):
        file = open("config.json", "r", encoding="utf-8")
        show_list = json.load(file).get("monitor_list")
        file.close()

        for show in show_list:
            task = get_task(show)
            if task:
                self.threadPool.submit(self.loop_monitor, task, show)
            else:
                logging.error(f"监控对象 {show.get('show_name')} 加载失败 show_id: {show.get('show_id')}")
        self.threadPool.shutdown(wait=True)


if __name__ == '__main__':
    runner = Runner()
    runner.start()
