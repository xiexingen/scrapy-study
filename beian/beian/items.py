# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BeianItem(scrapy.Item): # 备案管理index
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    # 对应备案系统数据主键Id
    _id=scrapy.Field()
    # 备案号
    recordNo=scrapy.Field()
    # 省份
    areaName=scrapy.Field()
    # 地址
    address=scrapy.Field()
    #机构名称
    compName=scrapy.Field()
    #联系人
    linkMan=scrapy.Field()
    #联系方式
    linkTel=scrapy.Field()
    #联系方式	备案状态
    linkTel=scrapy.Field()
    # 行号
    index=scrapy.Field()
    
    # 备案状态 8:已备案 9:取消备案
    recordStatus=scrapy.Field()
    # 备案状态-文本
    recordStatusText=scrapy.Field()
    # 详情页解析出来的
    # 机构级别
    orgLevel=scrapy.Field()
    # 备案时间（首次）
    recordFirstDate=scrapy.Field()
    # 备案时间(变更)
    recordChangeDate=scrapy.Field()

    # 备案专业和主要研究者信息-列表
    recordingProfessions=scrapy.Field()
    # 监督检查信息-列表
    inspectionInformations=scrapy.Field()
    # 其他机构地址
    otherAddresss=scrapy.Field()

class RecordingProfession(scrapy.Item): # 备案专业和主要研究者信息
    # 专业名称
    profession=scrapy.Field()
    # 主要研究者
    mainResearcher=scrapy.Field()
    # 职称
    jobTitle=scrapy.Field()

class InspectionInformation(scrapy.Item): # 监督检查信息
    # 检查日期
    checkDate=scrapy.Field()
    # 检查类别	
    checkType=scrapy.Field()
    # 监督检查结果	
    checkResult=scrapy.Field()
    # 处理情况
    processingSituation=scrapy.Field()