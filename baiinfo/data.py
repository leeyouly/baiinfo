from spiderlib.data import DataStorage
import PyDB


class ImportBitumenPriceStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_BM_BAI_BITUMEN_PRICE'
        self.db.set_metadata(self.table_name, [
            PyDB.DateField("datadate", is_key=True),
            PyDB.StringField("source", is_key=True),
            PyDB.StringField("area", is_key=True),
            PyDB.StringField("price1"),
            PyDB.StringField("price2"),
            PyDB.StringField("price3"),
            PyDB.StringField("price4"),
            PyDB.StringField("price5"),
            PyDB.StringField("change"),
            PyDB.StringField("shipment"),
            PyDB.StringField("unit"),
            PyDB.DateField("insert_dt"),
            PyDB.DateField("update_dt"),
        ])
    def save_or_update(self, item):
        self.db.save_or_update(self.table_name, item) 
        self.db.commit()  

class ImportBitumenFreightStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_BM_BAI_BITUMEN_FREIGHT'
        self.db.set_metadata(self.table_name, [
            PyDB.DateField("datadate", is_key=True),
            PyDB.StringField("source", is_key=True),
            PyDB.StringField("area", is_key=True),
            PyDB.StringField("price1"),
            PyDB.StringField("price2"),
            PyDB.StringField("price3"),
            PyDB.StringField("price4"),
            PyDB.StringField("price5"),
            PyDB.StringField("change"),
            PyDB.StringField("shipment"),
            PyDB.StringField("unit"),
            PyDB.DateField("insert_dt"),
            PyDB.DateField("update_dt"),
        ])
    def save_or_update(self, item):
        self.db.save_or_update(self.table_name, item) 
        self.db.commit()    

class ImportBitumenPriceCIFStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_BM_BAI_BITUMEN_PRICECIF'
        self.db.set_metadata(self.table_name, [
            PyDB.DateField("datadate", is_key=True),
            PyDB.StringField("source", is_key=True),
            PyDB.StringField("area", is_key=True),
            PyDB.StringField("price1"),
            PyDB.StringField("price2"),
            PyDB.StringField("price3"),
            PyDB.StringField("price4"),
            PyDB.StringField("price5"),
            PyDB.StringField("change"),
            PyDB.StringField("unit"),
            PyDB.DateField("insert_dt"),
            PyDB.DateField("update_dt"),
        ])
    def save_or_update(self, item):
        self.db.save_or_update(self.table_name, item) 
        self.db.commit()

class RubbPriceStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_EC_BAI_RUBB_PRICE'
        self.db.set_metadata(self.table_name, [
            PyDB.DateField("datadate", is_key=True),
            PyDB.StringField("category", is_key=True),
            PyDB.StringField("area", is_key=True),
            PyDB.StringField("price"),
            PyDB.StringField("remark"),
            PyDB.DateField("insert_dt"),
            PyDB.DateField("update_dt"),
            PyDB.StringField("source"),
        ])
    def save_or_update(self, item):
        self.db.save_or_update(self.table_name, item)
        self.db.commit()


class BcdataPriceStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_BC_DATA'
        self.db.set_metadata(self.table_name, [
            PyDB.StringField("datadate", is_key=True),
            PyDB.StringField("product_no", is_key=True),
            PyDB.StringField("industry"),
            PyDB.StringField("product"),
            PyDB.StringField("product_spec"),
            PyDB.StringField("area"),
            PyDB.StringField("price"),
            PyDB.StringField("unit"),
            PyDB.DateField("insert_dt"),
        ])
    def save_or_update(self, item):
        self.db.save_or_update(self.table_name, item)
        self.db.commit()

class ColourMetalStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 't_cl_colour_metal'
        self.db.set_metadata(self.table_name, [
            PyDB.DateField("datadate", is_key=True),
            PyDB.StringField("category", is_key=True),
            PyDB.StringField("data_type", is_key=True),
            PyDB.StringField("goods_name", is_key=True),
            PyDB.StringField("goods_code", is_key=True),
            PyDB.StringField("price"),
            PyDB.StringField("rise_offset"),
            PyDB.StringField("remark"),
			PyDB.StringField("data_title"),
            PyDB.DateField("update_dt"),
        ])
    def save_or_update(self, item):
        self.db.save_or_update(self.table_name, item)
        self.db.commit()


class ImportColourNewsStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_CL_MATE_NEWS'
        self.db.set_metadata(self.table_name, [
            PyDB.StringField("newsid"),
            PyDB.StringField("source", is_key=True),
            PyDB.DatetimeField("pubdate"),
            PyDB.StringField("large_variety"),
            PyDB.StringField("variety_type"),
            PyDB.StringField("channel"),
            PyDB.StringField("small_variety"),
            PyDB.StringField("title"),
            PyDB.StringField("url", is_key=True),
            PyDB.DatetimeField("update_dt"),
        ])

    def save_or_update(self, item):
        self.db.save_or_update(self.table_name, item)
        self.db.commit()


class BitumenInventoryStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_EC_BAIINFO_BITUMEN_INVENTORY'
        self.db.set_metadata(self.table_name, [
            PyDB.DateField("datadate", is_key=True),
            PyDB.StringField("area", is_key=True),
            PyDB.StringField("last_week_inventory"),
            PyDB.StringField("current_week_inventory"),
            PyDB.StringField("change"),
            PyDB.StringField("remark"),
            PyDB.StringField("source"),
            PyDB.DatetimeField("update_dt"),
        ])

    def save_or_update(self, item):
        self.db.save_or_update(self.table_name, item)
        self.db.commit()

class BitumenImportStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_EC_BAIINFO_BITUMEN_IMPORT'
        self.db.set_metadata(self.table_name, [
            PyDB.DateField("datadate", is_key=True),
            PyDB.StringField("ship_name", is_key=True),
            PyDB.StringField("start_port"),
            PyDB.StringField("destination_port"),
            PyDB.StringField("amount"),
            PyDB.StringField("quality"),
            PyDB.StringField("destination_date"),
            PyDB.StringField("source"),
            PyDB.DatetimeField("update_dt"),
        ])

    def save_or_update(self, item):
        self.db.save_or_update(self.table_name, item)
        self.db.commit()



class BitumenOpenRateStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_EC_BAIINFO_BITUMEN_OPENRATE'
        self.db.set_metadata(self.table_name, [
            PyDB.DateField("datadate", is_key=True),
            PyDB.StringField("area", is_key=True),
            PyDB.StringField("last_week_openrate"),
            PyDB.StringField("current_week_openrate"),
            PyDB.StringField("change"),
            PyDB.StringField("remark"),
            PyDB.StringField("source"),
            PyDB.DatetimeField("update_dt"),
        ])

    def save_or_update(self, item):
        self.db.save_or_update(self.table_name, item)
        self.db.commit()

class BitumenProductStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_EC_BAIINFO_BITUMEN_PRODUCT'
        self.db.set_metadata(self.table_name, [
            PyDB.DateField("datadate", is_key=True),
            PyDB.StringField("datemonth", is_key=True),
            PyDB.StringField("cls_type", is_key=True),
            PyDB.StringField("item_name", is_key=True),
            PyDB.StringField("pre_month_value"),
            PyDB.StringField("curr_month_value"),
            PyDB.StringField("pre_year_value"),
            PyDB.StringField("yoy"),
            PyDB.StringField("mom"),
            PyDB.StringField("cumu_value_y"),
            PyDB.StringField("pre_cumu_value_y"),
            PyDB.StringField("yoy_amount"),
            PyDB.StringField("cumu_yoy"),
            PyDB.StringField("source"),
            PyDB.DatetimeField("update_dt"),
        ])

    def save_or_update(self, item):
        self.db.save_or_update(self.table_name, item)
        self.db.commit()