import json
import logging

import requests
from requests import Response

from Monitor import Monitor


class MY(Monitor):

    def __init__(self, perform: dict) -> None:
        super().__init__()
        logging.info(f"猫眼 {perform.get('show_name')} 开始加载")
        self.performId = perform.get('show_id')
        self.show_info = dict()
        self.get_show_infos()
        logging.info(f"猫眼 {self.show_info.get('show_name')} 加载成功")

    def get_show_infos(self):
        response = self.request(f'https://wx.maoyan.com/maoyansh/myshow/ajax/v2/performance/{self.performId}', self.performId)
        self.show_info["show_id"] = json.loads(response.text).get("data").get("performanceId")
        self.show_info["show_name"] = json.loads(response.text).get("data").get("name")
        self.show_info["seat_info"] = list()
        self.show_info["platform"] = 1
        response = self.request(f'https://wx.maoyan.com/maoyansh/myshow/ajax/v2/performance/{self.performId}/shows/0', self.performId)
        show_info = json.loads(response.text)
        for session in show_info.get("data"):
            session_id = session.get("showId")
            session_name = session.get("name")
            response = self.request(f'https://wx.maoyan.com/maoyansh/myshow/ajax/v2/show/{session_id}/tickets?sellChannel=7&performanceId={self.performId}&cityId=1', self.performId)
            show_session_info = json.loads(response.text)
            for seat in show_session_info.get("data"):
                seat_info = dict()
                seat_info["session_id"] = session_id
                seat_info["session_name"] = session_name
                seat_info["seat_plan_id"] = seat.get("ticketClassId")
                seat_info["seat_plan_name"] = str(int(seat.get("ticketPrice")))
                self.show_info["seat_info"].append(seat_info)

    def monitor(self) -> list:
        logging.info(f"猫眼 {self.show_info.get('show_name')} 监控中")
        can_buy_list = list()
        response = self.request(f'https://wx.maoyan.com/maoyansh/myshow/ajax/v2/performance/{self.performId}/shows/0', self.performId)
        show_info = json.loads(response.text)
        if show_info.get("code") != 200:
            return can_buy_list
        for show in show_info.get("data"):
            show_id = show.get("showId")
            if show.get("soldOut"):
                continue
            response = self.request(f'https://wx.maoyan.com/maoyansh/myshow/ajax/v2/show/{show_id}/tickets?sellChannel=7&performanceId={self.performId}&cityId=1', self.performId)
            show_session_info = json.loads(response.text)
            if show_session_info.get("code") == 200:
                for session in show_session_info.get("data"):
                    seat = session.get("salesPlanVO")
                    salesPlanId = seat.get("salesPlanId")
                    if not seat.get("currentAmount"):
                        continue
                    can_buy_list.append(salesPlanId)
        return can_buy_list

    def request(self, url: str, perform_id: str) -> Response:
        return requests.get(
            url=url,
            headers={
                'xweb_xhr': '1',
                'Accept': '*/*',
                'Host': 'wx.maoyan.com',
                'X-Channel-ID': '70001',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'version': 'wallet-v4.5.11',
                'X-Requested-With': 'wxapp',
                'Accept-Language': 'zh-CN,zh',
                'Sec-Fetch-Site': 'cross-site',
                'x-wxa-referer': 'pages/search/index',
                'Content-Type': 'multipart/form-data',
                'x-wxa-page': 'pages/show/detail/index',
                'Referer': 'https://servicewechat.com/wxdbb4c5f1b8ee7da1/1366/page-frame.html',
                'x-wxa-query': f'%7B%22id%22%3A%22{perform_id}%22%2C%22utm_source%22%3A%22wxwallet_search%22%7D',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF XWEB/30817',
            },
            proxies=super()._proxy,
            verify=False,
            timeout=10
        )
