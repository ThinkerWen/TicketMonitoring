import json
import logging

import requests
from requests import Response

from Monitor import Monitor


class MY(Monitor):

    token = str()

    def __init__(self, perform: dict) -> None:
        super().__init__()
        file = open("config.json", "r", encoding="utf-8")
        self.token = json.load(file).get("token").get("my")
        file.close()
        self.performId = perform.get('show_id')
        self.show_info = {
            "platform": "猫眼",
            "seat_info": list(),
            "session_info": list(),
            "show_id": perform.get('show_id'),
            "show_name": perform.get('show_name')
        }
        logging.info(f"猫眼 {perform.get('show_name')} 开始加载")
        self.get_show_infos()
        logging.info(f"猫眼 {self.show_info.get('show_name')} 加载成功")

    def get_show_infos(self):
        show_id = self.show_info.get('show_id')
        response = requests.post(f"https://wx.maoyan.com/my/odea/project/shows?token={self.token}&clientPlatform=2", json={"projectId":show_id}, headers=MY.headers(), proxies=self._proxy)
        show_info = response.json().get("data")
        for session in show_info.get("showListVO"):
            session_id = session.get("showId")
            session_name = session.get("showName")
            self.show_info["session_info"].append({
                "session_id": session_id,
                "session_name": session_name,
            })
            response = self.request(f"https://wx.maoyan.com/my/odea/show/tickets?token={self.token}&showId={session_id}&projectId={show_id}&clientPlatform=2")
            show_session_info = response.json().get("data")
            for seat in show_session_info.get("ticketsVO"):
                self.show_info["seat_info"].append({
                    "session_id": session_id,
                    "session_name": session_name,
                    "seat_plan_id": seat.get("ticketId"),
                    "seat_plan_name": str(int(seat.get("ticketPriceVO").get("ticketPrice"))),
                })

    def monitor(self) -> list:
        logging.info(f"猫眼 {self.show_info.get('show_name')} 监控中")
        can_buy_list = []
        show_id = self.show_info.get('show_id')
        for session in self.show_info.get("session_info", []):
            session_id = session.get("session_id")
            response = self.request(f"https://wx.maoyan.com/my/odea/show/tickets?token={self.token}&showId={session_id}&projectId={show_id}&clientPlatform=2")
            tickets = response.json().get("data", {}).get("ticketsVO", [])
            can_buy_list.extend(ticket.get("ticketId") for ticket in tickets if ticket.get("remainingStock"))
        return can_buy_list

    def request(self, url: str) -> Response:
        return requests.get(
            url=url,
            headers=MY.headers(),
            proxies=super()._proxy,
            verify=False,
            timeout=10
        )

    @staticmethod
    def headers():
        return {
            'Host': 'wx.maoyan.com',
            'X-Channel-ID': '70001',
            'version': 'wallet-v5.10.9',
            'X-Requested-With': 'wxapp',
            'content-type': 'application/json',
            'x-wxa-referer': 'pages/show/detail/v2/index',
            'x-wxa-page': 'pages/showsubs/ticket-level/v2/index',
            'Referer': 'https://servicewechat.com/wxdbb4c5f1b8ee7da1/1557/page-frame.html',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.53(0x18003531) NetType/WIFI Language/zh_CN',
        }
