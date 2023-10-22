import json
import logging

import requests

from Headers import get_FWD_headers
from Monitor import Monitor


class FWD(Monitor):

    def __init__(self, performId: int) -> None:
        super().__init__()
        logging.info(f"纷玩岛 {performId} 开始加载")
        self.performId = performId
        self.show_info = dict()
        self.get_show_infos()
        logging.info(f"纷玩岛 {self.show_info.get('show_name')} 加载成功")

    def get_show_infos(self):
        headers = get_FWD_headers()
        response = requests.get(f'https://api.livelab.com.cn/performance/app/project/get_project_info?project_id={self.performId}&v=1695113662390&retry=false', headers=headers, verify=False, timeout=10)
        self.show_info["show_id"] = json.loads(response.text).get("data").get("projectId")
        self.show_info["show_name"] = json.loads(response.text).get("data").get("projectName")
        self.show_info["seat_info"] = list()
        self.show_info["platform"] = 2
        response = requests.get(f'https://api.livelab.com.cn/performance/app/project/get_performs?project_id={self.performId}&v=1694683437294&retry=false', headers=headers, verify=False, timeout=10)
        show_info = json.loads(response.text)
        for session_info in show_info.get("data").get("performInfos"):
            session = session_info.get("performInfo")[0]
            session_id = session.get("id")
            session_name = session.get("name")
            for seat in session.get("seatPlans"):
                seat_info = dict()
                seat_info["session_id"] = session_id
                seat_info["session_name"] = session_name
                seat_info["seat_plan_id"] = seat.get("seatPlanId")
                seat_info["seat_plan_name"] = seat.get("seatPlanName")
                self.show_info["seat_info"].append(seat_info)

    def monitor(self) -> list:
        logging.info(f"纷玩岛 {self.show_info.get('show_name')} 监控中")
        can_buy_list = list()
        headers = get_FWD_headers()
        response = requests.get(f'https://api.livelab.com.cn/performance/app/project/get_performs?project_id={self.performId}&v=1694683437294&retry=false', headers=headers, verify=False, proxies=self.proxy, timeout=10)
        show_info = json.loads(response.text)
        if show_info.get("code") != 10000:
            return can_buy_list
        for session_info in show_info.get("data").get("performInfos"):
            for seat in session_info.get("performInfo")[0].get("seatPlans"):
                if seat.get("display") != 1:
                    continue
                can_buy_list.append(seat.get("seatPlanId"))
        return can_buy_list
