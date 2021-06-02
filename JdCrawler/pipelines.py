# -*- coding: utf-8 -*-
from pymongo import MongoClient


class MongoPipeline(object):
    def __init__(self):
        # 创建一个mongo实例
        self.client = MongoClient(host="127.0.0.1", port=27017)
        # 访问数据库
        self.db = self.client["JdGoods"]
        # 访问集合（表）
        self.col = self.db["books"]

    def process_item(self, item, spider):
        data = dict(item)
        self.col.insert(data)
        return item

    def close_spider(self, spider):
        self.client.close()
