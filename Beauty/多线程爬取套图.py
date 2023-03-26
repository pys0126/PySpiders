# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     多线程爬取套图
   Description :
   Author :       chenci
   date：          2022/2/10
-------------------------------------------------
"""
from fake_useragent import UserAgent
import requests
from lxml import etree
from threading import Thread
import os
import time


def create_dir_not_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)


# 下载图片
def download_images(download_url, name, page):
    resp = requests.get(url=download_url, headers=header)
    print(resp.url)
    path = f'imgs/{name}'
    create_dir_not_exist(path)
    with open(f'{path}/{page}.jpg', 'wb') as f:
        f.write(resp.content)
        print('下载完成!')


# 获取图片下载链接
def get_images(href, name, max_page):
    for i in range(1, max_page):
        url = href + f'?page={i}'
        resp = requests.get(url=url, headers=header)
        html = etree.HTML(resp.text)
        download_url = html.xpath('//*[@class="entry"]//img/@src')[0]
        download_images(download_url, name, i)


# 获取最大页码和名字
def get_page(href):
    resp = requests.get(url=href, headers=header)
    html = etree.HTML(resp.text)
    max_page = int(html.xpath('//*[@id="dm-fy"]/li/a/text()')[-2])
    name = html.xpath('//*[@id="container"]/main/article/h1/text()')[0]
    get_images(href, name, max_page)


# 获取每一页的图集链接
def get_urls(url):
    resp = requests.get(url=url, headers=header)
    html = etree.HTML(resp.text)
    href = html.xpath('//*[@class="post-box cate2 auth2"]/div/a/@href')
    for i in href:
        href = i
        get_page(href)


# 初始函数
def main(url):
    get_urls(url)


if __name__ == '__main__':
    start = time.time()
    thread_list = []
    for page in range(1, 50):
        url = f'https://www.tuao8.xyz/category-2_{page}.html'
        ua = UserAgent()
        header = {
            'user-agent': ua.random,
            'Referer': 'https://www.tuao8.xyz/category-2.html'
        }
        t = Thread(target=main, args=(url,))
        thread_list.append(t)
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()
    end = time.time()
    print('运行时间:', end - start)
