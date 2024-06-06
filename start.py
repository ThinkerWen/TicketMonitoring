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

    threadPool = ThreadPoolExecutor(max_workers=100, thread_name_prefix="ticket_monitor_")

    @staticmethod
    def loop_monitor(monitor: Union[DM, MY, FWD, PXQ], show: dict) -> None:
        while datetime.strptime(show.get("deadline"), "%Y-%m-%d %H:%M:%S") > datetime.now():
            try:
                if monitor.monitor():
                    info = f"平台{show.get('platform')} {show.get('show_name')} 已回流，请及时购票！"
                    logging.info(info)
                    monitor.bark_alert(info)
            except Exception as e:
                logging.info(f"发生错误：{e}")
            finally:
                time.sleep(1)

    def start(self):
        file = open("config.json", "r", encoding="utf-8")
        show_list = json.loads(file.read())
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
