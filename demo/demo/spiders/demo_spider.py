# -*- encoding: utf-8 -*-
"""
Topic: sample
Desc :
"""
from demo.items import DemoItem
import scrapy
import datetime
import time
import codecs

from scrapy.loader import ItemLoader


class QuotesSpider(scrapy.Spider):
    name = 'demo'
    start_urls = [
        'http://www.chinadrugtrials.org.cn/eap/clinicaltrials.searchlist',
    ]

    def parse(self, response):
        for tr in response.xpath('//table[@class="Tab"]//tr[position()>1]'):
            itemRow = {
                'demo': tr.xpath('td[1000]/a/@id').get().strip(),
                'ss': tr.xpath('td[2]/a/@id').extract_first(default='').strip(),
                'id': tr.xpath('td[2]/a/@id').extract_first(),
                'registryNo': tr.xpath('td[2]/a/text()').re_first(r'\w+'),
                'status':tr.xpath('td[3]/a/text()'),
                'drugName':tr.xpath('td[4]/text()'),
                'shutZ':tr.xpath('td[5]/text()'),
                'title':tr.xpath('td[6]/text()'),
            }
            print(itemRow)

            l=ItemLoader(item=DemoItem(),response=response)
            l.add_xpath('name','')
            l.add_css('ff','')
            return l.load_item();
        #yield from response.follow_all(anchors, callback=self.parse)

        #     next_page = response.css('li.next a::attr(href)').get()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)
        # yield response.follow(href, callback=self.parse)
            yield itemRow

    def process_exception(self, request, exception, spider):
        self._faillog(request, u'EXCEPTION', exception, spider)
        return request

    def _faillog(self, request, errorType, reason, spider):
        with codecs.open('log/faillog.log', 'a', encoding='utf-8') as file:
            file.write("%(now)s [%(error)s] %(url)s reason: %(reason)s \r\n" %
                       {'now':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'error': errorType,
                        'url': request.url,
                        'reason': reason})