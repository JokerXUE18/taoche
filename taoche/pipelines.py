# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


# class TaochePipeline(object):
#     def process_item(self, item, spider):
#         # print(item)
#         return item


class MongoPipeline(object):
    def __init__(self):
        # 计数
        self.count = 1
        # 连接mongo客户端
        self.client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        # 选择连接的数据库
        self.db = self.client['taoche']

    def process_item(self, item, spider):
        print(self.count, dict(item))
        self.count += 1
        # 插入数据库
        self.db.cars.insert(dict(item))

        return item


