# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
from itemadapter import ItemAdapter


class JdcrawlerPipeline:
    def __init__(self):
        # self.f = open("detail.json", "w")
        self.con = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', charset='utf8')
        self.cor = self.con.cursor()
        self.cor.execute("CREATE DATABASE if not EXISTS myspider")
        self.cor.execute("USE myspider")
        self.cor.execute("CREATE TABLE if not EXISTS jd (id INT PRIMARY KEY AUTO_INCREMENT, name varchar (200), "
                         "title varchar (200), url varchar (200), shop varchar (200), price varchar (50), "
                         "searchword varchar (50));")

    def process_item(self, item, spider):
        # content = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        # self.f.write(content)
        try:
            name = item['name']
            title = item['title']
            url = item['url']
            shop = item['shop']
            price = item['price']
            searchword = item['searchword']
            sql = "INSERT INTO jd (name, title, url, shop, price, searchword) VALUES ('" + name + "','" + title + "','" \
                  + url + "','" + shop + "','" + price + "','" + searchword + "')"
            self.cor.execute(sql)
            self.con.commit()
        except Exception as e:
            print(e)
        return item

    def close_spider(self, spider):
        # self.f.close()
        self.con.close()
