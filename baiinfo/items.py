# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaiinfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ImportBitumenPrice(scrapy.Item):
    area = scrapy.Field()
    price1 = scrapy.Field()
    price2 = scrapy.Field()
    price3 = scrapy.Field()
    price4 = scrapy.Field()
    price5 = scrapy.Field()
    change = scrapy.Field()
    shipment = scrapy.Field()
    unit = scrapy.Field()
    datadate = scrapy.Field()
    insert_dt = scrapy.Field()
    update_dt = scrapy.Field()
    source = scrapy.Field()


class ImportBitumenFreight(scrapy.Item):
    area = scrapy.Field()
    price1 = scrapy.Field()
    price2 = scrapy.Field()
    price3 = scrapy.Field()
    price4 = scrapy.Field()
    price5 = scrapy.Field()
    change = scrapy.Field()
    unit = scrapy.Field()
    datadate = scrapy.Field()
    insert_dt = scrapy.Field()
    update_dt = scrapy.Field()
    source = scrapy.Field()


class ImportBitumenPriceCIF(scrapy.Item):
    area = scrapy.Field()
    price1 = scrapy.Field()
    price2 = scrapy.Field()
    price3 = scrapy.Field()
    price4 = scrapy.Field()
    price5 = scrapy.Field()
    change = scrapy.Field()
    unit = scrapy.Field()
    datadate = scrapy.Field()
    insert_dt = scrapy.Field()
    update_dt = scrapy.Field()
    source = scrapy.Field()


class RubbPrice(scrapy.Item):
    category = scrapy.Field()
    area = scrapy.Field()
    price = scrapy.Field()
    remark = scrapy.Field()
    datadate = scrapy.Field()
    insert_dt = scrapy.Field()
    update_dt = scrapy.Field()
    source = scrapy.Field()


class BcdataPrice(scrapy.Item):
    industry = scrapy.Field()
    product = scrapy.Field()
    product_spec = scrapy.Field()
    product_no = scrapy.Field()
    area = scrapy.Field()
    price = scrapy.Field()
    unit = scrapy.Field()
    datadate = scrapy.Field()
    insert_dt = scrapy.Field()


class ColourMetal(scrapy.Item):
    datadate = scrapy.Field()
    category = scrapy.Field()
    data_type = scrapy.Field()
    goods_name = scrapy.Field()
    goods_code = scrapy.Field()
    price = scrapy.Field()
    rise_offset = scrapy.Field()
    remark = scrapy.Field()
    data_title = scrapy.Field()
    update_dt = scrapy.Field()


class ColourNewsItem(scrapy.Item):
    newsid = scrapy.Field()
    source = scrapy.Field()
    pubdate = scrapy.Field()
    large_variety = scrapy.Field()
    variety_type = scrapy.Field()
    channel = scrapy.Field()
    small_variety = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    update_dt = scrapy.Field()


class BitumenInventoryItem(scrapy.Item):
    datadate = scrapy.Field()
    area = scrapy.Field()
    last_week_inventory = scrapy.Field()
    current_week_inventory = scrapy.Field()
    change = scrapy.Field()
    remark = scrapy.Field()
    update_dt = scrapy.Field()
    source = scrapy.Field()


class BitumenImportItem(scrapy.Item):
    datadate = scrapy.Field()
    ship_name = scrapy.Field()
    start_port = scrapy.Field()
    destination_port = scrapy.Field()
    amount = scrapy.Field()
    quality = scrapy.Field()
    destination_date = scrapy.Field()
    update_dt = scrapy.Field()
    source = scrapy.Field()


class BitumenOpenRateItem(scrapy.Item):
    datadate = scrapy.Field()
    area = scrapy.Field()
    last_week_openrate = scrapy.Field()
    current_week_openrate = scrapy.Field()
    change = scrapy.Field()
    remark = scrapy.Field()
    update_dt = scrapy.Field()
    source = scrapy.Field()


class BitumenProductItem(scrapy.Item):
    datadate = scrapy.Field()
    datemonth = scrapy.Field()
    cls_type = scrapy.Field()
    item_name = scrapy.Field()
    pre_month_value = scrapy.Field()
    curr_month_value = scrapy.Field()
    pre_year_value = scrapy.Field()
    yoy = scrapy.Field()
    mom = scrapy.Field()
    cumu_value_y = scrapy.Field()
    pre_cumu_value_y = scrapy.Field()
    yoy_amount = scrapy.Field()
    cumu_yoy = scrapy.Field()
    update_dt = scrapy.Field()
    source = scrapy.Field()
