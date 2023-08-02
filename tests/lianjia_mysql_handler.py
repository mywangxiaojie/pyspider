
# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-03-21 14:41:55
# Project: lianjia_spider

from pyspider.libs.base_handler import *
from lxml import etree
import pymysql


class Handler(BaseHandler):
    crawl_config = {
    }

    def __init__(self):
        db_config = {
            'host': '192.168.180.128',
            'user': 'admin',
            'password': 'Root110qwe',
            'db': 'lianjia',
            'charset': 'utf8',
            'port': 3306
        }
        self.db = pymysql.connect(**db_config)
        self.cur = self.db.cursor()
        # 创建表items
        sql1 = 'create table if not exists items  (url varchar(255) NOT NULL ,title VARCHAR(255) NOT NULL)'
        self.cur.execute(sql1)

    @every(minutes=24 * 60)
    def on_start(self):
        for i in range(1, 101):
            self.crawl('https://dg.lianjia.com/ershoufang/pg{}'.format(i), callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        seletor = etree.HTML(response.text)
        urls = seletor.xpath('//li[@class ="clear LOGCLICKDATA"]/a/@href')
        for url in urls:
            self.crawl(url, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }

    @config(priority=2)
    def on_result(self, result):
        sql2 = 'insert into items(url,title) values(%s, %s)'
        try:
            if result['url']:
                self.cur.execute(sql2, (result['url'], result['title']))
        except Exception as e:
            self.db.rollback()
            print(e)
        else:
            self.db.commit()
