# -*- encoding: utf-8 -*-
"""
Topic: sample
Desc :
"""
from cde.items import CdeItem, ProjectItem, SponsorInfoItem, MainInvestigatorItem, ClinicalTrialInformationItem, HospitalItem, ECItem
import scrapy 
from scrapy import Selector
from w3lib.html import remove_comments
import math
import json
import re
import os
import sys

def getAllcertification():
    result=[]
    with open(os.path.abspath('cde/assets/certification.txt'),'rt',encoding="UTF-8") as f:
        for line in f:
            result.append(line.strip('\n'))
    return result

class CDESPider(scrapy.Spider):
    name = 'cde'
    pageSize = 10
    allowed_domains = ["chinadrugtrials.org.cn"]
    certifications=getAllcertification()
    # start_urls = [
    #     'http://www.chinadrugtrials.org.cn/eap/clinicaltrials.searchlist',
    # ]

    def start_requests(self):
        indexUrl = "http://www.chinadrugtrials.org.cn/eap/clinicaltrials.searchlist"
        form_data = {'pagesize': str(self.pageSize), 'currentpage': '1'}
        yield scrapy.FormRequest(indexUrl, callback=self.parse, method='POST',formdata=form_data)

        # # 单条
        # detailUrl="http://www.chinadrugtrials.org.cn/eap/clinicaltrials.searchlistdetail"
        # CTR20191251
        # form_data = {'ckm_index':'1','pagesize': str(self.pageSize),'currentpage':'1','rule':'CTR','sort2':'desc','sort':'desc','keywords':'CTR20130174'}
        # yield scrapy.FormRequest(detailUrl, callback=self.parse_detail, method='POST',formdata=form_data)

    def parse(self, response):
        totalPages=int(response.xpath('//*[@id="searchfrm"]/div/div[3]/div[1]/a[1]/text()').extract_first().strip())
        #totalPages =math.ceil(total/self.pageSize)
        # indexUrl = "http://www.chinadrugtrials.org.cn/eap/clinicaltrials.searchlist"
        detailUrl="http://www.chinadrugtrials.org.cn/eap/clinicaltrials.searchlistdetail"
        for page in range(1,totalPages):       
            form_data = {'ckm_index': str(page),'pagesize': str(self.pageSize),'currentpage':'1','rule':'CTR','sort2':'desc','sort':'desc'}
            yield scrapy.FormRequest(detailUrl, callback=self.parse_detail, method='POST',formdata=form_data)

    # def parse_list(self,response):
    #     for tr in response.css('.apply_zhgl>table').xpath('.//tr[position()>1]'):
    #         projectItem = ProjectItem()
    #         projectItem['registrationId'] = tr.xpath('td[2]/a/@id').extract_first()
    #         projectItem['registrationNo'] = tr.xpath('td[2]/a/text()').extract_first(default='').strip()
    #         projectItem['studyStatus'] = tr.xpath('td[3]/a/text()').extract_first(default='').strip()
    #         projectItem['drugName'] = tr.xpath('td[4]/a/text()').extract_first(default='').strip()
    #         projectItem['indication'] = tr.xpath('td[5]/a/text()').extract_first(default='').strip()
    #         projectItem['popularTitle'] = tr.xpath('td[6]/a/text()').extract_first(default='').strip()
    #         id_name= tr.xpath('td[2]/a/@name').extract_first(default='').strip()
    #         # 请求详情页
    #         detailUrl = "http://www.chinadrugtrials.org.cn/eap/clinicaltrials.searchlistdetail"
    #         form_data = {'ckm_id':projectItem['registrationId'],'ckm_index':id_name,'reg_no':'CTR'}
    #         yield scrapy.FormRequest(detailUrl, callback=self.parse_detail, method='POST',formdata=form_data,meta={'projectItem':projectItem})

    def parse_detail(self, response):
        try:
            html=Selector(text=remove_comments(response.text))
            cdeItem=CdeItem()

            cdeContainer=html.xpath('//*[@id="div_open_close_01"]')

            projectItem= ProjectItem()

            projectMainContainer=html.css('.register_mainB>.apply_zhgl>.cxtj_tm')
            cdeItem['_id']=projectMainContainer.xpath('table//tr[1]/td[2]/text()').extract_first(default='').strip()
            # 登记号
            projectItem['registrationNo']=cdeItem['_id']
            # 试验状态
            projectItem['studyStatus']=projectMainContainer.xpath('table//tr[1]/td[4]/text()').extract_first(default='').strip()
            # 申办者联系人
            projectItem['sponsorConcatName']=projectMainContainer.xpath('table//tr[2]/td[2]/text()').extract_first(default='').strip()
            # 首次公示信息日期
            projectItem['firstPublishDate']=projectMainContainer.xpath('table//tr[2]/td[4]/text()').extract_first(default='').strip()
        
            # 适应症
            projectItem['indication']=cdeContainer.xpath('table//tr[2]/td[2]/text()').extract_first(default='').strip()
            # 试验通俗题目
            projectItem['popularTitle']=cdeContainer.xpath('table//tr[3]/td[2]/text()').extract_first(default='').strip()
            # 试验专业题目
            projectItem['studyTitle']=cdeContainer.xpath('table//tr[4]/td[2]/text()').extract_first(default='').strip()
            # 试验方案编号
            projectItem['protocolNo']=cdeContainer.xpath('table//tr[5]/td[2]/text()').extract_first(default='').strip()
            #临床申请受理号 -- 化学药备案号
            projectItem['acceptNo']=cdeContainer.xpath('table//tr[6]/td[2]/text()').extract_first(default='').strip()
            # 药物名称
            projectItem['drugName']=cdeContainer.xpath('table//tr[7]/td[2]/text()').extract_first(default='').strip()
            # 药物类型
            projectItem['drugClassification']=cdeContainer.xpath('table//tr[8]/td[2]/text()').extract_first(default='').strip()
            # 试验相关信息
            projectItem['otherInfo']='<div>{}</div>'.format(html.css('.register_main>.register_mainB>.apply_zhgl').xpath('./table').extract_first())
            # 首例入组日期
            # projectItem['firstSubjectEncroEnrollmentDate']=cdeContainer.xpath('.//table[4]//tr/td/text()').extract_first(default='').strip()
            projectItem['firstSubjectEncroEnrollmentDate']=cdeContainer.xpath(".//div[@class='STYLE2'][contains(., '第一例受试者入组日期')]/following-sibling::table[1]//td/text()").extract_first(default='').strip()
            # 试验终止日期
            # projectItem['testStopDate']=cdeContainer.xpath('.//table[5]//tr/td/text()').extract_first(default='').strip()
            projectItem['testStopDate']=cdeContainer.xpath(".//div[@class='STYLE2'][contains(., '试验终止日期')]/following-sibling::table[1]//td/text()").extract_first(default='').strip()
            #八、试验状态
            #projectItem['studyStatus2']=cdeContainer.xpath('.//table[8]//tr/td').extract_first(default='').strip()      
            projectItem['studyStatus2']=re.sub(r"\s+", "",cdeContainer.xpath(".//div[@class='STYLE2'][contains(., '试验状态')]/following-sibling::table[1]//td/text()").extract_first(default='').strip())

            cdeItem['Project']=dict(projectItem)

            ## 申办方信息
            sponsorInfoItem=SponsorInfoItem()
            sponsorContainer=cdeContainer.xpath('./table[2]')
            #申办方名称
            sponsorInfoItem['sponsorNames']=[]
            for tr in sponsorContainer.xpath('.//tr[1]/td[2]/table/tr'):
                sponsorInfoItem['sponsorNames'].append(tr.xpath('td[2]/text()').extract_first(default='').strip('/'))
            #联系人姓名
            sponsorInfoItem['concatName']=sponsorContainer.xpath('tr[2]/td[2]/text()').extract_first(default='').strip()
            #联系电话
            sponsorInfoItem['tel']=sponsorContainer.xpath('tr[3]/td[2]/text()').extract_first(default='').strip()
            #Email
            sponsorInfoItem['email']=sponsorContainer.xpath('tr[3]/td[4]/text()').extract_first(default='').strip()
            #地址
            sponsorInfoItem['address']=sponsorContainer.xpath('tr[4]/td[2]/text()').extract_first(default='').strip()
            #邮编
            sponsorInfoItem['zipCode']=sponsorContainer.xpath('tr[4]/td[4]/text()').extract_first(default='').strip()
            #费用来源
            # sponsorInfoItem['costFrom']=sponsorContainer.xpath('.//tr[5]/td[2]/text()').extract_first(default='').strip()
            sponsorInfoItem['costFrom']= ''.join([item.strip() for item in sponsorContainer.xpath('tr[5]/td[2]/text()').extract()])

            cdeItem['SponsorInfo']=dict(sponsorInfoItem)

            ## 试验设计信息
            clinicalTrialInfomation=ClinicalTrialInformationItem()
            clinicalTrialContainer=cdeContainer.xpath('./table[3]')
            #试验目的
            clinicalTrialInfomation['testPurpose']=re.sub(r"\s+", "", clinicalTrialContainer.xpath('tr[2]/td/text()').extract_first(default='').strip())
            #试验分类
            clinicalTrialInfomation['testType']=clinicalTrialContainer.xpath('tr[4]/td/table//tr[1]/td[3]/text()').extract_first(default='').strip()
            #试验分期
            clinicalTrialInfomation['testStaging']=clinicalTrialContainer.xpath('tr[4]/td/table//tr[2]/td[3]/text()').extract_first(default='').strip()
            #设计类型
            clinicalTrialInfomation['testDesignType']=clinicalTrialContainer.xpath('tr[4]/td/table//tr[3]/td[3]/text()').extract_first(default='').strip()
            #随机化
            clinicalTrialInfomation['testRandomization']=clinicalTrialContainer.xpath('tr[4]/td/table//tr[4]/td[3]/text()').extract_first(default='').strip()
            #盲法
            clinicalTrialInfomation['testBlind']=clinicalTrialContainer.xpath('tr[4]/td/table//tr[5]/td[3]/text()').extract_first(default='').strip()
            #试验范围
            clinicalTrialInfomation['testRange']=clinicalTrialContainer.xpath('tr[4]/td/table//tr[6]/td[3]/text()').extract_first(default='').strip()
            ##  3、受试者信息
            #年龄 -- 去掉内容中的\t\n\r
            clinicalTrialInfomation['subjectAge']=re.sub(r"\s+", "", clinicalTrialContainer.xpath('tr[6]/td[2]/text()').extract_first(default='').strip())
            #性别
            clinicalTrialInfomation['subjectGeneder']=clinicalTrialContainer.xpath('tr[7]/td[2]/text()').extract_first(default='').strip()
            #健康受试者
            clinicalTrialInfomation['subjectHealth']=clinicalTrialContainer.xpath('tr[8]/td[2]/text()').extract_first(default='').strip()
            # 目标入组人数
            clinicalTrialInfomation['subjectTargetEnrollment']=re.sub(r"\s+", "", clinicalTrialContainer.xpath('tr[11]/td[2]/text()').extract_first(default='').strip())
            # 实际入组人数
            clinicalTrialInfomation['subjectActualEnrollment']=clinicalTrialContainer.xpath('tr[12]/td[2]/text()').extract_first(default='').strip()
            # 数据安全监察委员会
            clinicalTrialInfomation['subjectDMC']=clinicalTrialContainer.xpath('tr[19]/td/text()').re_first(r'([有|无])')
            # 为受试者购买试验伤害保险
            clinicalTrialInfomation['subjectInjuryInsurance']=clinicalTrialContainer.xpath('tr[20]/td/text()').re_first(r'([有|无])')

            cdeItem['ClinicalTrialInformation']=dict(clinicalTrialInfomation)

            ## 主要研究者信息
            cdeItem['MainInvestigators']=[]
            for table in cdeContainer.xpath('table[6]//tr[2]/td/table'):
                mainInvestigator=MainInvestigatorItem()
                # 姓名 #去除人名中的杂质 如:(叶定伟，医学博士)
                tempNames=self.matchNameAndTitle(table.xpath('.//td[contains(.,"姓名")]//following-sibling::td[1]/text()'))
                mainInvestigator['name'] =tempNames[0] if len(tempNames)>0 else ''
                # 获取专业认证 从姓名中解析 如:(叶定伟，医学博士)
                mainInvestigator['certification'] = tempNames[1] if len(tempNames)>1 else ''
                # 职称
                mainInvestigator['jobTitle'] =table.xpath('.//td[contains(.,"职称")]//following-sibling::td[1]/text()').extract_first(default='').strip()
                # 电话
                mainInvestigator['tel'] =table.xpath('.//td[contains(.,"电话")]//following-sibling::td[1]/text()').extract_first(default='').strip()
                # Email
                mainInvestigator['email'] =table.xpath('.//td[contains(.,"Email")]//following-sibling::td[1]/text()').extract_first(default='').strip()
                # 地址
                mainInvestigator['address'] =table.xpath('.//td[contains(.,"邮政地址")]//following-sibling::td[1]/text()').extract_first(default='').strip()
                # 邮编
                mainInvestigator['zipCode'] = table.xpath('.//td[contains(.,"邮编")]//following-sibling::td[1]/text()').extract_first(default='').strip()
                # 单位名称
                mainInvestigator['companyName'] =table.xpath('.//td[contains(.,"单位名称")]//following-sibling::td[1]/text()').extract_first(default='').strip()
                
                if self.is_all_empty(mainInvestigator) is False :
                    cdeItem['MainInvestigators'].append(dict(mainInvestigator))
                    

            ## 各参加机构信息
            cdeItem['Hospitals']=[]
            for tr in cdeContainer.xpath('//*[@id="hspTable"]//tr[position()>1]'):
                hospital=HospitalItem()
                # 序号
                hospital['no']=tr.xpath('td[1]/text()').extract_first(default='').strip()
                # 机构名称                
                hospital['name'] = tr.xpath('td[2]/text()').extract_first(default='').strip()
                # 主要研究者(不要职称，只保留研究者姓名)
                tempNames=self.matchMultipleName(tr.xpath('td[3]/text()'))
                hospital['mainSponsorName'] = tempNames[0] if len(tempNames)>0 else ''
                # 国家
                hospital['state'] = tr.xpath('td[4]/text()').extract_first(default='').strip()
                # 所在省
                hospital['province'] = tr.xpath('td[5]/text()').extract_first(default='').strip()
                # 所在市
                hospital['city'] = tr.xpath('td[6]/text()').extract_first(default='').strip()
                
                if len(tempNames)>1:
                    for item in tempNames:
                        newHospital=hospital.copy()
                        newHospital['mainSponsorName']=item
                        cdeItem['Hospitals'].append(dict(newHospital))
                else:
                    cdeItem['Hospitals'].append(dict(hospital))


            ## 伦理委员会信息
            cdeItem['ECs']=[]
            for tr in cdeContainer.xpath('//*[@id="div_open_close_01"]/table[7]//tr[position()>1]'):
                ec=ECItem()
                # 下标
                ec['no'] =tr.xpath('td[1]/text()').extract_first(default='').strip()
                # 名称
                ec['name'] =tr.xpath('td[2]/text()').extract_first(default='').strip()
                # 审查结论
                ec['approveResult'] = tr.xpath('td[3]/text()').extract_first(default='').strip()
                # 审查日期
                ec['approveDate'] = tr.xpath('td[4]/text()').extract_first(default='').strip()
                
                if self.is_all_empty(ec) is False :
                    cdeItem['ECs'].append(dict(ec))
                
        
            yield cdeItem
        except Exception as e:
            self.logger.error('解析出错:%s?%s',response.url,response.request.body)
            self.logger.error(e)


    def is_all_empty(self,item):
        allEmpty=True
        for key in item.fields:
            if len(item.get(key))>0:
                allEmpty=False
                break
        return allEmpty

    # 匹配姓名以及所获证书职称 张三,博士
    def matchNameAndTitle(self,selector):
        content=selector.extract_first(default='').strip()
        # 处理两个字姓名的中间带空格的问题 张 三
        content=re.sub(r'^([\u4e00-\u9fa5])\s+([\u4e00-\u9fa5])$', r'\1\2',content)
        matchs=re.findall('([\u4e00-\u9fa5]+)',content)
        # matchs=selector.re('([\u4e00-\u9fa5]+)')
        if len(matchs)==0:
            #matchs=re.split('[,;，；、]',selector.extract_first(default='').strip())
            matchs=[selector.extract_first(default='').strip()]
        return matchs

    # 匹配单个或者多个姓名 张三,医学博士/张三，李四 只保留姓名
    def matchMultipleName(self,selector):
        content=selector.extract_first(default='').strip()
        # 处理两个字姓名的中间带空格的问题 张 三
        content=re.sub(r'^([\u4e00-\u9fa5])\s+([\u4e00-\u9fa5])$', r'\1\2',content)
        matchs=re.findall('([\u4e00-\u9fa5]+)',content)
        if len(matchs)==0:
            #matchs=re.split('[,;，；、]',selector.extract_first(default='').strip())
            matchs=[selector.extract_first(default='').strip()]
        for ele in matchs:
            if ele in self.certifications:
                matchs.remove(ele)
        return matchs
    
    def log_error_back(self, failure):
         # 日志记录所有的异常信息
        self.logger.error(repr(failure))
        request = failure.request
        self.logger.error('error on %s', request.url)

