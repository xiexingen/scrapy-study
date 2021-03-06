# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

class JsonFilePipeLine(object):
    # def __init__(self):
    #     #self.file = open('novel.json', 'wb')
    #     pass
    # def open_spider(self, item):  # 蜘蛛打开的时执行
    #     pass
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False)
        file=open('data/{0}.json'.format(item['_id']), 'wb')
        file.write(line.encode('utf-8'))
        return item

    # def from_crawler(cls, crawler):  # 可访问核心组件比如配置和信号，并注册钩子函数到Scrapy中
    #     pass

    # def close_spider(self, spider):  # 蜘蛛关闭时执行
    #     pass

# class CdeMongoPipeline(object):
#     collection_name = 'scrapy_items'

#     def __init__(self, mongo_uri, mongo_db):
#         self.mongo_uri = mongo_uri
#         self.mongo_db = mongo_db

#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             mongo_uri=crawler.settings.get('MONGO_URI'),
#             mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
#         )

#     def open_spider(self, spider):
#         self.client = pymongo.MongoClient(self.mongo_uri)
#         self.db = self.client[self.mongo_db]

#     def close_spider(self, spider):
#         self.client.close()

#     def process_item(self, item, spider):
#         self.db[self.collection_name].insert(dict(item))
#         return item
