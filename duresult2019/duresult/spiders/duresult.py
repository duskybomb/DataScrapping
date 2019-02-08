import scrapy
from scrapy.selector import Selector
import os
import csv


class DuResultSpider(scrapy.Spider):
    name = "duresult"
    allowed_domains = ['duresult.in']
    if not os.path.isdir('pages'):
        os.mkdir('pages')
    PATH = 'pages/'

    start_urls = ['http://duresult.in/students/Combine_GradeCard.aspx']

    def parse(self, response):
        for roll_no in range(17312911001, 17312911045):
            self.log(response.xpath('//*[@id="imgCaptcha"]/@src').get()[33: 39])
            yield scrapy.FormRequest(
                'http://duresult.in/students/Combine_GradeCard.aspx',
                formdata={
                    'ddlcollege': '312',
                    'txtrollno': str(roll_no),
                    'txtcaptcha': response.xpath('//*[@id="imgCaptcha"]/@src').get()[33: 39],
                    'btnsearch': 'Print+Score+Card',
                    '__VIEWSTATE': response.css('input#__VIEWSTATE::attr(value)').extract_first(),
                    '__EVENTVALIDATION': response.css('input#__EVENTVALIDATION::attr(value)').extract_first(),
                    '__VIEWSTATEGENERATOR': response.css('input#__VIEWSTATEGENERATOR::attr(value)').extract_first(),
                    '__EVENTTARGET': '',	
                    '__EVENTARGUMENT': ''	
                },
                callback=self.parse_page,
                meta={'txtrollno': str(roll_no)}
            )
    def parse_page(self, response):
        self.log('here')
        with open('results_combined.csv', 'a+') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            new_list = []
            item = response.meta.get('txtrollno')
            new_list.append(item)
            new_list.append(response.xpath('//table[@id="gvrslt"]//tr[4]//td[2]/text()').get())
            new_list.append(response.xpath('//table[@id="gvrslt"]//tr[3]//td[2]/text()').get())
            new_list.append(response.xpath('//table[@id="gvrslt"]//tr[2]//td[2]/text()').get())
            wr.writerow(new_list)
