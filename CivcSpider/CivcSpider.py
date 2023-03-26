import requests
from PIL import Image
from xpinyin import Pinyin
from bs4 import BeautifulSoup

session = requests.Session()
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.59"
}
user = "2020080301005"
pwd = "bmw-m3gtr"
pinyin = Pinyin()

login_jiaowu_url = "http://xj.cqcivc.cn/default2.aspx"
login_jiaowu_get_re = session.get(url=login_jiaowu_url, headers=header)
login_jiaowu_get_re.encoding = "gb2312"
login_jiaowu_get_bs = BeautifulSoup(login_jiaowu_get_re.text, "lxml")
__VIEWSTATE = login_jiaowu_get_bs.find(type="hidden")["value"]
RadioButtonList1 = login_jiaowu_get_bs.find_all(type="radio")[2]["value"]
Button1 = login_jiaowu_get_bs.find(type="submit")["value"]

# 获取验证码图片
login_jiaowu_CheckCode = "http://xj.cqcivc.cn/CheckCode.aspx"
login_jiaowu_CheckCode_re = session.get(url=login_jiaowu_CheckCode, headers=header)
with open("CheckCode.jpg", "wb") as f:
    f.write(login_jiaowu_CheckCode_re.content)
CheckCode = Image.open("CheckCode.jpg")
CheckCode.show()

# 根据获取的验证码图片进行登录
TextBox3 = input("输入验证码：")
login_jiaowu_post_re = session.post(url=login_jiaowu_url, data={
    "__VIEWSTATE": __VIEWSTATE,
    "TextBox1": user,
    "TextBox2": pwd,
    "TextBox3": TextBox3,
    "RadioButtonList1": RadioButtonList1,
    "Button1": Button1
}, headers=header)
login_jiaowu_post_re.encoding = "gb2312"
login_jiaowu_post_bs = BeautifulSoup(login_jiaowu_post_re.text, "lxml")


def get_user_info():
    get_user_info_url = "http://xj.cqcivc.cn/" + login_jiaowu_post_bs.find_all(class_="top")[3].find(class_="sub").a[
        "href"]
    get_user_info_re = session.get(url=get_user_info_url, headers=header)
    get_user_info_bs = BeautifulSoup(get_user_info_re.text, "lxml")
    get_user_info_body = get_user_info_bs.find(class_="mid_box").find()  # 未写完

    pinyin.get_initials("传入汉字", "").lower()  # 将汉字转换成拼音，并小写字母
