#_*_ coding:utf-8 _*_
import os
import requests
import time
from lxml import etree


class wallhaven_spider(object):
    def __init__(self,keyword):
        self.keyword=keyword
        self.headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36",
        }
        self.filePath = str(keyword)+"\\"
        if not os.path.exists(self.filePath):
            os.mkdir(self.filePath)

    def getLinks(self,number):
        keyword=self.keyword
        url = ("https://alpha.wallhaven.cc/search?q={}&categories=010&purity=110&sorting=relevance&order=desc&page={}").format(keyword,number)
        try:
            html = requests.get(url)
            selector = etree.HTML(html.text)
            pic_Linklist = selector.xpath('//a[@class="jsAnchor thumb-tags-toggle tagged"]/@href')
        except Exception as e:
            print(repr(e))
        return pic_Linklist
    
    def get_page(self):
        keyword=self.keyword
        total = ""
        url = ("https://alpha.wallhaven.cc/search?q={}&categories=010&purity=110&sorting=relevance&order=desc").format(keyword)
        html = requests.get(url)
        selector = etree.HTML(html.text)
        pageInfo = selector.xpath('//header[@class="listing-header"]/h1[1]/text()')
        string = str(pageInfo[0])
        numlist = list(filter(str.isdigit,string))
        for item in numlist:
            total += item
        totalPagenum = int(total)
        return totalPagenum

    def download(self,url,count):
        keyword=self.keyword
        string = url.strip('/thumbTags').strip('https://alpha.wallhaven.cc/wallpaper/')
        html = 'http://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-' + string + '.jpg'
        pic_path = (self.filePath + keyword + str(count) + '.jpg' )
        try:
            start = time.time()
            pic = requests.get(html,headers = self.headers)
            f = open(pic_path,'wb')
            f.write(pic.content)
            f.close()
            end = time.time()
            print(f"{count}张图片已经被下载,花费:",end - start,'s')
        except Exception as e:
            print(repr(e))
    
    def run(self):
        keyword=self.keyword
        count = self.get_page()
        print("已为您找到{}项结果！".format(count))
        times = int(count/24 + 1)
        j = 1
        start = time.time()
        for i in range(times):
            pic_Urls = self.getLinks(i+1)
            start2 = time.time()
            for img in pic_Urls:
                self.download(img,j)
                j += 1
            end2 = time.time()
            print('本页花费时间：',end2 - start2,'s')
        end = time.time()
        print('共花费时间:',end - start,'s')
