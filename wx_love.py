import requests
import schedule
import itchat
import time

ToUser = "女友的备注"
content = []
Sessions = requests.session()
itchat.auto_login(hotReload=True)  # hotReload=True用于存储登录信息

# 请求情话api
def parse():
    url = "https://api.lovelive.tools/api/SweetNothings"  # "https://chp.shadiao.app/api.php"
    re = Sessions.get(url=url)
    content.append(re.text)


# 发送微信消息
def sen_msg(size):
    print(content[size])
    user = itchat.search_friends(ToUser)
    itchat.send(content[size], toUserName=user[0]["UserName"])


# 启动
def run():
    for i in range(99):
        parse()
        sen_msg(size=i)


schedule.every().thursday.at("13:14").do(run)  # 星期四的13:14发一次
while True:
    schedule.run_pending()
    time.sleep(1)
