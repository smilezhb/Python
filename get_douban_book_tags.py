# -*- coding:utf-8 -*-
import requests
from lxml import etree

if __name__ == '__main__':
    url = "https://book.douban.com/tag/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    }
    page_text = requests.get(url=url,headers=headers).text
    tree = etree.HTML(page_text)
    td_list = tree.xpath('//table[@class="tagCol"]/tbody/tr/td')
    tag_list = []
    for td in td_list:
        tag = td.xpath('./a/text()')[0]
        tag_list.append(tag)
    print(tag_list)
    with open('douban_tag.txt','w',encoding='utf-8') as f:
        f.writelines('\n'.join(tag_list))
    print("豆瓣图书标签，下载成功!")

