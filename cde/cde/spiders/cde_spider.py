# -*- encoding: utf-8 -*-
"""
Topic: sample
Desc :
"""
from cde.items import CdeItem, ProjectItem, SponsorInfoItem, MainInvestigatorItem, TestDesignItem, SubjectInfoItem, HospitalItem, ECItem
import scrapy


class CDESPider(scrapy.Spider):
    name = 'cde'
    start_urls = [
        'http://www.chinadrugtrials.org.cn/eap/clinicaltrials.searchlist',
    ]

    #  def start_requests(self):
    #     yield scrapy.Request(url = 'https://www.baidu.com',method = 'POST',callback = self.parse_post)

    def parse(self, response):
        for tr in response.xpath('//table[@class="Tab"]//tr[position()>1]'):
            projectItem = ProjectItem()
            projectItem['id'] = tr.xpath('td[2]/a/@id').get()
            projectItem['registrationNo'] = tr.xpath(
                'td[2]/a/text()').get().strip()
            projectItem['studyStatus'] = tr.xpath(
                'td[3]/a/text()').get().strip()
            projectItem['drugName'] = tr.xpath('td[4]/text()').get().strip()
            projectItem['indication'] = tr.xpath(
                'td[5]/a/text()').get().strip()
            projectItem['popularTitle'] = tr.xpath(
                'td[6]/a/text()').get().strip()

            cdeItem = CdeItem()
            cdeItem['Project'] = projectItem

            print(cdeItem)
        # yield from response.follow_all(anchors, callback=self.parse)

        #     next_page = response.css('li.next a::attr(href)').get()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)
        # yield response.follow(href, callback=self.parse)
            yield cdeItem

    def parse_post(self, response):
        pass
