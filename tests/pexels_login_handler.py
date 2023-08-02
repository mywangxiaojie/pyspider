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
        self.crawl('https://www.pexels.com/zh-cn/login/', callback=self.login, validate_cert=False)
 
    @config(age=1 * 24 * 60 * 60)
    def login(self, response):
        cookies = response.cookies
        base_url = 'https://www.pexels.com/zh-cn/api/v2/auth/sign_in?cachebust=true'
        url = base_url
        data = {}
        for each in response.doc("form input"):
            data[each.name]=each.value
            if each.name == "email":
                data["email"] = "1873297122@qq.com"
            if each.type == "password":
                data[each.name] = "pexels@467321"
        print("-----------------", data)
        headers = {}
        headers["Content-Type"]="application/x-www-form-urlencoded"
        headers["Referer"]="https://www.pexels.com/zh-cn/login/"
        headers["Origin"]="https://www.pexels.com/"
        headers["Referer"]="https://www.pexels.com/zh-cn/login/"
        self.crawl(url, callback=self.login_ok,data=data,cookies=cookies,headers=headers,method="POST", validate_cert=False)
        
 
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
        
        self.crawl("https://www.pexels.com/zh-cn/new-photos/",
                   cookies=response.cookies,callback=self.index_page, validate_cert=False)
        
        
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.detail_page, validate_cert=False)