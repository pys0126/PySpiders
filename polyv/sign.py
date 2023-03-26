import requests

session = requests.Session()

def login():
    url = "https://uc.tmooc.cn/login"
    headers = {
        "Referer": "https://www.tmooc.cn/",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.42"
    }
    data = {
        "loginName": "2493919891@qq.com",
        "password": "ad1e31a5eb6ade690c65e7758fb90032",
        "imgCode": "",
        "accountType": "1",
        "whetherIntranet": "10121002"
    }
    res = session.post(url=url, data=data, headers=headers)
    return res.json()

def sign():
    if login()["code"] != 1:
        print("Login failed")

    url = "https://tts.tmooc.cn/studentCenter/studentSign?studentClaId=990120"
    res = session.get(url=url, headers={
        "cookie": "isCenterCookie=no; ssss990120=0; Hm_lvt_51179c297feac072ee8d3f66a55aa1bd=1667899173; TMOOC-SESSION=28a662533d9a46beb06bc07393da940c; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22E_bfv5lpu%22%2C%22first_id%22%3A%221845689adae83b-08703b8ec8b9fa-7d5d5474-2073600-1845689adafd50%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfbG9naW5faWQiOiJFX2JmdjVscHUiLCIkaWRlbnRpdHlfY29va2llX2lkIjoiMTg0NTY4OWFkYWU4M2ItMDg3MDNiOGVjOGI5ZmEtN2Q1ZDU0NzQtMjA3MzYwMC0xODQ1Njg5YWRhZmQ1MCJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22E_bfv5lpu%22%7D%2C%22%24device_id%22%3A%221845689adae83b-08703b8ec8b9fa-7d5d5474-2073600-1845689adafd50%22%7D; sessionid=28a662533d9a46beb06bc07393da940c|E_bfv5lpu; tesSessionId=28a662533d9a46beb06bc07393da940c; tedu.local.language=zh-CN; Hm_lvt_e997f0189b675e95bb22e0f8e2b5fa74=1667899183; href=https%3A%2F%2Ftts.tmooc.cn%2FstudentCenter%2FtoMyttsPage; Hm_lpvt_51179c297feac072ee8d3f66a55aa1bd=1668477388; cloudAuthorityCookie=0; versionListCookie=JSDTN202208001; defaultVersionCookie=JSDTN202208001; versionAndNamesListCookie=JSDTN202208001N22NJAVA%25E5%2585%25A8%25E6%2597%25A5%25E5%2588%25B6%25E8%25AF%25BE%25E7%25A8%258BV14%25EF%25BC%25882208-2211%25E7%25B3%25BB%25E5%2588%2597%25E7%258F%25AD%25EF%25BC%2589N22N990120; courseCookie=JAVA; stuClaIdCookie=990120; qimo_seosource_0=%E5%85%B6%E4%BB%96%E7%BD%91%E7%AB%99; qimo_seokeywords_0=%E6%9C%AA%E7%9F%A5; uuid_62ee1ae0-e34d-11ea-a69b-c5bb157be2a1=6eff5070-7c1e-4d29-a2d1-ded1c196dc58; qimo_seosource_62ee1ae0-e34d-11ea-a69b-c5bb157be2a1=%E5%85%B6%E4%BB%96%E7%BD%91%E7%AB%99; qimo_seokeywords_62ee1ae0-e34d-11ea-a69b-c5bb157be2a1=%E6%9C%AA%E7%9F%A5; qimo_xstKeywords_62ee1ae0-e34d-11ea-a69b-c5bb157be2a1=; accessId=62ee1ae0-e34d-11ea-a69b-c5bb157be2a1; JSESSIONID=C9623003E13502AB9FE3725BD98A29F9; Hm_lpvt_e997f0189b675e95bb22e0f8e2b5fa74=1668478373; pageViewNum=4"
    })
    print(res.text)

if __name__ == '__main__':
    sign()