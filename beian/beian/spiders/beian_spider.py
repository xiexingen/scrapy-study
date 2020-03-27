#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
Topic: sample
Desc :
"""
from beian.items import BeianItem, InspectionInformation, RecordingProfession
import scrapy
import json
import datetime
import time
import math


class BeianSpider(scrapy.Spider):
    name = 'beian'
    # allowed_domains = ["cfdi.org.cn"]
    pageSize = 10
    # start_urls = [
    #     'http://beian.cfdi.org.cn:9000/CTMDS/pub/PUB010100.do?method=handle06?pageSize=10'
    # ]

    def start_requests(self):
        indexUrl = "http://beian.cfdi.org.cn:9000/CTMDS/pub/PUB010100.do?method=handle06&_dt={timespan}".format(
            timespan=datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        form_data = {'pageSize': str(self.pageSize), 'curPage': '1'}
        yield scrapy.FormRequest(indexUrl, callback=self.parse, method='POST',formdata=form_data)
        # yield scrapy.Request(indexUrl, callback=self.parse, method='POST', body=json.dumps(formData), headers={'Content-Type': 'application/json','Accept':'application/json'})

    def parse(self, response):
        repJson=json.loads(response.text)
        if repJson.get('success')!=True:
            raise  RuntimeError("请求地址{address}失败!".format(address=response.url))
        # 请求其他页码的数据
        total =int(repJson['totalRows'])
        totalPages =math.ceil(total/self.pageSize)
        for page in range(1, total):
            indexUrl = "http://beian.cfdi.org.cn:9000/CTMDS/pub/PUB010100.do?method=handle06&_dt={timespan}".format(
            timespan=datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
            form_data = {'pageSize': str(self.pageSize), 'curPage': str(page)}
            yield scrapy.FormRequest(indexUrl, callback=self.parse_list, method='POST',formdata=form_data)

    def parse_list(self,response):
        repJson=json.loads(response.text)
        if repJson.get('success')!=True:
            raise  RuntimeError("请求地址{address}失败!".format(address=response.url))
        for item in repJson['data']:
            result = BeianItem()

            result['recordNo'] = item['recordNo']
            result['areaName'] = item['areaName']
            result['address'] = item['address']
            result['compName'] = item['compName']
            result['linkMan'] = item['linkMan']
            result['linkTel'] = item['linkTel']
            result['index'] = item['ROW2']
            result['companyId'] = item['companyId']
            result['recordStatus'] = item['recordStatus']
            if item['recordStatus'] == '8':
                result['recordStatusText'] = '已备案'
            elif item['recordStatus'] == '9':
                result['recordStatusText'] = '取消备案'
            else:
                result['recordStatusText'] = item['recordStatus']
            
            # 请求详情页
            detailUrl = "http://beian.cfdi.org.cn:9000/CTMDS/pub/PUB010100.do?method=handle07&compId={compId}&_={timespan}".format(
            compId=result['companyId'], timespan=datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
            yield scrapy.Request(detailUrl, callback=self.parse_detail,meta={'index':result})

    def parse_detail(self, response):
        result = response.meta['index']
        # 机构基本信息
        mainContainer=response.xpath('//*[@id="tabContent1"]')
        result['orgLevel']=mainContainer.xpath('div/div[3]/div/text()').get().strip()
        result['recordFirstDate']=mainContainer.xpath('div/div[7]/div/text()').get().strip()
        result['recordChangeDate']=mainContainer.xpath('div/div[8]/div/text()').get().strip()

        # 备案专业和主要研究者信息 
        result['recordingProfessions']=[]
        for tr in response.xpath('//*[@id="tabContent2"]//tbody/tr'):
            recordingProfession=RecordingProfession()
            recordingProfession['profession']=tr.xpath('td[1]/text()').get().strip()
            recordingProfession['mainResearcher']=tr.xpath('td[2]/text()').get().strip()
            recordingProfession['jobTitle']=tr.xpath('td[3]/text()').get().strip()
            result['recordingProfessions'].append(recordingProfession)

        # 监督检查信息
        result['inspectionInformations']=[]
        for tr in response.xpath('//*[@id="tabContent3"]//tbody/tr'):
            inspectionInformation=InspectionInformation()
            inspectionInformation['checkDate']=tr.xpath('td[1]/text()').get().strip()
            inspectionInformation['checkType']=tr.xpath('td[2]/text()').get().strip()
            inspectionInformation['checkResult']=tr.xpath('td[3]/text()').get().strip()
            inspectionInformation['processingSituation']=tr.xpath('td[4]/text()').get().strip()
            result['inspectionInformations'].append(inspectionInformation)

        yield result