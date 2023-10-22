import json
import logging
import time

import requests
import urllib3


class Monitor:
    _last_time = 0
    _proxy_data = dict()

    proxy = dict()
    last_alert_time = 0

    def __init__(self):
        self.proxy = self.proxy_data
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(filename)s:%(lineno)d] : %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

    @property
    def proxy_data(self):
        return self._fetch_proxy()

    @classmethod
    def _fetch_proxy(cls) -> dict:
        current_time = time.time()
        if current_time - cls._last_time > 10 or not cls._proxy_data:
            # 可以修改为动态获取代理
            cls._proxy_data = {
                "http": f"http://127.0.0.1:12301",
                "https": f"http://@127.0.0.1:12301"
            }
            cls._last_time = current_time
        return cls._proxy_data

    @staticmethod
    def send_replenish_alert(show_name):
        content = {
            "appToken": "去WxPusher公众号申请APPToken",
            "content": '''<h2>%s补票</h2>
            <img src="https://www.hive-net.cn/Assets/Images/MonitorExample.jpg" width="200" alt="演示图片">
            <h3 style="color: red;"><a href="https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzAxMzI1OTgwNQ==#wechat_redirect">扫码关注公众号获取更多抢票技巧</a></h3>
            <img src="https://www.hive-net.cn/Assets/Images/wxmpQRCode.jpg" width="200" alt="公众号">
            ''' % show_name,
            "summary": f"{show_name}补票",
            "contentType": 2,
            "topicIds": [22581],
            "url": "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzAxMzI1OTgwNQ==#wechat_redirect",
            "verifyPay": False
        }
        response = requests.post(url="https://wxpusher.zjiecode.com/api/send/message", json=content, verify=False)
        if json.loads(response.text).get("code") == 1000:
            logging.info(f"{show_name} 已补票, 推送消息成功")
        else:
            logging.info(f"{show_name} 已补票, 推送消息失败")

    @staticmethod
    def send_order_alert(show_name, ticket):
        pass
