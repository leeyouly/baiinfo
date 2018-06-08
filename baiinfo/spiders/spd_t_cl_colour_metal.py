# encoding=utf8
import scrapy
import scrapy.http
from baiinfo.table import table_to_list, table_to_list2
from baiinfo.items import ColourMetal
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
    name = "spd_t_cl_colour_metal"
    allowed_domains = ["baiinfo.com"]
    start_urls = (
            'http://www.baiinfo.com/',
    )
    ignore_page_incremental = True

    def parse(self, response):
        self.crawler.stats.set_value('spiderlog/source_name', u'百川资讯-有色价格数据')
        self.crawler.stats.set_value('spiderlog/target_tables', ['t_cl_colour_metal'])
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
            ['http://www.baiinfo.com/youse/tong', u'有色金属']
            #('http://www.baiinfo.com/tiehejin/tiehejin', u'铁合金')
        ]
        for path in paths:
            yield scrapy.Request(url=path[0], meta={'productid':path[1],'urls':path[0]}, callback=self.index_url)

    def index_url(self, response):
        product = response.meta['productid']
        #index_list=[]
        # index_list.append(response.meta['urls'].replace('http://www.baiinfo.com',''))
        # for i in response.xpath('/html/body/div/div[@class="shiyoumtop_nav_new"]/div[@class="top_nav_new"]//ul/li/a/@href').extract():
        #     index_list.append(i)
        # print index_list
        #index_list = response.xpath('/html/body/div/div[@class="shiyoumtop_nav_new"]/div[@class="top_nav_new"]//ul/li/a/@href').extract()
        # index_name = response.xpath('/html/body/div/div[@class="shiyoumtop_nav_new"]/div[@class="top_nav_new"]//ul/li/a/text()').extract()
        index_list = ['http://www.baiinfo.com/youse/li','http://www.baiinfo.com/lidian/zjcl','http://www.baiinfo.com/lidian/fjcl','http://www.baiinfo.com/lidian/djygm','http://www.baiinfo.com/tiehejin/xitu']
        index_name = ['锂','正极材料','负极材料','电解液隔膜','稀土']
        print product
        #print 'http://www.baiinfo.com'+index_list[0]
        for c_row in range(0, len(index_list)):
            yield scrapy.Request(url=index_list[c_row], meta={'productid': product, 'category': index_name[c_row]}, callback=self.url_list)

    def url_list(self, response):
        #data_cate = response.xpath('/html/body/div/div[@class="liqing_body"]/div[3]')
        #data_catw_list = table_to_list(data_cate)
        product = response.meta['productid']
        category = response.meta['category']
        goods_url = response.xpath('/html/body/div/div[@class="liqing_body"]/div[3]/div[1]/ul/li/a/@href').extract()
        goods_name = response.xpath('/html/body/div/div[@class="liqing_body"]/div[3]/div[1]/ul/li/a/text()').extract()
        print goods_url
        for g_row in range(0,len(goods_url)):
            yield scrapy.Request(url='http://www.baiinfo.com' + goods_url[g_row],meta={'productid': product, 'category': category, 'goods_name': goods_name[g_row]}, callback=self.parse_content)


    def parse_content(self, response):
        data_table=response.xpath('//*[@id="ctl00_theBody_grdPriceList"]')
        data_list = table_to_list(data_table)
        print data_list
        for tr_row in range(1,len(data_list)):
            for rows in range(1,len(data_list[0])-2):
                item = ColourMetal()
                data_type = response.meta['productid']
                category =  response.meta['category']
                goods_name = response.meta['goods_name']
                price = data_list[tr_row][rows]
                goods_code = data_list[tr_row][0]
                datadate = data_list[0][rows].replace("/","-")
                rise_offset = data_list[tr_row][7]
                remark = data_list[tr_row][8]
                item['data_type'] = data_type
                item['category'] = category
                item['goods_name'] = goods_name
                item['goods_code'] = goods_code
                item['price'] = price
                item['datadate'] = datadate
                item['rise_offset'] = rise_offset
                item['remark'] = remark
                item['data_title'] = u'百川资讯有色价格数据'
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
