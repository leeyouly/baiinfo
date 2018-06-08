# encoding=utf8
import scrapy
import scrapy.http
from baiinfo.table import table_to_list, table_to_list2
from baiinfo.items import BcdataPrice
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
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class BcdataPriceSpider(scrapy.Spider):
    name = "bcdataprice"
    allowed_domains = ["baiinfo.com"]
    start_urls = (
            'http://www.baiinfo.com/',
    )
    ignore_page_incremental = True

    def parse(self, response):
        self.crawler.stats.set_value('spiderlog/source_name', u'百川资讯-价格')
        self.crawler.stats.set_value('spiderlog/target_tables', ['T_BC_DATA'])
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
            ('http://www.baiinfo.com/Orders/Price?categoryID=215&ProductID=1269', u'纸浆','spider1269',),
            ('http://www.baiinfo.com/Orders/Price?categoryID=215&ProductID=1311', u'美废','spider1311',),
            ('http://www.baiinfo.com/Orders/Price?categoryID=215&ProductID=1965', u'进口浆', 'spider1965',),
            ('http://www.baiinfo.com/Orders/Price?categoryID=297&ProductID=1684', u'瓦楞纸企业价格', 'spider1684',),
            ('http://www.baiinfo.com/Orders/Price?categoryID=298&ProductID=1686', u'双胶纸企业价格', 'spider1686',),
            ('http://www.baiinfo.com/Orders/Price?categoryID=297&ProductID=1683', u'白卡纸企业价格', 'spider1683',),
        ]
        for path in paths:
            yield scrapy.Request(url=path[0], meta={'category': path[1],'productid':path[2],}, callback=self.parse_content)


    def parse_content(self, response):
        head_table = response.xpath('//div[@id="divResult"]/div/table')
        head_list = table_to_list(head_table)
        head = head_list[0][1]
        index1 = head.find('：')
        index2 = head.find('：',index1+1)
        index3 = head.find('：', index2+1)
        product = head[head.find('：')+1:head.find('\n')].strip()
        area = head[head.find('：',index2)+1:head.find('\n',index2)].strip()
        unit = head[head.find('：',index3)+1:head.find('\n',index3)].strip()
        #data_table = response.xpath('//div[@id="SynPrice"]/table')
        #data_list = table_to_list(data_table)
        if len(head_list) <= 3 or len(head_list[2]) < 9:
            raise Exception('BAIINFO----get table failed %s' % response.url)
        dateindex = [1, 2, 3, 4, 5, 6]
        for i,row in enumerate(head_list[2:]):
            for index in dateindex:
                item = BcdataPrice()
                item['industry'] = u'纸品产业'
                item['product'] = product
                item['product_spec'] = row[0].strip()
                item['product_no'] = response.meta['productid'] + str(i + 1)
                item['area'] = area
                item['price'] = row[index].strip()
                item['unit'] = unit
                item['datadate'] = datetime.datetime.strptime(head_list[1][index].strip(), '%Y/%m/%d').strftime('%Y-%m-%d')
                item['insert_dt'] = datetime.datetime.now()
                yield item

        # begin = datetime.datetime(2016, 4, 17).strftime('%Y-%m-%d')
        # end = datetime.datetime(2017, 4, 16).strftime('%Y-%m-%d')
        # skuid = ','.join(response.xpath('//input[@name="sku"]/@id').extract()) + ','
        # productid = re.search('ProductID=(\d+)', response.url).group(1)
        # url = 'http://www.baiinfo.com/Orders/NewHistoryGrid?begin={0}&end={1}&skuid={2}&productID={3}'.format(begin, end, skuid, productid)
        # yield scrapy.Request(url=url, meta=response.meta, callback=self.parse_history)

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
'''
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
'''

