from pyspider.libs.base_handler import *
import redis
from pymongo import MongoClient
import requests
import re
import json
import random
import time
from fake_useragent import UserAgent

def user_agent():
    ua=UserAgent()
    return ua.random
r=redis.Redis("127.0.0.1",6666)
class Handler(BaseHandler):
    crawl_config = {
    "proxy":"userame:password@ip:port",
    #"headers":{"User-Agent":user_agent()},
    }

    @every(minutes=0,seconds=30)#设定这两个条件实现30秒循环抓取yic
    @config(age=0)#设定这两个条件实现30秒循环抓取一次
    def on_start(self):
        self.crawl('http://search.guangdongip.gov.cn/page/indexnew',callback=self.index_page,headers={"User-Agent":user_agent()})
    @config(age=0)
    def index_page(self, response):
        cookie = response.cookies
        data={
            "channelId": "FMZL_FT,SYXX_FT,WGZL_AB,FMSQ_FT",
            "checkSimilar": "false",
            "crossLanguage": "",
            "filterChannel": "",
            "filterItems": "",
            "key2Save": "申请（专利权）人=",
            "keyword2Save": "公司",
            "limit": "10",
            "option": "",
            "start": r.lpop("queue:ip_patent_guangdong"),
            "strSortMethod": "",
            "strSources": "",
            "strSynonymous": "",
            "strWhere": "申请（专利权）人=公司"
        }
        self.crawl('http://183.62.9.130/search/doOverviewSearch',method="GET",params=data,cookies=cookie,callback=self.detail_page,headers={"Host":"search.guangdongip.gov.cn","Upgrade-Insecure-Requests":"1","Origin":"http://search.guangdongip.gov.cn","User-Agent":user_agent()})
                
    @config(priority=2)
    def detail_page(self, response):
        print response.url
        cookie = response.cookies
        image_url=[]
        try:
            for images in response.doc(".span3 > img"):
                image_url.append(images.get("src"))
        except Exception as e:
            print e
            for images in response.doc(".span12 > .thumbnails"):
                for imurl in images.xpath(".//img"):
                    image_urls.append(imurl.get("src"))
                image_url.append(image_urls)
        print image_url
        zys=[]
        for zy in response.doc(".muted"):
            zys.append(zy.xpath("string(.)").strip())
        for each,zya,imageu in zip(response.doc(".text-info > a"),zys,image_url):
            zhaiyao=zya
            title=each.text.strip()
            app_num=re.search("(CN.*?\..)",title).group(1)
            title=title.replace("("+app_num+")","")
            #label=labels.text.strip()
            at=each.get("onclick")[12:-2]
            self.crawl("http://search.guangdongip.gov.cn/search/doDetailSearch"+"?pid=%s"%at,callback=self.phantomjs,cookies=cookie,save={"title":title,"app_num":app_num,"abs":zhaiyao,"image_url":imageu})
            
    @config(priority=2)
    def phantomjs(self, response):
        cookie=response.cookies
        d={
           "url":response.url,
           "title": response.save["title"].strip(),
           "app_num": response.save["app_num"].strip(),
           "abs":response.save["abs"],
           "content":response.text,
           "image_url":response.save["image_url"]
        }
        
        #client=connect_mongo()
        #client.insert(d)
        #
        legal_url="http://search.guangdongip.gov.cn/search/doPatentLegalSearch?appNumber=%s"%d["app_num"]
        self.crawl(legal_url,callback=self.request_next,cookies=cookie,save=d)
    @config(priority=10)
    def request_next(self,response):
        dic=response.save
        dic.update({"legal":response.json,"create_time":time.strftime("%Y%m%d",time.localtime())})
        data={
            "spider_name": "ip_patent_gd",
            "content": json.dumps(dic),
            "hash_key": "",
        }
        requests.post(url="api接口", data=data, timeout=20)
        return dic