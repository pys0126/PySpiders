'''
达内网课刷礼物
'''
import requests
import random
import threading
import time

def fetch(good_id: int = 1):
    '''
    good_id: 礼物id
    '''
    url = f"http://live.polyv.cn/watch/wxpay_donate?donate_type=good&channel_id=3436752&roomId=3436752&good_id={good_id}"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "Cookie": "language=zh_CN; UM_distinctid=184541dcad9559-02a3a1583f9aa-c505425-1fa400-184541dcada564; CNZZDATA1279149660=244417426-1667886360-https%253A%252F%252Ftts.tmooc.cn%252F%7C1668644743; SESSION=5fd7425c-b1e0-4fdc-8031-81afce8c3e3b",
        "Referer": "https://live.polyv.cn/watch/3436752?userid=E_bfv5lpu,990120,1310484M111Mtts&ts=1667906146374&sign=a1a8592d10af8bab706f77263af30b44"
    }
    res = requests.post(url=url, headers=headers)
    print(res.text)

if __name__ == "__main__":
    tasks = []
    for _ in range(15):
        randomint = random.randint(1, 9)
        task = threading.Thread(target=fetch, args=(randomint,))
        tasks.append(task)

    for task in tasks:
        task.start()

    for task in tasks:
        task.join()
    