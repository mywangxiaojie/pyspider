#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-11-05 11:41:06
# Project: sinaweibo
# SinaUser:username@sina.cn
from pyspider.libs.base_handler import *
 
 
class Handler(BaseHandler):
    crawl_config = {
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko)',
        }
    }
    
 
    @every(minutes=24 * 60)
    def on_start(self):
        
        self.crawl('http://login.weibo.cn/login/', callback=self.login)
 
    @config(age=1 * 24 * 60 * 60)
    def login(self, response):
        cookies = response.cookies
        base_url = 'http://login.weibo.cn/login/'
        url = base_url + response.doc("form").attr("action")
        data = {}
        for each in response.doc("form input"):
            data[each.name]=each.value
            if each.name == "mobile":
                data["mobile"] = "username@sina.cn"
            if each.type == "password":
                data[each.name] = "password"
        headers = {}
        headers["Content-Type"]="application/x-www-form-urlencoded"
        headers["Referer"]="http://login.weibo.cn/login/"
        headers["Origin"]="http://login.weibo.cn"
        headers["Referer"]="http://login.weibo.cn/login/"
        self.crawl(url, callback=self.login_ok,data=data,cookies=cookies,headers=headers,method="POST")
        
 
    @config(priority=2)
    def login_ok(self, response):
        '''
        return {
            "url": response.url,
            "headers": response.headers,
            "cookies": response.cookies,
            "status":response.status_code,
            "text":response.text,
        }
        '''
        
        self.crawl("http://weibo.cn/yumayin",
                   cookies=response.cookies,callback=self.index_page)
        
    def index_page(self, response):
        
        weibos  = []
        for each in response.doc("div.c").items():
            #each.find("span.kt"):
            if each.find("span.kt").html()!= None:
                continue
            #if each.find("span.ctt")!= None:
            if each.find("span.ctt").html()!= None:
                weibos.append(each.find("span.ctt").html())    
        return weibos