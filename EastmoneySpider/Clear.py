import requests
import csv
import json
import datetime
import os

print("开始获取...")
Url = "http://data.eastmoney.com/xg/xg/default.html"
GetData = requests.get("http://data.eastmoney.com/xg/xg/default.html")
with open("cache.txt", "w", encoding="utf-8") as w:
    w.write(GetData.text.replace(" ", ""))

with open("cache.txt", "r", encoding="utf-8") as r:
    for rr in r.readlines():
        OutData = rr.replace("\n", "")
        if OutData[:11] == "varpagedata":
            with open("cache.json", "w", encoding="utf-8") as j:
                j.write(OutData[12:].rstrip(";"))

with open("cache.json", "r", encoding="utf-8") as rj:
    PayloadJson = json.load(rj)

InfoTitle = ["股票代码", "股票简称", "发型价格", "申购日期"]
InfoList = []
# 股票代码，股票简称，发型价格，申购日期
for GpInfo in PayloadJson["xgsg"]["data"]:
    Securitycode = GpInfo["securitycode"]  # 股票代码
    Securityshortname = GpInfo["securityshortname"]  # 股票简称
    Issueprice = str(GpInfo["issueprice"])  # 发型价格
    Purchasedate = GpInfo['purchasedate'][5:-9]  # 申购日期

    MbDate = datetime.datetime.strptime(Purchasedate, "%m-%d")
    NowDate = datetime.datetime.strptime(datetime.datetime.now().strftime('%m-%d'), "%m-%d")
    NowWeek = datetime.datetime.now().weekday() + 1
    Delta = MbDate - NowDate
    PurchasedateWeek = GpInfo['purchasedate'][5:-9] + " " + str((NowWeek + Delta.days) % 7)  # 最终申购日期
    InfoList.append([Securitycode, Securityshortname, Issueprice, PurchasedateWeek])

with open('股票信息.csv', 'w')as f:
    f_csv = csv.writer(f)
    f_csv.writerow(InfoTitle)
    f_csv.writerows(InfoList)
print("保存在当前路径下：股票信息.csv")
print("清理缓存文件...")
os.system("del cache.txt")
os.system("del cache.json")
print("清理完成")




