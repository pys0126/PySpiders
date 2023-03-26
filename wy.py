import xlwt
import requests
from bs4 import BeautifulSoup
import re
from fake_useragent import UserAgent

session = requests.Session()
headers = {
    "user-agent": str(UserAgent().random)
}
url = 'http://music.163.com/discover/artist/cat?id=1001'
r = session.get(url=url, headers=headers, proxies=proxy)
r.raise_for_status()
r.encoding = r.apparent_encoding
html = r.text
soup = BeautifulSoup(html, 'html.parser')
top_10 = soup.find_all('div', attrs={'class': 'u-cover u-cover-5'})
singers = []
for i in top_10:
    singers.append(re.findall(r'.*?<a class="msk" href="(.*?)" title="(.*?)的音乐".*?', str(i)))
print(singers)
url = 'http://music.163.com'
book = xlwt.Workbook()
for singer in singers:
    new_url = url + str(singer[0])
    songs = session.get(new_url, headers=headers).text
    soup = BeautifulSoup(songs, 'html.parser')
    Info = soup.find_all('textarea', attrs={'style': 'display:none;'})[0]
    songs_url_and_name = soup.find_all('ul', attrs={'class': 'f-hide'})[0]
    datas = []
    data1 = re.findall(r'"album".*?"name":"(.*?)".*?', str(Info.text))
    data2 = re.findall(r'.*?<li><a href="(/song\?id=\d+)">(.*?)</a></li>.*?', str(songs_url_and_name))
    for i in range(len(data2)):
        datas.append([data2[i][1], data1[i], 'http://music.163.com/#' + str(data2[i][0])])
    print(singer[1])
    sheet1 = book.add_sheet(singer[1], cell_overwrite_ok=True)  # (添加工作表，并设置同一单元格可以重复写
    sheet1.col(0).width = (25 * 256)
    sheet1.col(1).width = (30 * 256)
    sheet1.col(2).width = (40 * 256)
    heads = ['歌曲名称', '专辑', '歌曲链接']
    count = 0
    for head in heads:
        sheet1.write(0, count, head)
        count += 1
    i = 1
    for data in datas:
        j = 0
        for k in data:
            sheet1.write(i, j, k)
            j += 1
        i += 1
book.save("1.xls")  # 活号里写存入的地址
