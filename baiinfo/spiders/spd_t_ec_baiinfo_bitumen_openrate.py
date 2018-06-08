# encoding=utf8
import scrapy
import scrapy.http
from baiinfo.table import table_to_list, table_to_list2
from baiinfo.items import BitumenOpenRateItem
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


class BitumenOpenRateSpider(scrapy.Spider):
    name = "spd_t_ec_baiinfo_bitumen_openrate"
    # allowed_domains = ["baiinfo.com"]
    start_urls = (
            'http://www.baiinfo.com/',
    )
    ignore_page_incremental = True

    def parse(self, response):
        self.crawler.stats.set_value('spiderlog/source_name', u'百川资讯-开工率')
        self.crawler.stats.set_value('spiderlog/target_tables', ['T_EC_BAIINFO_BITUMEN_OPENRATE'])
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

        for page in range(2,4,1):
            artlistURL = 'http://www.baiinfo.com.cn/Orders/NewsList/104?pageid=' + str(page)
            request = scrapy.http.Request(url=artlistURL, callback=self.parse_articleList)
            yield request


    def parse_articleList(self, response):
        print response.url

        artListHtml = response.xpath(
            '/html/body/div[6]/div[1]/ul[2]/li')
        for artList in artListHtml:
            datadate = artList.xpath('./span/text()').extract()[0]
            artTitle = artList.xpath('./a/font/text()').extract()[0]
            if u'开工率' in artTitle:
                artUrl = response.urljoin(artList.xpath('./a/@href').extract()[0])
                request = scrapy.http.FormRequest(url=artUrl, callback=self.parse_content,)
                request.meta['datadate'] = datadate
                yield request

    def parse_content(self, response):
        # print '-------->' + response.url
        datadateStr = response.xpath('/html/body/div[6]/ul/div[1]/text()').extract()[0]
        datadateyear = str(20) + re.findall(u'20(.+)',datadateStr)[0][:2]
        datadate = datadateyear + '-' + response.meta['datadate']

        data_table = response.xpath('/html/body/div[6]/ul/div[3]/div/table')
        data_list = table_to_list(data_table)
        if data_list == []:
            print 'data_list is null-----> ' + response.url

        for data in data_list[1:]:
            item = BitumenOpenRateItem()
            item['datadate'] = datadate
            item['area'] = data[0]
            item['last_week_openrate'] = data[1]
            item['current_week_openrate'] = data[2]
            item['change'] = data[3]
            item['remark'] = data[4]
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