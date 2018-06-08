# -*- coding: utf-8 -*-

# Scrapy settings for baiinfo project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'baiinfo'

SPIDER_MODULES = ['baiinfo.spiders']
NEWSPIDER_MODULE = 'baiinfo.spiders'
DUPEFILTER_CLASS = 'baiinfo.dupefilters.ChemDupeFilter'

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
DOWNLOAD_DELAY=3
SPIDER_MIDDLEWARES = {
   # 'spiderlib.middlewares.IndexPageSaveMiddleware': 300,
}
EXTENSIONS = {
   'spiderlib.extensions.WriteEtlLog': 300,
}
ITEM_PIPELINES = {
   'baiinfo.pipelines.ImportBitumenPriceSave': 300,
   'baiinfo.pipelines.ImportBitumenFreightSave': 300,
   'baiinfo.pipelines.ImportBitumenPriceCIFSave': 300,
   'baiinfo.pipelines.RubbPriceSave': 300,
   'baiinfo.pipelines.BcdataPriceSave': 300,
   'baiinfo.pipelines.ColourMetalSave': 300,
   'baiinfo.pipelines.ColouNewsSave': 300,
   'baiinfo.pipelines.BitumenInventorySave': 300,
   'baiinfo.pipelines.BitumenImportSave': 300,
   'baiinfo.pipelines.BitumenOpenRateSave': 300,
   'baiinfo.pipelines.BitumenProductSave': 300,

}
LOG_LEVEL = 'INFO'

USERNAME = '3363208'
PASSWORD = '3363208'

USERNAME_EC = 'kffund2017'
# PASSWORD_EC = 'kf168168'
PASSWORD_EC = 'kffund2018'
#USERNAME_EC = 'kftz123'
#PASSWORD_EC = '000000'

# DATABASE = 'oracle://stg:devstg123@10.10.50.17:1534/?service_name=db'
DATABASE = 'oracle://stg:stg123@10.6.0.94:1521/?service_name=db'