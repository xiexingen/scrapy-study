# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import logging
import pymongo
from bson.objectid import ObjectId


class BeianMongoDBPipeline(object):
    collection_name = 'beian'

    def __init__(self, mongo_uri, mongo_db,crawler):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        # pull in information from settings.py
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
            crawler=crawler
        )

    def open_spider(self, spider):
        # initializing spider
        # opening db connection
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        # how to handle each post
        newItem = dict(item.copy())
        
        #_id = ObjectId(newItem['_id'])
        _id = newItem['_id']

        oldItem = self.db[self.collection_name].find_one({"_id": _id})
        # update
        if (oldItem is not None):
            if(oldItem['recordChangeDate']!=newItem['recordChangeDate']):
                newItem['needupdate'] = True
            else:
                newItem['needupdate']=False
            self.db[self.collection_name].update_one({
                "_id": _id
            }, {
                "$set": dict(newItem)
            })
        else:  # create
            newItem['needupdate'] = True
            self.db[self.collection_name].insert(newItem)
        
        # # 如果需要更新 则调用api
        # if(newItem['needupdate']):
        #     req = scrapy.Request('http://www.baidu.com',self.parse_update, meta={'item':item})
        #     self.crawler.engine.crawl(req, spider)

        return item

    def close_spider(self, spider):
        # clean up when spider is closed
        self.client.close()

    # def parse_update(self,spider):
    #     pass