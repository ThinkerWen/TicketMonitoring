import json
import logging

import requests
from requests import Response

from Monitor import Monitor


class FWD(Monitor):

    show_start = False

    def __init__(self, perform: dict) -> None:
        super().__init__()
        self.show_info = {
            "platform": "纷玩岛",
            "seat_info": list(),
            "session_info": list(),
            "show_id": perform.get('show_id'),
            "show_name": perform.get('show_name')
        }
        logging.info(f"纷玩岛 {perform.get('show_name')} 开始加载")
        self.get_show_infos()
        logging.info(f"纷玩岛 {self.show_info.get('show_name')} 加载成功")

    def get_show_infos(self):
        show_id = self.show_info.get('show_id')
        response = self.request(f'https://api.livelab.com.cn/performance/app/project/get_performs?project_id={show_id}&v=1694683437294&retry=false')
        show_info = json.loads(response.text)
        for session_info in show_info.get("data").get("performInfos"):
            session = session_info.get("performInfo")[0]
            session_id = session.get("id")
            session_name = session.get("name")
            for seat in session.get("seatPlans"):
                self.show_info["seat_info"].append({
                    "session_id": session_id,
                    "session_name": session_name,
                    "seat_plan_id": seat.get("seatPlanId"),
                    "seat_plan_name": seat.get("seatPlanName"),
                })

    def monitor(self) -> list:
        logging.info(f"纷玩岛 {self.show_info.get('show_name')} 监控中")
        can_buy_list = []
        show_id = self.show_info.get('show_id')
        if not self.show_start:
            response = self.request(f'https://api.livelab.com.cn/performance/app/project/countDown?projectId={show_id}')
            if response.json().get("data", 0) > 0:
                return can_buy_list
            self.show_start = True
        response = self.request(f'https://api.livelab.com.cn/performance/app/project/get_performs?project_id={show_id}&v=1694683437294&retry=false')
        show_info = response.json()
        if show_info.get("code") != 10000:
            return can_buy_list
        for session_info in show_info.get("data", {}).get("performInfos", []):
            seat_plans = session_info.get("performInfo", [])[0].get("seatPlans", [])
            can_buy_list.extend(
                str(seat.get("seatPlanId")) for seat in seat_plans if seat.get("display") == 1
            )
        return can_buy_list

    def request(self, url: str) -> Response:
        return requests.get(
            url=url,
            headers={
                'xweb_xhr': '1',
                'Accept': '*/*',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Host': 'api.livelab.com.cn',
                'Accept-Language': 'zh-CN,zh',
                'Sec-Fetch-Site': 'cross-site',
                'Content-Type': 'application/json',
                'Referer': 'https://servicewechat.com/wx5a8f481d967649eb/70/page-frame.html',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF XWEB/30817',
                'authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJjdCI6MTcxMzI1MTY0Nzg1NCwibWlkIjoxNzU4ODA4NTcxMzc3NDI2MzMzLCJ0eXBlIjoiYXBwIiwiZGlkIjoiZDVhNGUwMDg0ODc0NTY4OCJ9.Q1ltCrRG48TfjAWaAnfuLHo0oX2NQKsSMNalffwncztBjYVb38LnbLYOCgXhf7hK5vGOHy_xf11qBe5Xk9hqhA',
            },
            proxies=super()._proxy,
            verify=False,
            timeout=10
        )
