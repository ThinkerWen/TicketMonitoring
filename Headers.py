def get_DM_headers() -> dict:
    return {
        'authority': 'mtop.damai.cn',
        'accept': 'application/json',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://m.damai.cn',
        'pragma': 'no-cache',
        'referer': 'https://m.damai.cn/',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    }


def get_MY_headers(perform_id: int) -> dict:
    return {
        'Host': 'wx.maoyan.com',
        'X-Channel-ID': '70001',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF XWEB/30817',
        'Content-Type': 'multipart/form-data',
        'X-Requested-With': 'wxapp',
        'xweb_xhr': '1',
        'x-wxa-page': 'pages/show/detail/index',
        'x-wxa-referer': 'pages/search/index',
        'x-wxa-query': f'%7B%22id%22%3A%22{perform_id}%22%2C%22utm_source%22%3A%22wxwallet_search%22%7D',
        'version': 'wallet-v4.5.11',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://servicewechat.com/wxdbb4c5f1b8ee7da1/1366/page-frame.html',
        'Accept-Language': 'zh-CN,zh',
    }


def get_FWD_headers() -> dict:
    return {
        'Host': 'api.livelab.com.cn',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF XWEB/30817',
        'xweb_xhr': '1',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://servicewechat.com/wx5a8f481d967649eb/70/page-frame.html',
        'Accept-Language': 'zh-CN,zh',
    }
