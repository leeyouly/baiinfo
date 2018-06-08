# encoding=utf8
import scrapy
import scrapy.http
from baiinfo.table import table_to_list, table_to_list2
from baiinfo.items import BitumenProductItem
import re
import datetime
from dateutil.parser import parse
import logging
import lxml.html
import urlparse
import urllib
from scrapy.http import HtmlResponse
from scrapy.utils.project import get_project_settings
import urllib2
from scrapy.http.cookies import CookieJar
import sys

reload(sys)
sys.setdefaultencoding('utf8')

#进口沥青船期表
class BitumenImportShipSpider(scrapy.Spider):
    name = "spd_t_ec_baiinfo_bitumen_product"
    # allowed_domains = ["baiinfo.com"]
    start_urls = (
            'http://www.baiinfo.com/',
    )
    ignore_page_incremental = True

    def parse(self, response):
        self.crawler.stats.set_value('spiderlog/source_name', u'百川资讯-中国石油沥青产量')
        self.crawler.stats.set_value('spiderlog/target_tables', ['T_EC_BAIINFO_BITUMEN_product'])
        settings = get_project_settings()

        for page in range(3,4,1):
            artlistURL = 'http://www.baiinfo.com.cn/Orders/NewsList/119?pageid=' + str(page)
            request = scrapy.http.Request(url=artlistURL, callback=self.parse_articleList)
            yield request


    def parse_articleList(self, response):
        print response.url
        pagecookie = {
            'ASP.NET_SessionId':'avj0kmoq2r21b2hzmv1khxly',
            'BaiifoUser': 'LogName=kffund2017&LogPwd=1AACE8FB15051F900444FB136BCAA5C5&UserNames=%c2%a5%a0D%bf%a1+&Userrights=18&UserPrice=&UserReport=&HistoryEndTime=365&CurveEndTime=365&UserType=2&DayReadAmount=300&EndDate=2019/4/25 0:00:00&UserGuidKeys=851a0cc2-8b9c-4be2-be97-ddb5731599e6',
        }

        artListHtml = response.xpath(
            '/html/body/div[6]/div[1]/ul[2]/li')
        for artList in artListHtml:
            datadate = artList.xpath('./span/text()').extract()[0]
            artTitle = artList.xpath('./a/text()').extract()
            if artTitle == []:
                artTitle = artList.xpath('./a/font/text()').extract()
            if u'中国石油沥青产量（分所属）' in artTitle[0]:
                datamonth = re.findall(u'(.+)中国',artTitle[0])
                artUrl = response.urljoin(artList.xpath('./a/@href').extract()[0])
                request = scrapy.http.FormRequest(url=artUrl, callback=self.parse_content, cookies=pagecookie)
                request.meta['datadate'] = datadate
                request.meta['datamonth'] = datamonth[0]
                request.meta['cls_type'] = u'所属'
                yield request
            if u'中国石油沥青产量（分地区）' in artTitle[0]:
                datamonth = re.findall(u'(.+)中国', artTitle[0])
                artUrl = response.urljoin(artList.xpath('./a/@href').extract()[0])
                request = scrapy.http.FormRequest(url=artUrl, callback=self.parse_content, cookies=pagecookie)
                request.meta['datadate'] = datadate
                request.meta['datamonth'] = datamonth[0]
                request.meta['cls_type'] = u'地区'
                yield request


    def parse_content(self, response):
        # print '-------->' + response.url
        datadateStr = response.xpath('/html/body/div[6]/ul/div[1]/text()').extract()[0]
        datadateyear = str(20) + re.findall(u'20(.+)',datadateStr)[0][:2]
        datadate = datadateyear + '-' + response.meta['datadate']
        datamonth = response.meta['datamonth']
        cls_type = response.meta['cls_type']

        data_table = response.xpath('/html/body/div[6]/ul/div[3]/div/table')
        data_list = table_to_list(data_table)
        if data_list <> []:
            if len(data_list[2]) == 10:
                for data in data_list[2:-1]:
                    item = BitumenProductItem()
                    item['datadate'] = datadate
                    item['datemonth'] = datamonth
                    item['cls_type'] = cls_type
                    item['item_name'] = "".join(data[0].split())
                    item['pre_month_value'] = data[1]
                    item['curr_month_value'] = data[2]
                    item['pre_year_value'] = data[3]
                    item['yoy'] = data[4]
                    item['mom'] = data[5]
                    item['cumu_value_y'] = data[6]
                    item['pre_cumu_value_y'] = data[7]
                    item['yoy_amount'] = data[8]
                    item['cumu_yoy'] = data[9]
                    item['update_dt'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    item['source'] = response.url
                    yield item
            else:
                print '-----------> ' + response.url
        else:
            print 'data_list is null ------'