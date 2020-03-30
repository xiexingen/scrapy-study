# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst,MapCompose
from w3lib.html import remove_tags
import re

def str_strip(str):
    """
    定义一个函数去重字符中空格及换行
    :param str:
    :return:
    """
    return re.sub(re.compile('[\n\t\r]'), '', str)

def add_title(val):
    """
    定义一个添加标题的函数
    :param val:
    :return:
    """
    return "标题:{0}".format(val)

def format_json(val):
    result = [val]
    return result

class DemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field(input_process=MapCompose(add_title))    # 标题
    link = scrapy.Field()     # 链接
    desc = scrapy.Field()     # 简述
    posttime = scrapy.Field() # 发布时间
    pass


class DemoItemLoader(ItemLoader):
    # 设置默认的输出取第一个值
    default_output_processor=TakeFirst()

