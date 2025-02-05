pyspider [![Build Status]][Travis CI] [![Coverage Status]][Coverage]
========

A Powerful Spider(Web Crawler) System in Python.

- Write script in Python
- Powerful WebUI with script editor, task monitor, project manager and result viewer
- [MySQL](https://www.mysql.com/), [MongoDB](https://www.mongodb.org/), [Redis](http://redis.io/), [SQLite](https://www.sqlite.org/), [Elasticsearch](https://www.elastic.co/products/elasticsearch); [PostgreSQL](http://www.postgresql.org/) with [SQLAlchemy](http://www.sqlalchemy.org/) as database backend
- [RabbitMQ](http://www.rabbitmq.com/), [Redis](http://redis.io/) and [Kombu](http://kombu.readthedocs.org/) as message queue
- Task priority, retry, periodical, recrawl by age, etc...
- Distributed architecture, Crawl Javascript pages, Python 2.{6,7}, 3.{3,4,5,6} support, etc...

Tutorial: [http://docs.pyspider.org/en/latest/tutorial/](http://docs.pyspider.org/en/latest/tutorial/)  
Documentation: [http://docs.pyspider.org/](http://docs.pyspider.org/)  
Release notes: [https://github.com/binux/pyspider/releases](https://github.com/binux/pyspider/releases)  

Sample Code 
-----------

```python
from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://scrapy.org/', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }
```


Installation
------------
### （1）通过扩展方式直接安装
* `pip install pyspider`
* run command `pyspider`, visit [http://localhost:5000/](http://localhost:5000/)

**WARNING:** WebUI is open to the public by default, it can be used to execute any command which may harm your system. Please use it in an internal network or [enable `need-auth` for webui](http://docs.pyspider.org/en/latest/Command-Line/#-config).

### （2）通过Docker容器方式安装
#### 使用源码重新打包镜像
```
docker build -t pyspider:latest .
```
* 启动服务
```
docker-compose up -d
```
#### 使用官方镜像
```
docker pull binux/pyspider:latest
```

### (3)通过运行代码的方式运行
* 安装phantomjs, 版本要求2.1.1
* 安装node环境，版本要求8.5.0, 安装node扩展包puppeteer@1.15.0和express@4.18.2
* 安装python3.6开发环境，安装项目目录下的requirements.txt扩展
* 运行python run.py启动服务。
备注：服务依赖的counchdb、mysql等中间件可以使用docker-compose.yaml文件中的配置通过docker容器启动


Quickstart: [http://docs.pyspider.org/en/latest/Quickstart/](http://docs.pyspider.org/en/latest/Quickstart/)

Contribute
----------

* Use It
* Open [Issue], send PR
* [User Group]
* [中文问答](http://segmentfault.com/t/pyspider)


TODO
----

### v0.4.0

- [ ] a visual scraping interface like [portia](https://github.com/scrapinghub/portia)


优秀的项目
----------
- [https://github.com/chancechang/pySpider](https://github.com/chancechang/pySpider)
- 


License
-------
Licensed under the Apache License, Version 2.0


[Build Status]:         https://img.shields.io/travis/binux/pyspider/master.svg?style=flat
[Travis CI]:            https://travis-ci.org/binux/pyspider
[Coverage Status]:      https://img.shields.io/coveralls/binux/pyspider.svg?branch=master&style=flat
[Coverage]:             https://coveralls.io/r/binux/pyspider
[Try]:                  https://img.shields.io/badge/try-pyspider-blue.svg?style=flat
[Issue]:                https://github.com/binux/pyspider/issues
[User Group]:           https://groups.google.com/group/pyspider-users
