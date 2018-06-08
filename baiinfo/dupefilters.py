from scrapy.dupefilters import RFPDupeFilter
import random

class ChemDupeFilter(RFPDupeFilter):
    def request_fingerprint(self, request):
        if request.url.startswith('http://www.baiinfo.com/youse/tong'):
            dummy_request = request.copy()
            dummy_request = dummy_request.replace(url = dummy_request.url + '&rdm=' + str(random.random()))
            return super(ChemDupeFilter, self).request_fingerprint(dummy_request)
        if request.url.startswith('http://www.baiinfo.com/tiehejin/tiehejin'):
            dummy_request = request.copy()
            dummy_request = dummy_request.replace(url = dummy_request.url + '&rdm=' + str(random.random()))
            return super(ChemDupeFilter, self).request_fingerprint(dummy_request)
        return super(ChemDupeFilter, self).request_fingerprint(request)
