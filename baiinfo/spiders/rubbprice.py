# -*- coding: utf-8 -*-
import scrapy
import scrapy.http
from baiinfo.table import table_to_list, table_to_list2
from baiinfo.items import RubbPrice
import re
import datetime
import logging
import lxml.html
import urlparse
import urllib
from scrapy.http import HtmlResponse
from scrapy.utils.project import get_project_settings
import urllib2
from scrapy.http.cookies import CookieJar
import json


class RubbPriceSpider(scrapy.Spider):
    name = "rubbprice"
    allowed_domains = ["baiinfo.com"]
    start_urls = (
            'http://www.baiinfo.com/',
    )
    ignore_page_incremental = True

    def parse(self, response):
        self.crawler.stats.set_value('spiderlog/source_name', u'百川资讯-国内橡胶价格')
        self.crawler.stats.set_value('spiderlog/target_tables', ['T_EC_BAI_RUBB_PRICE'])
        settings = get_project_settings()
        request = scrapy.http.FormRequest(url='http://www.baiinfo.com/Account/TopPart', 
            formdata = {
                'LogName':settings.get('USERNAME_EC'),
                'password':settings.get('PASSWORD_EC'),
                'rememberMe':'false'}, 
                callback = self.login_callback)
        return [request]


    def login_callback(self, response):
        cookiejar = CookieJar()
        cookiejar.extract_cookies(response, response.request)
        self.cookiejar = cookiejar
        paths = [
            ('http://www.baiinfo.com/Orders/Price?categoryID=74&ProductID=419', u'天胶（全乳胶）市场价格',),
            ('http://www.baiinfo.com/Orders/Price?categoryID=74&ProductID=420', u'天然橡胶国际价格',),
            ('http://www.baiinfo.com/Orders/Price?categoryID=74&ProductID=421', u'天然橡胶期货收盘价',),
            ('http://www.baiinfo.com/Orders/Price?categoryID=74&ProductID=2025', u'天胶（进口乳胶）市场报价',),
            ('http://www.baiinfo.com/Orders/Price?categoryID=74&ProductID=2026', u'天胶（标准胶）市场报价',),
            ('http://www.baiinfo.com/Orders/Price?categoryID=74&ProductID=2028', u'天胶（进口胶）市场报价',),
            ('http://www.baiinfo.com/Orders/Price?categoryID=74&ProductID=2029', u'天胶（复合胶）市场报价',),
            ('http://www.baiinfo.com/Orders/Price?categoryID=74&ProductID=2030', u'天胶（轮胎专用胶）市场报价',),
            ('http://www.baiinfo.com/Orders/Price?categoryID=75&ProductID=428', u'SBS出厂价格',),
            ('http://www.baiinfo.com/Orders/Price?categoryID=77&ProductID=422', u'丁苯橡胶出厂价格',),
            ('http://www.baiinfo.com/Orders/Price?categoryID=77&ProductID=423', u'丁苯橡胶市场价格',),
            ('http://www.baiinfo.com/Orders/Price?categoryID=77&ProductID=425', u'顺丁橡胶出厂价格',),
            ('http://www.baiinfo.com/Orders/Price?categoryID=77&ProductID=426', u'顺丁橡胶市场价格',),
            ('http://www.baiinfo.com/Orders/Price?categoryID=77&ProductID=2031', u'溶聚丁苯橡胶报价',),
            ('http://www.baiinfo.com/Orders/Price?categoryID=77&ProductID=2032', u'顺丁橡胶国际价格',),
            ('http://www.baiinfo.com/Orders/Price?categoryID=77&ProductID=2033', u'丁苯橡胶国际价格',),
            ('http://www.baiinfo.com/Orders/Price?categoryID=77&ProductID=2034', u'丁苯橡胶1712报价',),
        ]
        for path in paths:
            yield scrapy.Request(url=path[0], meta={'category': path[1],}, callback=self.parse_content)


    def parse_content(self, response):
        data_table = response.xpath('//div[@id="SynPrice"]/table')
        data_list = table_to_list(data_table)
        if len(data_list) <= 1 or len(data_list[1]) < 9:
            raise Exception('BAIINFO----get table failed %s' % response.url)
        dateindex = [1, 2, 3, 4, 5, 6]
        for row in data_list[1:]:
            for index in dateindex:
                item = RubbPrice()
                item['category'] = response.meta['category']
                item['area'] = row[0].strip()
                item['price'] = row[index].strip()
                item['remark'] = row[8].strip()
                item['datadate'] = datetime.datetime.strptime(data_list[0][index].strip(), '%Y/%m/%d')
                item['update_dt'] = datetime.datetime.now()
                item['source'] = u'百川资讯国内橡胶价格'
                yield item

        # begin = datetime.datetime(2016, 4, 17).strftime('%Y-%m-%d')
        # end = datetime.datetime(2017, 4, 16).strftime('%Y-%m-%d')
        # skuid = ','.join(response.xpath('//input[@name="sku"]/@id').extract()) + ','
        # productid = re.search('ProductID=(\d+)', response.url).group(1)
        # url = 'http://www.baiinfo.com/Orders/NewHistoryGrid?begin={0}&end={1}&skuid={2}&productID={3}'.format(begin, end, skuid, productid)
        # yield scrapy.Request(url=url, meta=response.meta, callback=self.parse_history)


    def parse_history(self, response):
        datas = json.loads(u'{"data": ' + response.body_as_unicode() + u'}')['data']
        doc = lxml.html.document_fromstring(datas)
        data_table = doc.xpath('//table')[1]
        data_list = table_to_list2(data_table)
        if len(data_list) <= 1:
            raise Exception('BAIINFO HISTORY----get table failed %s' % response.url)
        for row in data_list[1:]:
            if u'平均价' in row[0]:
                continue
            for index in range(1, len(data_list[0])):
                item = RubbPrice()
                item['category'] = response.meta['category']
                item['area'] = data_list[0][index].strip()
                item['price'] = row[index].strip()
                item['datadate'] = datetime.datetime.strptime(row[0].strip(), '%Y-%m-%d')
                item['update_dt'] = datetime.datetime.now()
                item['source'] = u'百川资讯国内橡胶价格'
                yield item
            
            
    def closed(self, reason):
        logout_url = 'http://www.baiinfo.com/Account/LogOff'
        headers = { 
            'User-Agent' : self.crawler.settings.get('USER_AGENT'),
        }
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookiejar.jar))
        urllib2.install_opener(opener)
        req = urllib2.Request(url=logout_url, headers = headers, data = urllib.urlencode({}))
        response = urllib2.urlopen(req)
        logging.debug(response)
        the_page = response.read()

