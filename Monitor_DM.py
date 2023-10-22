import json
import logging
import time
from hashlib import md5

import requests

from Headers import get_DM_headers
from Monitor import Monitor


class DM(Monitor):

    def __init__(self, performId: str) -> None:
        super().__init__()
        logging.info(f"大麦 {performId} 开始加载")
        self.cookies = self.get_cookies(True)
        self.performId = performId
        self.show_info = dict()
        self.get_show_infos()
        logging.info(f"大麦 {self.show_info.get('show_name')} 加载成功")

    def get_show_infos(self):
        headers = get_DM_headers()
        t, sign = self.get_show_params()
        response = requests.get('https://mtop.damai.cn/h5/mtop.alibaba.damai.detail.getdetail/1.2/?jsv=2.7.2&appKey=12574478&t=%d&sign=%s&api=mtop.alibaba.damai.detail.getdetail&v=1.2&H5Request=true&type=originaljson&timeout=10000&dataType=json&valueType=original&forceAntiCreep=true&AntiCreep=true&useH5=true&data={"itemId":%s,"platform":"8","comboChannel":"2","dmChannel":"damai@damaih5_h5"}' % (t, sign, self.performId), cookies=self.cookies, headers=headers, verify=False, proxies=self.proxy, timeout=10)
        data = json.loads(response.text).get("data")
        if not data:
            self.cookies = self.get_cookies(True)
            return
        show_info = json.loads(data.get("result")).get("detailViewComponentMap").get("item")
        self.show_info["show_id"] = show_info.get("staticData").get("itemBase").get("itemId")
        self.show_info["show_name"] = show_info.get("staticData").get("itemBase").get("itemName")
        self.show_info["seat_info"] = list()
        self.show_info["platform"] = 0
        for session in show_info.get("item").get("performBases"):
            session_id = session.get("performs")[0].get("performId")
            session_name = session.get("performs")[0].get("performName")
            t, sign = self.get_seat_params(session_id)
            response = requests.get('https://mtop.damai.cn/h5/mtop.alibaba.detail.subpage.getdetail/2.0/?jsv=2.7.2&appKey=12574478&t=%d&sign=%s&api=mtop.alibaba.detail.subpage.getdetail&v=2.0&H5Request=true&type=originaljson&timeout=10000&dataType=json&valueType=original&forceAntiCreep=true&AntiCreep=true&useH5=true&data={"itemId":"%s","bizCode":"ali.china.damai","scenario":"itemsku","exParams":"{\\"dataType\\":2,\\"dataId\\":\\"%s\\",\\"privilegeActId\\":\\"\\"}","platform":"8","comboChannel":"2","dmChannel":"damai@damaih5_h5"}' % (t, sign, self.performId, session_id), cookies=self.cookies, headers=headers, verify=False, proxies=self.proxy, timeout=10)
            data = json.loads(response.text)
            if not data:
                self.cookies = self.get_cookies(True)
                return
            show_session_info = json.loads(data.get("data").get("result"))
            for seat in show_session_info.get("perform").get("skuList"):
                seat_info = dict()
                seat_info["session_id"] = session_id
                seat_info["session_name"] = session_name
                seat_info["seat_plan_id"] = seat.get("skuId")
                seat_info["seat_plan_name"] = seat.get("priceName")
                self.show_info["seat_info"].append(seat_info)

    def monitor(self) -> list:
        logging.info(f"大麦 {self.show_info.get('show_name')} 监控中")
        can_buy_list = list()
        headers = get_DM_headers()
        t, sign = self.get_show_params()
        response = requests.get('https://mtop.damai.cn/h5/mtop.alibaba.damai.detail.getdetail/1.2/?jsv=2.7.2&appKey=12574478&t=%d&sign=%s&api=mtop.alibaba.damai.detail.getdetail&v=1.2&H5Request=true&type=originaljson&timeout=10000&dataType=json&valueType=original&forceAntiCreep=true&AntiCreep=true&useH5=true&data={"itemId":%s,"platform":"8","comboChannel":"2","dmChannel":"damai@damaih5_h5"}' % (t, sign, self.performId), cookies=self.cookies, headers=headers, verify=False, timeout=10)
        data = json.loads(response.text).get("data")
        if not data:
            self.cookies = self.get_cookies(True)
            return list()
        show_info = json.loads(data.get("result")).get("detailViewComponentMap").get("item")
        for session in show_info.get("item").get("performBases"):
            session_id = session.get("performs")[0].get("performId")
            t, sign = self.get_seat_params(session_id)
            response = requests.get('https://mtop.damai.cn/h5/mtop.alibaba.detail.subpage.getdetail/2.0/?jsv=2.7.2&appKey=12574478&t=%d&sign=%s&api=mtop.alibaba.detail.subpage.getdetail&v=2.0&H5Request=true&type=originaljson&timeout=10000&dataType=json&valueType=original&forceAntiCreep=true&AntiCreep=true&useH5=true&data={"itemId":"%s","bizCode":"ali.china.damai","scenario":"itemsku","exParams":"{\\"dataType\\":2,\\"dataId\\":\\"%s\\",\\"privilegeActId\\":\\"\\"}","platform":"8","comboChannel":"2","dmChannel":"damai@damaih5_h5"}' % (t, sign, self.performId, session_id), cookies=self.cookies, headers=headers, verify=False, timeout=10)
            data = json.loads(response.text)
            if not data:
                self.cookies = self.get_cookies(True)
                return list()
            show_session_info = json.loads(data.get("data").get("result"))
            for seat in show_session_info.get("perform").get("skuList"):
                if seat.get("skuSalable") == "false":
                    continue
                can_buy_list.append(seat.get("skuId"))
        return can_buy_list

    def get_cookies(self, generate=False):
        cookies = {'_m_h5_tk': '3248763e77796ca30ca6f491c67e295d_1695299807188', '_m_h5_tk_enc': 'b5f681b816498129282f003be7b8c547'}
        if generate:
            response = requests.get("https://mtop.damai.cn/h5/mtop.damai.wireless.search.project.classify/1.0/?jsv=2.7.2&appKey=12574478&t=1695289192037&sign=26ff9869af995563292758401df0e5c5&type=originaljson&dataType=json&v=1.0&H5Request=true&AntiCreep=true&AntiFlood=true&api=mtop.damai.wireless.search.project.classify&requestStart=1695288564353&data=%7B%22currentCityId%22%3A%220%22%2C%22cityOption%22%3A1%2C%22pageIndex%22%3A1%2C%22pageSize%22%3A15%2C%22sortType%22%3A3%2C%22categoryId%22%3A0%2C%22returnItemOption%22%3A4%2C%22dateType%22%3A0%2C%22dmChannel%22%3A%22damai%40damaih5_h5%22%7D", headers=get_DM_headers(), verify=False, proxies=self.proxy, timeout=10)
            cookies = requests.utils.dict_from_cookiejar(response.cookies)
        return cookies

    def get_show_params(self):
        token = self.cookies.get("_m_h5_tk").split("_")[0]
        t = int(time.time() * 1000)
        raw = '%s&%d&12574478&{"itemId":%s,"platform":"8","comboChannel":"2","dmChannel":"damai@damaih5_h5"}' % (token, t, self.performId)
        return t, self.encrypt_md5(raw)

    def get_seat_params(self, showId):
        token = self.cookies.get("_m_h5_tk").split("_")[0]
        t = int(time.time() * 1000)
        raw = '%s&%d&12574478&{"itemId":"%s","bizCode":"ali.china.damai","scenario":"itemsku","exParams":"{\\"dataType\\":2,\\"dataId\\":\\"%s\\",\\"privilegeActId\\":\\"\\"}","platform":"8","comboChannel":"2","dmChannel":"damai@damaih5_h5"}' % (token, t, self.performId, showId)
        return t, self.encrypt_md5(raw)

    @staticmethod
    def encrypt_md5(s:str):
        new_md5 = md5()
        new_md5.update(s.encode(encoding='utf-8'))
        return new_md5.hexdigest()
