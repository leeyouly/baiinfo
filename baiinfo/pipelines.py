# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from baiinfo.data import ImportBitumenPriceStorage, ImportBitumenFreightStorage, ImportBitumenPriceCIFStorage, \
    RubbPriceStorage, BcdataPriceStorage,ColourMetalStorage,ImportColourNewsStorage,BitumenInventoryStorage,\
    BitumenImportStorage,BitumenOpenRateStorage,BitumenProductStorage
from baiinfo.items import ImportBitumenPrice, ImportBitumenFreight, ImportBitumenPriceCIF, RubbPrice, BcdataPrice,\
    ColourMetal,ColourNewsItem,BitumenInventoryItem,BitumenImportItem,BitumenOpenRateItem,BitumenProductItem
from scrapy.utils.project import get_project_settings

class BaiinfoPipeline(object):
    def process_item(self, item, spider):
        return item


class ImportBitumenPriceSave(object):
    def __init__(self):
        self.storage = ImportBitumenPriceStorage(get_project_settings().get('DATABASE'))
    
    def process_item(self, item, spider):
        if isinstance(item, ImportBitumenPrice):
            if not self.storage.exist(item):           
                self.storage.save_or_update(item)
                spider.crawler.stats.inc_value('spiderlog/save_count')
            
        return item  
    
    
class ImportBitumenFreightSave(object):
    def __init__(self):
        self.storage = ImportBitumenFreightStorage(get_project_settings().get('DATABASE'))
    
    def process_item(self, item, spider):
        if isinstance(item, ImportBitumenFreight):
            if not self.storage.exist(item):           
                self.storage.save_or_update(item)
                spider.crawler.stats.inc_value('spiderlog/save_count')
            
        return item  
    
    
class ImportBitumenPriceCIFSave(object):
    def __init__(self):
        self.storage = ImportBitumenPriceCIFStorage(get_project_settings().get('DATABASE'))
    
    def process_item(self, item, spider):
        if isinstance(item, ImportBitumenPriceCIF):
            if not self.storage.exist(item):           
                self.storage.save_or_update(item)
                spider.crawler.stats.inc_value('spiderlog/save_count')
            
        return item


class RubbPriceSave(object):
    def __init__(self):
        self.storage = RubbPriceStorage(get_project_settings().get('DATABASE'))

    def process_item(self, item, spider):
        if isinstance(item, RubbPrice):
            self.storage.save_or_update(item)
            spider.crawler.stats.inc_value('spiderlog/save_count')

        return item


class BcdataPriceSave(object):
    def __init__(self):
        self.storage = BcdataPriceStorage(get_project_settings().get('DATABASE'))

    def process_item(self, item, spider):
        if isinstance(item, BcdataPrice):
            self.storage.save_or_update(item)
            spider.crawler.stats.inc_value('spiderlog/save_count')

        return item

class ColourMetalSave(object):
    def __init__(self):
        self.storage = ColourMetalStorage(get_project_settings().get('DATABASE'))

    def process_item(self, item, spider):
        if isinstance(item, ColourMetal):
            self.storage.save_or_update(item)
            spider.crawler.stats.inc_value('spiderlog/save_count')

        return item

class ColouNewsSave(object):
    def __init__(self):
        self.storage = ImportColourNewsStorage(get_project_settings().get('DATABASE'))

    def process_item(self, item, spider):
        if isinstance(item, ColourNewsItem):
            self.storage.save_or_update(item)
            spider.crawler.stats.inc_value('spiderlog/save_count')

        return item


class BitumenInventorySave(object):
    def __init__(self):
        self.storage = BitumenInventoryStorage(get_project_settings().get('DATABASE'))

    def process_item(self, item, spider):
        if isinstance(item, BitumenInventoryItem):
            self.storage.save_or_update(item)
            spider.crawler.stats.inc_value('spiderlog/save_count')

        return item

class BitumenImportSave(object):
    def __init__(self):
        self.storage = BitumenImportStorage(get_project_settings().get('DATABASE'))

    def process_item(self, item, spider):
        if isinstance(item, BitumenImportItem):
            self.storage.save_or_update(item)
            spider.crawler.stats.inc_value('spiderlog/save_count')

        return item


class BitumenOpenRateSave(object):
    def __init__(self):
        self.storage = BitumenOpenRateStorage(get_project_settings().get('DATABASE'))

    def process_item(self, item, spider):
        if isinstance(item, BitumenOpenRateItem):
            self.storage.save_or_update(item)
            spider.crawler.stats.inc_value('spiderlog/save_count')

        return item


class BitumenProductSave(object):
    def __init__(self):
        self.storage = BitumenProductStorage(get_project_settings().get('DATABASE'))

    def process_item(self, item, spider):
        if isinstance(item, BitumenProductItem):
            self.storage.save_or_update(item)
            spider.crawler.stats.inc_value('spiderlog/save_count')

        return item