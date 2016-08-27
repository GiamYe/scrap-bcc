# -*- coding: utf-8 -*-
from scrapy.spider import Spider
from scrapy import FormRequest
import urllib

class BccSpider(Spider):
    name = 'bcc'
    allowed_domains = ['bcc.blcu.edu.cn/']

    def _get_search_keys(self):
        return ['万分病病歪歪', '较稀少', '较苍老']

    def start_requests(self):
        keys = self._get_search_keys()
        return [FormRequest('http://bcc.blcu.edu.cn/zh/search/0/{0}'.format(urllib.quote(k)), dont_filter=True) for k in keys]

    def parse(self, response):
        #keys = BccSpider._get_search_keys()
        texts = response.xpath('//tbody/tr/td/text()').extract()
        filename = 'result.txt'
        texts = [t.encode('utf-8') for t in texts if '\n' not in t]
        merged_texts = []
        key = urllib.unquote(response.url.split('/')[-1])
        for i in xrange(0, len(texts)):
            index = i % 2
            if index == 0:
                merged_texts.append(texts[i]+texts[i+1]+'\n')
        with open(filename, 'a') as f:
            f.write(key+'\t'+str(len(set(merged_texts)))+'\n')


