import json
import logging

import requests

from Headers import get_MY_headers
from Monitor import Monitor


class MY(Monitor):

    def __init__(self, performId: int) -> None:
        super().__init__()
        logging.info(f"猫眼 {performId} 开始加载")
        self.performId = performId
        self.show_info = dict()
        self.get_show_infos()
        logging.info(f"猫眼 {self.show_info.get('show_name')} 加载成功")

    def get_show_infos(self):
        headers = get_MY_headers(self.performId)
        response = requests.get(f'https://wx.maoyan.com/maoyansh/myshow/ajax/v2/performance/{self.performId}', headers=headers, verify=False, timeout=10)
        self.show_info["show_id"] = json.loads(response.text).get("data").get("performanceId")
        self.show_info["show_name"] = json.loads(response.text).get("data").get("name")
        self.show_info["seat_info"] = list()
        self.show_info["platform"] = 1
        response = requests.get(f'https://wx.maoyan.com/maoyansh/myshow/ajax/v2/performance/{self.performId}/shows/0', headers=headers, verify=False, timeout=10)
        show_info = json.loads(response.text)
        for session in show_info.get("data"):
            session_id = session.get("showId")
            session_name = session.get("name")
            response = requests.get(f'https://wx.maoyan.com/maoyansh/myshow/ajax/v2/show/{session_id}/tickets?sellChannel=7&performanceId={self.performId}&cityId=1', headers=headers, verify=False, timeout=10)
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
        headers = get_MY_headers(self.performId)
        response = requests.get(f'https://wx.maoyan.com/maoyansh/myshow/ajax/v2/performance/{self.performId}/shows/0', headers=headers, verify=False, proxies=self.proxy, timeout=10)
        show_info = json.loads(response.text)
        if show_info.get("code") != 200:
            return can_buy_list
        for show in show_info.get("data"):
            show_id = show.get("showId")
            if show.get("soldOut"):
                continue
            response = requests.get(f'https://wx.maoyan.com/maoyansh/myshow/ajax/v2/show/{show_id}/tickets?sellChannel=7&performanceId={self.performId}&cityId=1', headers=headers, verify=False, proxies=self.proxy, timeout=10)
            show_session_info = json.loads(response.text)
            if show_session_info.get("code") == 200:
                for session in show_session_info.get("data"):
                    seat = session.get("salesPlanVO")
                    salesPlanId = seat.get("salesPlanId")
                    if not seat.get("currentAmount"):
                        continue
                    can_buy_list.append(salesPlanId)
        return can_buy_list
