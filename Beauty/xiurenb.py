'''
多线程爬取
'''
from threading import Thread
from lxml import etree
import requests
import os

session = requests.Session()
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.70"
}

def create_dir(save_path: str, dir_name: str):
    try:
        os.makedirs(save_path + "/" + dir_name)
    except:
        pass
    finally:
        print(save_path + "/" + dir_name)

def get_all_photo_pack():
    new_100_url = "https://www.xiurenb.cc/new.html"
    res = session.get(url=new_100_url, headers=headers)
    res.encoding = "UTF-8"
    lxml_html = etree.HTML(res.text)
    all_photo_pack_url = ["https://www.xiurenb.cc" + photo_pack_url for photo_pack_url in lxml_html.xpath('//ul[@class="update_area_lists cl"]/li/a/@href')]    
    return all_photo_pack_url
        
def download_all_photo_pack(save_path: str, photo_pack_url: str):
    res = session.get(url=photo_pack_url, headers=headers)
    res.encoding = "UTF-8"
    lxml_html = etree.HTML(res.text)
    photo_pack_title = lxml_html.xpath('//div[@class="item_title"]/h1/text()')[0]
    create_dir(save_path=save_path, dir_name=photo_pack_title)
    
    all_page_url = lxml_html.xpath('//div[@class="page"]//a/@href')
    all_photo_url = all_page_url[1:len(all_page_url)//2-1]
    for page_url in all_photo_url:
        page_res = session.get(url="https://www.xiurenb.cc" + page_url, headers=headers)
        page_res.encoding = "UTF-8"
        page_lxml_html = etree.HTML(page_res.text)
        one_page_photo_src_list = page_lxml_html.xpath('//div[@class="content"]//img/@src')
        for one_page_photo_src in one_page_photo_src_list:
            get_photo = session.get(url="https://www.xiurenb.cc" + one_page_photo_src, headers=headers)
            save_photo_name = save_path + "/" + photo_pack_title + "/" + one_page_photo_src.split("/")[-1]
            with open(save_photo_name, "wb") as f:
                f.write(get_photo.content)
            print(save_photo_name)

if __name__ == "__main__":
    save_path = "./xiurenb"
    all_photo_pack_url = get_all_photo_pack()

    tasks = []
    for photo_pack_url in all_photo_pack_url:
        t = Thread(target=download_all_photo_pack, args=(save_path, photo_pack_url))
        tasks.append(t)
    for task in tasks:
        task.start()
    for task in tasks:
        task.join()

