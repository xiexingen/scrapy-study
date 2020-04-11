# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

# 从arr列表中查找属性值prop为value的对象，并获取getProp属性的值
def FindFirstValue(arr,prop,value,getProp):
    searchValue=''
    for ele in arr:
        if(ele[prop]==value and len(ele[getProp])>0):
            searchValue=ele[getProp]
            break
    return searchValue

# 纠正里面的错误数据
class CorrectPipe(object):
     def process_item(self, item, spider):
        certifications=spider.certifications
        # 纠正主要研究者姓名是医院名称的
        for ele in item['MainInvestigators']:
            if ele["name"] in certifications:
                ele["name"]=''

        # 纠正机构姓名是机构名称的错误数据
        for ele in item['Hospitals']:
            if ele["mainSponsorName"] in certifications:
                ele["mainSponsorName"]=''

        # 如果主要研究者姓名是空，就去机构信息中找第一条对应的非空人名
        for ele in item['MainInvestigators']:
            if(len(ele["name"])==0):
                ele["name"]=FindFirstValue(item['Hospitals'],'name',ele["companyName"],'mainSponsorName')

        return item

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
