import json
import logging
import urllib.parse
from hashlib import md5
from time import time

import requests
from requests import Response

from Monitor import Monitor


class DM(Monitor):

    def __init__(self, perform: dict) -> None:
        super().__init__()
        self.show_url = DM.get_show_url()
        self.seat_url = DM.get_seat_url()
        self.request = self.do_request()
        self.show_info = {
            "platform": 0,
            "seat_info": list(),
            "session_info": list(),
            "show_id": perform.get('show_id'),
            "show_name": perform.get('show_name')
        }
        logging.info(f"大麦 {perform.get('show_name')} 开始加载")
        self.get_show_infos()
        logging.info(f"大麦 {self.show_info.get('show_name')} 加载成功")

    def get_show_infos(self):
        show_id = self.show_info.get('show_id')
        response = self.request(self.show_url(show_id))
        data = self.get_data_from_response(response)
        show_info = data.get("detailViewComponentMap").get("item")
        for session in show_info.get("item").get("performBases"):
            session_id = session.get("performs")[0].get("performId")
            session_name = session.get("performs")[0].get("performName")
            self.show_info["session_info"].append({
                "session_id": session_id,
                "session_name": session_name,
            })
            response = self.request(self.seat_url(show_id, session_id))
            show_session_info = self.get_data_from_response(response, session_id)
            for seat in show_session_info.get("perform").get("skuList"):
                self.show_info["seat_info"].append({
                    "session_id": session_id,
                    "session_name": session_name,
                    "seat_plan_id": seat.get("skuId"),
                    "seat_plan_name": seat.get("priceName"),
                })

    def monitor(self) -> list:
        logging.info(f"大麦 {self.show_info.get('show_name')} 监控中")
        can_buy_list = list()
        show_id = self.show_info.get('show_id')
        for session in self.show_info["session_info"]:
            session_id = session.get("session_id")
            response = self.request(self.seat_url(show_id, session_id))
            show_session_info = self.get_data_from_response(response, session_id)
            for seat in show_session_info.get("perform").get("skuList"):
                if seat.get("skuSalable") == "false":
                    continue
                can_buy_list.append(seat.get("skuId"))
        return can_buy_list

    def get_data_from_response(self, response, ext="show"):
        show_id = self.show_info.get('show_id')
        if "SUCCESS::调用成功" not in response.json().get("ret"):
            if ext == "show":
                response = self.request(self.show_url(show_id, c=response.json().get("c")))
            else:
                cookies = requests.utils.dict_from_cookiejar(response.cookies)
                response = self.request(self.seat_url(show_id, ext, c=cookies.get("_m_h5_tk")), cookies=cookies)
        return json.loads(response.json().get("data",{}).get("legacy",{})) if ext == "show" else json.loads(response.json().get("data").get("result"))

    @staticmethod
    def get_show_url():
        inner_c = '5441487fd096478b73f9b299562eb789_1731931246634;150179d8faf5815c2f70b06bd9a82bc4'
        def inner_show_url(show_id: str, c=""):
            nonlocal inner_c
            inner_c = inner_c if not c else c
            url = 'https://mtop.damai.cn/h5/mtop.damai.item.detail.getdetail/1.0/2.0/'
            params = {
                'jsv': '2.4.12',
                'appKey': '12574478',
                't': f'{time() * 1000}',
                'sign': '4da8114e4cd5600f75a968a51bce928',
                'c': inner_c,
                'v': '1.0',
                'dataType': 'json',
                'type': 'json',
                'AntiCreep': 'true',
                'AntiFlood': 'true',
                'api': 'mtop.damai.item.detail.getdetail',
                'url': 'mtop.damai.item.detail.getdetail',
                'env': 'm',
                'valueType': 'string',
                'data': '{"dmChannel":"damai@weixin_weapp","itemId":"'+show_id+'","lat":39.93722786511198,"lng":116.43680040115234}',
                '_bx-m': '0.0.11',
            }
            params["sign"] = DM.get_sign(params["c"], params["t"], params["data"])
            return f"{url}?{urllib.parse.urlencode(params)}"
        return inner_show_url

    @staticmethod
    def get_seat_url():
        inner_c = 'e1ff1f67d9bd7570c338aabd651c011d_1731992988831'
        def inner_seat_url(show_id: str, session_id: str, c=""):
            nonlocal inner_c
            inner_c = inner_c if not c else c
            url = 'https://mtop.damai.cn/h5/mtop.alibaba.detail.subpage.getdetail/2.0/'
            params = {
                'jsv': '2.7.4',
                'appKey': '12574478',
                't': f'{time() * 1000}',
                'sign': 'cfcc345ab6871c74f3b1d45ff536d261',
                'api': 'mtop.alibaba.detail.subpage.getdetail',
                'v': '2.0',
                'H5Request': 'true',
                'type': 'originaljson',
                'timeout': '10000',
                'dataType': 'json',
                'valueType': 'original',
                'forceAntiCreep': 'true',
                'AntiCreep': 'true',
                'useH5': 'true',
                'data': '{"itemId":"' + show_id + '","bizCode":"ali.china.damai","scenario":"itemsku","exParams":"{\\"dataType\\":2,\\"dataId\\":\\"' + session_id + '\\"}","platform":"8","comboChannel":"2","dmChannel":"damai@damaih5_h5"}',
            }
            params["sign"] = DM.get_sign(inner_c, params["t"], params["data"])
            return f"{url}?{urllib.parse.urlencode(params)}"
        return inner_seat_url

    @staticmethod
    def get_sign(c: str, t: str, data: str):
        plain = f"{c.split('_')[0]}&{t}&12574478&{data}"
        return md5(plain.encode(encoding='utf-8')).hexdigest()

    def do_request(self):
        inner_cookies = dict()
        def inner_request(url: str, cookies=None) -> Response:
            nonlocal inner_cookies
            inner_cookies = inner_cookies if not cookies else cookies
            return requests.get(
                url=url,
                headers={
                    'x-tap': 'wx',
                    'Host': 'mtop.damai.cn',
                    'Accept': 'application/json',
                    'content-type': 'application/x-www-form-urlencoded',
                    'Referer': 'https://servicewechat.com/wx938b41d0d7e8def0/350/page-frame.html',
                    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.53(0x18003531) NetType/WIFI Language/zh_CN',
                },
                cookies={
                    'csg': '354a0bd6',
                    '_hvn_login': '18',
                    'munb': '2218951629204',
                    'usercode': '532127652',
                    '_samesite_flag_': 'true',
                    'havanaId': '2218951629204',
                    '_tb_token_': 'ee5b537387ee1',
                    't': '0bdf4d2eef5a59975c4922c8c7f6e4e9',
                    'dm_nickname': '%E9%BA%A6%E5%AD%90acCkX',
                    'cookie2': '1318094fd8689145b9831b581c396fd7',
                    'isg': 'BHNzJUGRECbwetx5Cy3BQP_hCHOdqAdqdBfSKyUQwxLpJJLGrXi_uPTm2NLKn19i',
                    'sgcookie': 'E1003SPW8GLYK1h1JSPuDtsWj%2BRUfcdScMMELTEgntdA8gUL8jBP6A%2FNdboy6gkOaXqPqMfWZ4pDm8%2F8y67DAT2YyXEGgIPKriLaP3KRUtQrBvY%3D',
                    'tfstk': 'fxqZg89Eor4eA6jl1Ao2Ylpt4Gftmcf53oGjn-2mCfcgC-Dq0WN4CqfThWl06Wd6fc210rPSOStbCS9TJ7wkfl_tcnosDmf5NgsSBRnxmV-vqolTKJHmnF6dDRetDpILjVB3BIkL0VzmmSm3KYHmmC00iHxn9xHDsxxGL9kxthcmmnmHKYkriCVmm9yn9xA9m40XqAgGeAe0o1fVOVhuIfvHKyDyNbyign-VhAuw8Rcemnq3RXMsbfCwQbz7eoPattxmgy4QEXPhnnc4-rqsWmIyEnHnMfEY7IYmSnMEN9WEVMjVfZ9P3ELvkVFtLb6nUELxSvHEN9WekE3T6vl5KY5..',
                    '_m_h5_tk': inner_cookies.get("_m_h5_tk"),
                    '_m_h5_tk_enc': inner_cookies.get("_m_h5_tk_enc"),
                },
                proxies=self._proxy,
                verify=False,
                timeout=10
            )
        return inner_request
