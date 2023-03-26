import asyncio
import aiohttp
import aiofiles
from lxml import etree


async def send(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.text()
            await get_ip(content)


async def get_ip(content):
    get_ip_html = etree.HTML(content)
    ip_list = get_ip_html.xpath('//tbody/tr/td[1]/text()')
    port_list = get_ip_html.xpath('//tbody/tr/td[2]/text()')
    for ip, port in zip(ip_list, port_list):
        async with aiofiles.open("cache.txt", mode="a", encoding="utf-8") as f:
            await f.write(ip.replace("\n\t", "").replace("\t", "")+":"+port.replace("\n\t", "").replace("\t", "")+"\n")


def clear():
    print("清洗文件")
    with open("cache.txt", mode="r") as f:
        for content in f.readlines():
            if content != "\n":
                if content != "99\n":
                    if content != "9\n":
                        if len(content) == 38:
                            with open("代理IP池.txt", mode="a", encoding="utf-8") as w:
                                w.write(content[:18] + "\n" + content[18:])
                        else:
                            with open("代理IP池.txt", mode="a", encoding="utf-8") as w:
                                w.write(content)


if __name__ == "__main__":
    print("开始抓取")
    urls = [f"https://www.89ip.cn/index_{page_size}.html" for page_size in range(1, 20)]
    tasks = [send(url) for url in urls]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    clear()
    print("完成")
    # asyncio.run(asyncio.wait(tasks))


