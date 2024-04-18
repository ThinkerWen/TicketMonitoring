import logging
from time import time

import requests
import urllib3


class Monitor:
    __last_alert_time = 0
    # 频繁请求请添加代理，自建代理见GitHub: https://github.com/ThinkerWen/ProxyServer
    _proxy = {"http": f"http://127.0.0.1:12301", "https": f"http://127.0.0.1:12301"}

    def __init__(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(filename)s:%(lineno)d] : %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

    # IOS用户建议使用Bark提醒，见GitHub: https://github.com/Finb/Bark
    def bark_alert(self, content: str):
        if time() - self.__last_alert_time < 10:
            return
        self.__last_alert_time = time()
        for key in ["BARK_PUSH_KEY"]:
            requests.get(f"https://api.day.app/{key}/{content}")
