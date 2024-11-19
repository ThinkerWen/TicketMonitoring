import json
import logging

import requests
from requests import Response

from Monitor import Monitor


class PXQ(Monitor):

    show_start = False

    def __init__(self, perform: dict) -> None:
        super().__init__()
        self.show_info = {
            "platform": "票星球",
            "seat_info": list(),
            "session_info": list(),
            "show_id": perform.get('show_id'),
            "show_name": perform.get('show_name')
        }
        logging.info(f"票星球 {perform.get('show_name')} 开始加载")
        self.get_show_infos()
        logging.info(f"票星球 {self.show_info.get('show_name')} 加载成功")

    def get_show_infos(self):
        show_id = self.show_info.get('show_id')
        response = self.request(f"https://m.piaoxingqiu.com/cyy_gatewayapi/show/pub/v3/show/{show_id}/sessions_static_data")
        show_info = json.loads(response.text)
        for session in show_info.get("data").get("sessionVOs"):
            session_id = session.get("bizShowSessionId")
            session_name = session.get("sessionName")
            self.show_info["session_info"].append({
                "session_id": session_id,
                "session_name": session_name,
            })
            response = self.request(f'https://m.piaoxingqiu.com/cyy_gatewayapi/show/pub/v3/show/{show_id}/show_session/{session_id}/seat_plans_static_data')
            for seat in response.json().get("data").get("seatPlans"):
                self.show_info["seat_info"].append({
                    "session_id": session_id,
                    "session_name": session_name,
                    "seat_plan_id": seat.get("seatPlanId"),
                    "seat_plan_name": seat.get("seatPlanName"),
                })

    def monitor(self) -> list:
        logging.info(f"票星球 {self.show_info.get('show_name')} 监控中")
        can_buy_list = []
        show_id = self.show_info.get('show_id')

        if not self.show_start:
            response = self.request( f'https://m.piaoxingqiu.com/cyy_gatewayapi/show/pub/v3/show/{show_id}/sessions_dynamic_data')
            show_info = response.json()
            if show_info.get("statusCode") == 200:
                for session in show_info.get("data", {}).get("sessionVOs", []):
                    if session.get("sessionSaleTimeCountdown", 0) > 0:
                        return can_buy_list
                self.show_start = True
        for session in self.show_info.get("session_info"):
            session_id = session.get("session_id")
            response = self.request(f'https://m.piaoxingqiu.com/cyy_gatewayapi/show/pub/v3/show/{show_id}/show_session/{session_id}/seat_plans_dynamic_data')
            if response.json().get("statusCode") == 200:
                can_buy_list.extend(
                    seat.get("seatPlanId") for seat in response.json().get("data", {}).get("seatPlans", [])
                    if seat.get("canBuyCount", 0) > 0
                )
        return can_buy_list

    def request(self, url: str) -> Response:
        return requests.get(
            url=url,
            headers={
                'ver': '3.1.5',
                'xweb_xhr': '1',
                'Accept': '*/*',
                'src': 'weixin_mini',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Host': 'm.piaoxingqiu.com',
                'terminal-src': 'WEIXIN_MINI',
                'Accept-Language': 'zh-CN,zh',
                'Sec-Fetch-Site': 'cross-site',
                'Content-Type': 'application/json',
                "merchant-id": "6267a80eed218542786f1494",
                'Referer': 'https://servicewechat.com/wxad60dd8123a62329/238/page-frame.html',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF XWEB/30817',
            },
            proxies=super()._proxy,
            verify=False,
            timeout=10
        )
