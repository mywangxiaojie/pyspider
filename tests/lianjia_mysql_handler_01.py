from pyspider.libs.base_handler import *
import pymysql

class Handler(BaseHandler):
    crawl_config = {
    }

    def __init__(self):
        # 下面参数修改成自己对应的 MySQL 信息 
        self.db = MySQLdb.connect(ip, username, password, db, charset='utf8')

    def add_Mysql(self, title, unit_price, sell_point):
        try:
            cursor = self.db.cursor()
            sql = 'insert into house(title, unit_price, sell_point) values ("%s","%s","%s")' % (title[0],unit_price[0],sell_point);  
            print(sql)
            cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://hz.lianjia.com/ershoufang/', callback=self.index_page,validate_cert=False)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.title').items():
            self.crawl(each.attr.href, callback=self.detail_page,validate_cert=False)

    @config(priority=2)
    def detail_page(self, response):
        title = response.doc('.main').text(),
        unit_price = response.doc('.unitPrice').text(),
        sell_point = response.doc('.baseattribute > .content').text()
        self.add_Mysql(title, unit_price, sell_point)
        yield {
            'title': response.doc('.main').text(),
            'unit_price':response.doc('.unitPrice').text(),
            'sell_point': response.doc('.baseattribute > .content').text()
        }