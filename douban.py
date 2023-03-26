import requests
import csv
from lxml import etree

headers = {
    'Referer': 'https://accounts.douban.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0',
    'Cookie': 'bid=eOSDcDum3Bo; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1654826427%2C%22https%3A%2F%2Faccounts.douban.com%2F%22%5D; _pk_id.100001.4cf6=bfca0d1ddbebfa22.1654822299.2.1654830872.1654822740.; __utma=30149280.1351571282.1654822300.1654822300.1654826427.2; __utmc=30149280; __utmz=30149280.1654826427.2.2.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=223695111.1935026336.1654822300.1654822300.1654826427.2; __utmc=223695111; __utmz=223695111.1654826427.2.2.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __gads=ID=14e81f6d3b3a29e4-220fbc5ce1d300bf:T=1654822301:RT=1654822301:S=ALNI_MZ01Pyq0dK_kUo6MImdsirAWZuJyw; __gpi=UID=000006841139e3db:T=1654822301:RT=1654822301:S=ALNI_MYSs0K6YUJT7v2Y8e-XMeJySS8Urw; dbcl2="248903511:O2Hhnoxn7HM"; ck=mhsa; _pk_ses.100001.4cf6=*; __utmb=30149280.8.10.1654826427; __utmb=223695111.0.10.1654826427; push_noty_num=0; push_doumail_num=0; ll="108309"; _vwo_uuid_v2=DD991B9B3A67E15FF9A7B6E66364FEC37|ce4991dd4e1a8732ac48053e16895075; __utmv=30149280.24890; __utmt=1; ct=y'
}
session = requests.Session()


def fetch(url):
    res = session.get(url=url, headers=headers)
    return res


def parse(text):
    html = etree.HTML(text)
    if html.xpath("/html/body/div[3]/div[1]/div/div[1]/h2/text()")[0] == "…你访问豆瓣的方式有点像机器人程序。为了保护用户的数据，请向我们证明你是人类:":
        img_url = html.xpath('//form[@method="POST"]/img/@src')[0]
        with open("./code.jpg", 'wb') as f:
            f.write(fetch(img_url).content)
        code = input("请输入验证码：")

    rows = []
    try:
        for info in html.xpath('//div[@class="item"]//div[@class="info"]'):
            name = info.xpath('.//div[@class="hd"]//a/span[1]/text()')[0]
            year = info.xpath('.//div[@class="bd"]//p/text()')[1].split("\n")[1].replace(" ", "").split("/")[0].replace("\xa0", "")
            pingfen = info.xpath('.//div[@class="bd"]//div[@class="star"]/span[2]/text()')[0]
            pingfen_size = info.xpath('.//div[@class="bd"]//div[@class="star"]/span[4]/text()')[0].split("人")[0]

            movie_url = info.xpath('.//div[@class="hd"]//a/@href')[0]
            response = fetch(movie_url)
            movie_html = etree.HTML(response.text)
            pianchang = movie_html.xpath('//div[@id="info"]/span[@property="v:runtime"]')[0].text
            IMDb = movie_html.xpath('//div[@id="info"]/text()')[-2].replace(" ", "")

            guojia = info.xpath('.//div[@class="bd"]//p/text()')[1].split("\n")[1].replace(" ", "").split("/")[1].replace("\xa0", "")
            movie_type = info.xpath('.//div[@class="bd"]//p/text()')[1].split("\n")[1].replace(" ", "").split("/")[2].replace("\xa0", "")
            rows.append([name, year, pingfen, pingfen_size, pianchang, guojia, movie_type, IMDb])
    except Exception as e:
        print(e)
        print(html.xpath('//form[@method="POST"]/img/@src'))
    return rows


def save(rows):
    heads = ["电影名称", "年份", "评分", "评价人数", "片长", "制片国家", "类型", "IMDb号"]
    with open("./豆瓣TOP250.csv", "a", newline="", encoding="ANSI") as f:
        f_csv = csv.writer(f)
        f_csv.writerow(heads)
        f_csv.writerows(rows)


def main():
    douban_url_list = [f"https://movie.douban.com/top250?start={size}" for size in range(75, 250, 25)]
    for douban_url in douban_url_list:
        response = fetch(douban_url)
        moive_parse = parse(response.text)
        print(moive_parse)
        # save(moive_parse)


if __name__ == "__main__":
    main()

