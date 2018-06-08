# -*-coding:utf8 -*-
import scrapy
import scrapy.http
from baiinfo.table import table_to_list, table_to_list2
from baiinfo.items import ColourNewsItem
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


class BcdataPriceSpider(scrapy.Spider):
    name = "spd_t_cl_colour_news"
    allowed_domains = ["baiinfo.com"]
    start_urls = (
            'http://www.baiinfo.com/',
    )
    #ignore_page_incremental = True

    def parse(self, response):
        self.crawler.stats.set_value('spiderlog/source_name', u'百川资讯-新闻')
        self.crawler.stats.set_value('spiderlog/target_tables', ['null'])
        settings = get_project_settings()
        #循环page
        for li in range(1,3):
            urls = 'http://www.baiinfo.com/Orders/NewsList/3541?pageid='+str(li)
            request = scrapy.http.Request(url=urls, callback = self.url_list)
            
            yield request
    def url_list(self, response):
        Datalist = response.xpath('/html/body/div[@class="news_more"]/div[@class="news_more_left"]/ul/li/a')
        DataUrl = response.xpath('/html/body/div[@class="news_more"]/div[@class="news_more_left"]/ul/li/a/@href').extract()
        DataTitle = response.xpath('/html/body/div[@class="news_more"]/div[@class="news_more_left"]/ul/li/a//text()').extract()
        for lr in range(0,len(Datalist)):
        #for lr in range(3, 4):
            if 'baiinfo' in DataUrl[lr]:
                urls=DataUrl[lr]
                login_flg='N'
            else:
                urls = 'http://www.baiinfo.com'+DataUrl[lr]
                login_flg = 'Y'
            Data_title = DataTitle[lr]
            request = scrapy.http.Request(url=urls,meta={'login_flg':login_flg,'Data_title':Data_title}, callback=self.parse_content)
            yield request

    def parse_content(self, response):
        if response.meta['login_flg'] == 'Y':
            if '\xe5\xb9\xb4' in  response.xpath('/html/body/div[@class="news_body"]/ul/div[@class="news_tel_2"]/text()').extract()[0]:
                DataTime = response.xpath('/html/body/div[@class="news_body"]/ul/div[@class="news_tel_2"]/text()').extract()[0].replace(' ','')[-11:]
                DataTime=DataTime.decode('utf-8').replace('\xe5\xb9\xb4','-').replace('\xe6\x9c\x88','-').encode('utf-8').replace('\xe6\x97\xa5','')
            else:
                DataTime = response.xpath('/html/body/div[@class="news_body"]/ul/div[@class="news_tel_2"]/text()').extract()[
                    0].replace('  ', '')[-17:]
        else:
            DataTime = response.xpath('/html/body/div[@class="news_body"]/ul/div[@class="news_tel_2"]/text()').extract()[0][-17:]
        item = ColourNewsItem()
        item['large_variety'] = u'稀土'
        item['variety_type'] = u'铁合金'
        item['channel'] = u'行业资讯'
        item['newsid'] = '-9999'
        item['pubdate'] = DataTime
        item['title'] = response.meta['Data_title']
        item['url'] = response.url
        item['source'] = u'百川资讯'
        item['update_dt'] = datetime.datetime.now()
        yield item
