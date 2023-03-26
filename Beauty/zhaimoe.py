'''
多线程+异步爬虫
'''

import asyncio
import requests
import time
import os
import aiofiles
from lxml import etree
from threading import Thread
from aiohttp import ClientSession


def get_all_photos_spider(page_size: int, all_photo_url: list, all_photo_title: list):
    # 提取每页所有的图集URL并保存到一个List容器
    main_url = f"https://www.zhaimoe.com/portal/List/index?id=3&page={str(page_size)}"
    main_res = session.get(url=main_url, headers=headers)
    page_photos_urls = parser(main_res.text, '//div[@class="col-md-3 col-xs-6"]//h3/a/@href')
    page_photos_titles = parser(main_res.text, '//div[@class="col-md-3 col-xs-6"]//h3/a/text()')
    for photos_urls in page_photos_urls:
        all_photo_url.append("https://www.zhaimoe.com" + photos_urls)
    for photo_title in page_photos_titles:
        try:
            os.makedirs(f"./www.zhaimoe.com/{photo_title}")
        except:
            pass
        all_photo_title.append(photo_title)


def get_all_photos(page_start: int = 1, page_stop: int = 1):
    # page_start：起始页默认为第一页， page_stop：结束页默认为第一页
    # 利用多线程提取所有图集的url，并返回
    all_photo_url = []
    all_photo_title = []
    thread_list = []
    for page_size in range(page_start, page_stop + 1):
        # get_all_photos_spider(page_size, all_photo_url)
        create_thread = Thread(target=get_all_photos_spider, args=(page_size, all_photo_url, all_photo_title))
        thread_list.append(create_thread)
    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()
    return all_photo_url, all_photo_title


def parser(html: str, xpath: str):
    parser_text = etree.HTML(html).xpath(xpath)
    return parser_text


async def download_photo(url: str, title: str):
    async with ClientSession(headers=headers) as Session:
        async with Session.get(url) as photo_page_response:
            html = await photo_page_response.text(errors="ignore")
            photo_urls = parser(html, '//p/img[@class="pimg lazyload"]/@src')
        item = 0
        print(title)
        for photo_url in photo_urls:
            item += 1
            async with Session.get(photo_url) as photo_response:
                async with aiofiles.open(f"./www.zhaimoe.com/{title}/{str(item)}.jpg", "wb") as af:
                    await af.write(await photo_response.read())


async def get_photo_urls(urls: list, titles: list):
    tasks = []
    for url, title in zip(urls, titles):
        task = asyncio.ensure_future(download_photo(url, title))
        tasks.append(task)
    await asyncio.wait(tasks)


if __name__ == "__main__":
    start_time = time.time()

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.43"
    }
    session = requests.Session()
    #page_start起始页，page_stop停止页，一页28个图集
    all_photos_url, all_photos_title = get_all_photos(page_start=1, page_stop=5)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(get_photo_urls(all_photos_url, all_photos_title))

    stop_time = time.time()
    print("总耗时: ", stop_time - start_time)
