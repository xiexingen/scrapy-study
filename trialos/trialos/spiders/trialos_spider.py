# -*- encoding: utf-8 -*-
"""
Topic: sample
Desc :
"""
from trialos.items import TrialosItem
import scrapy 
from scrapy import Selector
from w3lib.html import remove_comments
import math
import json
import re


class TrialosPider(scrapy.Spider):
    name = 'trialos'
    pageSize = 1
    allowed_domains = ["trialos.com"]
  
    def start_requests(self):
        indexUrl = "http://www.chinadrugtrials.org.cn/eap/clinicaltrials.searchlist"
        form_data = {'pagesize': str(self.pageSize), 'currentpage': '1'}
        yield scrapy.FormRequest(indexUrl, callback=self.parse, method='POST',formdata=form_data)

    def parse_detail(self, response):
        try:
            html=Selector(text=remove_comments(response.text))
            
            yield cdeItem
        except Exception as e:
            self.logger.error('解析出错:%s?%s',response.url,response.request.body)
            self.logger.error(e)


        
    def log_error_back(self, failure):
         # 日志记录所有的异常信息
        self.logger.error(repr(failure))
        request = failure.request
        self.logger.error('error on %s', request.url)

