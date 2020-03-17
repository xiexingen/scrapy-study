import scrapy

class HuxiuItem(scrapy.Item):
    title=scrapy.Field() # 标题
    link=scrapy.Field() # 连接
    desc = scrapy.Field()     # 简述
    posttime = scrapy.Field() # 发布时间