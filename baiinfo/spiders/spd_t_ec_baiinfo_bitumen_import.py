# encoding=utf8
import scrapy
import scrapy.http
from baiinfo.table import table_to_list, table_to_list2
from baiinfo.items import BitumenImportItem
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
    name = "spd_t_ec_baiinfo_bitumen_import"
    # allowed_domains = ["baiinfo.com"]
    start_urls = (
            'http://www.baiinfo.com/',
    )
    ignore_page_incremental = True

    def parse(self, response):
        self.crawler.stats.set_value('spiderlog/source_name', u'百川资讯-进口沥青船期表')
        self.crawler.stats.set_value('spiderlog/target_tables', ['T_EC_BAIINFO_BITUMEN_IMPORT'])
        settings = get_project_settings()

        data = {
            'LogName': settings.get('USERNAME_EC'),
            'password': settings.get('PASSWORD_EC'),
            'rememberMe': 'false'}

        url = 'http://www.baiinfo.com.cn/Account/TopPart'
        request = scrapy.http.FormRequest(url, callback=self.login_callback, formdata=data, )
        yield request

    def login_callback(self,response):
        cookiejar = CookieJar()
        cookiejar.extract_cookies(response, response.request)
        self.cookiejar = cookiejar

        for page in range(2,3,1):
            artlistURL = 'http://www.baiinfo.com.cn/Orders/NewsList/109?pageid=' + str(page)
            request = scrapy.http.Request(url=artlistURL, callback=self.parse_articleList)
            yield request


    def parse_articleList(self, response):

        artListHtml = response.xpath(
            '/html/body/div[6]/div[1]/ul[2]/li')
        for artList in artListHtml:
            datadate = artList.xpath('./span/text()').extract()[0]
            artTitle = artList.xpath('./a/text()').extract()
            if artTitle == []:
                artTitle = artList.xpath('./a/font/text()').extract()
            if u'进口沥青船期' in artTitle[0]:
                artUrl = response.urljoin(artList.xpath('./a/@href').extract()[0])
                request = scrapy.http.Request(url=artUrl, callback=self.parse_content,)
                request.meta['datadate'] = datadate
                yield request

    def parse_content(self, response):
        # print '-------->' + response.url
        datadateStr = response.xpath('/html/body/div[6]/ul/div[1]/text()').extract()[0]
        datadateyear = str(20) + re.findall(u'20(.+)',datadateStr)[0][:2]
        datadate = datadateyear + '-' + response.meta['datadate']

        data_table = response.xpath('/html/body/div[6]/ul/div[3]/div/table')
        data_list = table_to_list(data_table)

        for data in data_list[1:-1]:
            item = BitumenImportItem()
            item['datadate'] = datadate
            item['ship_name'] = data[0]
            item['start_port'] = data[1]
            item['destination_port'] = data[2]
            item['amount'] = data[3]
            item['quality'] = data[4]
            item['destination_date'] = data[5]
            item['update_dt'] = datetime.datetime.now().strftime( '%Y-%m-%d %H:%M:%S')
            item['source'] = response.url
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