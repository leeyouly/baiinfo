# -*- coding: utf-8 -*-
import unittest
from scrapy.http import HtmlResponse
from baiinfo.spiders.importbitumenfreight import ImportBitumenFreightSpider
import os
import logging

class GlobalmarketNaphthaSpiderTest(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.target = ImportBitumenFreightSpider()
        
    def test_parse(self):
        dir = os.path.dirname(os.path.realpath(__file__))
        data_file_path = os.path.join(dir, 'pages/bitumenfreight.html')
        f = open(unicode(data_file_path, "utf8"))
        html_content = f.read()
        f.close()
        page_url = 'http://www.baiinfo.com/Orders/News//12848228'
        response = HtmlResponse(url=page_url, body=html_content)
        items = self.target.parse_content(response)
        
        items = list(items)
        self.assertEqual(len(items), 4)
        
        self.assertEqual(items[0]['area'],u'韩国—华南')
        self.assertEqual(items[0]['price1'],u'55.0-60.0')
        self.assertEqual(items[0]['price2'],u'55.0-60.0')
        self.assertEqual(items[0]['price3'],u'55.0-60.0')
        self.assertEqual(items[0]['price4'],u'55.0-60.0')
        self.assertEqual(items[0]['price5'],u'55.0-60.0')
        self.assertEqual(items[0]['change'],u'0')
        self.assertEqual(items[0]['unit'],u'美元/吨')
        self.assertEqual(items[0]['datadate'],datetime.datetime.strptime('20161018', '%Y%m%d').date())
        self.assertEqual(items[0]['source'],u'10月18日进口沥青船运费价格')
        
        self.assertEqual(items[3]['area'],u'新加坡—华东')
        self.assertEqual(items[3]['price1'],u'70.0-80.0')
        self.assertEqual(items[3]['price2'],u'70.0-80.0')
        self.assertEqual(items[3]['price3'],u'70.0-80.0')
        self.assertEqual(items[3]['price4'],u'70.0-80.0')
        self.assertEqual(items[3]['price5'],u'70.0-80.0')
        self.assertEqual(items[3]['change'],u'0')
        self.assertEqual(items[3]['unit'],u'美元/吨')
        self.assertEqual(items[3]['datadate'],datetime.datetime.strptime('20161018', '%Y%m%d').date())
        self.assertEqual(items[3]['source'],u'10月18日进口沥青船运费价格')

        