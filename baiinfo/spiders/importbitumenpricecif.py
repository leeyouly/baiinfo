# -*- coding: utf-8 -*-
import scrapy
import scrapy.http
from baiinfo.table import table_to_list
from baiinfo.items import ImportBitumenPriceCIF
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


class ImportBitumenPriceCIFSpider(scrapy.Spider):
    name = "importbitumenpricecif"
    allowed_domains = ["baiinfo.com"]
    start_urls = (
            'http://www.baiinfo.com/',
    )
    
    def parse(self, response):
        self.crawler.stats.set_value('spiderlog/source_name', u'百川资讯-散装进口沥青到岸价')
        self.crawler.stats.set_value('spiderlog/target_tables', ['T_BM_BAI_BITUMEN_PRICECIF'])

        settings = get_project_settings()
        request = scrapy.http.FormRequest(url='http://www.baiinfo.com/Account/TopPart', 
            formdata = {
                'LogName':settings.get('USERNAME'),
                'password':settings.get('PASSWORD'),
                'rememberMe':'false'}, 
                callback = self.login_callback)
  
        return [request]


    def login_callback(self, response):
        cookiejar = CookieJar()
        cookiejar.extract_cookies(response, response.request)
        self.cookiejar = cookiejar
        
        request = scrapy.http.Request(url='http://www.baiinfo.com/Search/Index?wd=%E6%95%A3%E8%A3%85%E8%BF%9B%E5%8F%A3%E6%B2%A5%E9%9D%92%E5%88%B0%E5%B2%B8%E4%BB%B7', 
            callback = self.parse_index)
        return [request]
        

    def parse_index(self, response):
        for link in response.xpath('//div[@class="news_more_left"]//li'):
            link_url = link.xpath('./a/@href').extract_first()
            if link_url.strip():
                link_url = urlparse.urljoin('http://www.baiinfo.com/', link_url)
                print link_url
                yield scrapy.http.Request(url = link_url,
                                          callback=self.parse_content)
            

    def parse_content(self, response):
        data_table = response.xpath('//div[@class="news_tex"]//table')
        title = response.xpath('//div[@class="news_tel"]/text()').extract_first().strip()
        title2 = response.xpath('//div[@class="news_tel_2"]/text()').extract_first().strip()
        datestr = ''.join(re.search('(\d{4}).(\d{2}).(\d{2}).', title2).groups())
        datadate = datetime.datetime.strptime(datestr, '%Y%m%d').date()
        
        logging.debug(title)
        data_list = table_to_list(data_table)
        
        if len(data_list) <= 1 or len(data_list[1]) < 7:
            raise Exception('BAIINFO----get table failed %s' % response.url)
        
        unit = re.search('\((.*)\)', data_list[0][0]).group(1).strip()
        
        for row in data_list[1:]:
            item = ImportBitumenPriceCIF()
            item['area'] = row[0].strip()
            item['price1'] = row[1].strip()
            item['price2'] = row[2].strip()
            item['price3'] = row[3].strip()
            item['price4'] = row[4].strip()
            item['price5'] = row[5].strip()
            item['change'] = row[6].strip()
            item['unit'] = unit
            item['datadate'] = datadate
            item['update_dt'] = datetime.datetime.now()
            item['source'] = title
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