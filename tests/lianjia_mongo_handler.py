
# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-03-21 14:41:55
# Project: lianjia_spider

from pyspider.libs.base_handler import *
from lxml import etree
import pymongo

class Handler(BaseHandler):
    crawl_config = {
    }
    def __init__(self):
        connection = pymongo.MongoClient(host='192.168.180.128',port=27017)
        client = connection['lianjia']
        self.db = client['items']

    @every(minutes=24 * 60)
    def on_start(self):
        for i in range(1,101):
            self.crawl('https://dg.lianjia.com/ershoufang/pg{}'.format(i), callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        seletor = etree.HTML(response.text)
        urls  =seletor.xpath('//li[@class ="clear LOGCLICKDATA"]/a/@href')
        for url in urls  :
            self.crawl(url, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }
    
    @config(priority=2)
    def on_result(self, result):
        self.db.save(result)
