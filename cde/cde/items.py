# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

# Cde项目信息


class CdeItem(scrapy.Item):  # Cde 实体
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 项目主体信息
    Project = scrapy.Field()
    # 项目申办方信息
    SponsorInfo = scrapy.Field()
    # 主要研究者信息(组长单位)
    MainInvestigators = scrapy.Field()
    # 临床试验信息  2、试验设计（单选）
    TestDesign = scrapy.Field()
    # 受试者信息
    SubjectInfo = scrapy.Field()
    # 存储医院信息
    SrcHospitals = scrapy.Field()
    # 伦理数据
    SrcECs = scrapy.Field()


class ProjectItem(scrapy.Item):  # 项目主信息
    # id
    id = scrapy.Field()
   # 登记号
    registrationNo = scrapy.Field()
    # 适应症
    indication = scrapy.Field()
   # 试验方案编号
    protocolNO = scrapy.Field()
    # 临床申请受理号
    acceptNo = scrapy.Field()
    # 试验通俗题目
    popularTitle = scrapy.Field()
    # 试验专业题目
    studyTitle = scrapy.Field()
    # 药物名称
    drugName = scrapy.Field()
    # 药物类型
    drugClassification = scrapy.Field()
    # 试验状态
    studyStatus = scrapy.Field()
    # 试验相关信息
    otherInfo = scrapy.Field(serializer=str)
    # 来源说明
    sourceComment = scrapy.Field()
    # 来源链接
    sourceLink = scrapy.Field()
    # 首次公示信息日期
    firstPublishDate = scrapy.Field()
    # 首例入组日期
    firstSubjectEncroEnrollmentDate = scrapy.Field()
    # 试验终止日期
    testStopDate = scrapy.Field()
    # 申办者联系人
    sponsorConcatName = scrapy.Field()


class SponsorInfoItem(scrapy.Item):  # 申办方信息
    # 申办方名称
    sponsorNames = scrapy.Field()
    # 联系人姓名
    concatName = scrapy.Field()
    # 联系电话
    tel = scrapy.Field()
    # Email
    email = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 邮编
    zipCode = scrapy.Field()
    # 费用来源
    costFrom = scrapy.Field()


class MainInvestigatorItem(scrapy.Item):  # 主要研究者信息
     # 姓名 #去除人名中的杂质 如:(叶定伟，医学博士)
    name = scrapy.Field()
    # 职称
    jobTitle = scrapy.Field()
    # 电话
    tel = scrapy.Field()
    # Email
    email = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 邮编
    zipCode = scrapy.Field()
    # 单位名称
    companyName = scrapy.Field()
    # 获取专业认证 从姓名中解析 如:(叶定伟，医学博士)
    certification = scrapy.Field()


class TestDesignItem(scrapy.Item):  # 试验设计信息
     # 试验分类
    testType = scrapy.Field()
    # 试验分期
    testStaging = scrapy.Field()
    # 设计类型
    designType = scrapy.Field()
    # 随机化
    randomization = scrapy.Field()
    # 盲法
    blind = scrapy.Field()
    # 试验范围
    testRange = scrapy.Field()


class SubjectInfoItem(scrapy.Item):  # 临床试验信息 受试者信息
    # 年龄
    age = scrapy.Field()
    # 性别
    geneder = scrapy.Field()

    # 健康受试者
    healthSubject = scrapy.Field()
    # 目标入组人数
    targetEnrollment = scrapy.Field()
    # 实际入组人数
    actualEnrollment = scrapy.Field()
    # 数据安全监察委员会
    dMC = scrapy.Field()
    # 为受试者购买试验伤害保险
    testInjuryInsurance = scrapy.Field()
    # 第一例受试者入组日期
    firstJoinDate = scrapy.Field()
    # 试验终止日期
    abortDate = scrapy.Field()
    # 试验状态
    testStatus = scrapy.Field()


class HospitalItem(scrapy.Item):  # 医院信息
   # 机构名称
    name = scrapy.Field()
    # 国家
    state = scrapy.Field()
    # 所在省
    province = scrapy.Field()
    # 所在市
    city = scrapy.Field()
    # 办公地址
    address = scrapy.Field()
    # 电话
    telephone = scrapy.Field()
    # 邮箱
    email = scrapy.Field()
    # 主要研究者
    mainSponsorName = scrapy.Field()


class ECItem(scrapy.Item):  # 伦理委员会信息
    # 名称
    name = scrapy.Field()
    # 审查结论
    approveResult = scrapy.Field()
    # 审查日期
    approveDate = scrapy.Field()
