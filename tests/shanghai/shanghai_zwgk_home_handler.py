#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2023-08-03 21:32:53
# Project: shanghaizhengwu

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
        'headers': {
            # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko)',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            # 'Host':'shanghai.gov.cn'
        }
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://www.shanghai.gov.cn/nw2319/index.html', callback=self.index_page, validate_cert=False)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.detail_page, validate_cert=False)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }

    def on_result(self, result):
        if result:
            return super(Handler, self).on_result(result)
        
    # def save_to_conchdb(self,result):
    #     if self.db['chinastrip'].insert(result):
    #         print('save to mongo',result)