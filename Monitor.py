import json
import logging
from time import time

import requests
import urllib3


class Monitor:
    __last_alert_time = 0
    _proxy = None
    # proxy在config.json中配置格式为: {
    #     "http": "http://10.16.10.24:12001",
    #     "https": "http://10.16.10.24:12001"
    #   }
    # 频繁请求请添加代理，自建代理见GitHub: https://github.com/ThinkerWen/ProxyServer

    def __init__(self):
        file = open("config.json", "r", encoding="utf-8")
        proxy = json.load(file).get("proxy")
        self._proxy = proxy if proxy else None
        file.close()
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(filename)s:%(lineno)d] : %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

    # IOS用户建议使用Bark提醒，见GitHub: https://github.com/Finb/Bark
    def bark_alert(self, content: str):
        if time() - self.__last_alert_time < 10:
            return
        self.__last_alert_time = time()
        for key in ["BARK_PUSH_KEY"]:   # 此处列表填充Bark的key，如果没有Bark则注释这两行代码，添加您自定义的提醒方式
            requests.get(f"https://api.day.app/{key}/{content}")
