import requests
import aiohttp
import asyncio
import json
import csv
import os
import datetime

# 获取总页数
IndexUrl = "http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get?callback=jQuery112305322698587246995_1623936943787&st=purchasedate%2Csecuritycode&sr=-1&ps=50&p=55&type=XGSG_LB&js=%7B%22data%22%3A(x)%2C%22pages%22%3A(tp)%7D&token=894050c76af8597a853f5b408b759f5d"
IndexRe = requests.get(IndexUrl)
DataJson = json.loads(IndexRe.text.replace("jQuery112305322698587246995_1623936943787(", "").rstrip(")"))

DataUrlList = [f"http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get?callback=jQuery112305322698587246995_1623936943787&st=purchasedate%2Csecuritycode&sr=-1&ps=50&p={Page}&type=XGSG_LB&js=%7B%22data%22%3A(x)%2C%22pages%22%3A(tp)%7D&token=894050c76af8597a853f5b408b759f5d" for Page in range(1, int(DataJson["pages"])+1)]

InfoTitle = ["股票代码", "股票简称", "发型价格", "申购日期"]
InfoList = []


# 获取所有股票信息
async def AioDownload(url):
    async with aiohttp.ClientSession() as Session:
        async with Session.get(url) as Res:
            GpInfo = await Res.text()
            for DataJson in json.loads(GpInfo.replace("jQuery112305322698587246995_1623936943787(", "").rstrip(")"))["data"]:
                Securitycode = DataJson["securitycode"]  # 股票代码
                Securityshortname = DataJson["securityshortname"]  # 股票简称
                Issueprice = str(DataJson["issueprice"])  # 发型价格
                Purchasedate = DataJson['purchasedate'][5:-9]  # 申购日期

                # MbDate = datetime.datetime.strptime(Purchasedate, "%m-%d")
                # NowDate = datetime.datetime.strptime(datetime.datetime.now().strftime('%m-%d'), "%m-%d")
                # NowWeek = datetime.datetime.now().weekday() + 1
                # Delta = MbDate - NowDate
                # PurchasedateWeek = DataJson['purchasedate'][5:-9] + " 周" + str((NowWeek + Delta.days) % 7)  # 最终申购日期
                InfoList.append([Securitycode, Securityshortname, Issueprice, Purchasedate])

# 运行函数
async def Main():
    Tasks = []
    for DataUrl in DataUrlList:
        Tasks.append(AioDownload(DataUrl))

    await asyncio.wait(Tasks)

# run
if __name__ == "__main__":
    asyncio.run(Main())
    try:
        os.mkdir("./股票信息")
    except:
        pass
    with open(f'./股票信息/{datetime.datetime.now().strftime("%m-%d")}股票信息.csv', 'w', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(InfoTitle)
        f_csv.writerows(InfoList)
    print(f"保存在当前路径'股票信息'文件夹下：{datetime.datetime.now().strftime('%m-%d')}股票信息.csv")