# -*- coding: utf-8 -*-
from scrapy.spider import Spider, Request
from scrapy import FormRequest
import urllib

class BccSpider(Spider):
    name = 'bcc'
    allowed_domains = ['bcc.blcu.edu.cn']
    count = 0
    def _get_search_keys(self):
        keys = []
        advs = []
        adjs = []
        adv_file_path = '/data/adv.txt'
        adj_file_path = '/data/adj.txt'
        adv_file = open(adv_file_path)
        adj_file = open(adj_file_path)
        while 1:
            adv_key = adv_file.readline()
            if not adv_key:
                break
            adv_key = adv_key.replace(' ', '').replace('\n', '')
            advs.append(adv_key)
        while 1:
            adj_key = adj_file.readline()
            if not adj_key:
                break
            adj_key = adj_key.replace(' ', '').replace('\n', '')
            adjs.append(adj_key)
        for v in advs:
            for j in adjs:
                keys.append(v+j)
        adj_file.close()
        adv_file.close()
        print 'keys:', keys
        return keys

    def start_requests(self):
        keys = self._get_search_keys()
        #reqs = [FormRequest('http://bcc.blcu.edu.cn/zh/search/0/{0}'.format(urllib.quote(k)), dont_filter=True) for k in keys]

        return [FormRequest('http://bcc.blcu.edu.cn/zh/search/0/{0}'.format(urllib.quote(k)), dont_filter=True) for k in keys]

    def parse(self, response):
        #keys = BccSpider._get_search_keys()
        texts = response.xpath('//tbody/tr/td/text()').extract()

        filename = '/data/result.txt'
        texts = [t.encode('utf-8') for t in texts if '\n' not in t]
        merged_texts = []
        key = urllib.unquote(response.url.split('/')[-1])
        for i in xrange(0, len(texts)):
            index = i % 2
            if index == 0:
                merged_texts.append(texts[i]+texts[i+1]+'\n')
        #print 'lines num:', len(merged_texts)
        legacy_file_path = '/data/legacy.txt'
        if len(merged_texts) == 100:
            with open(legacy_file_path, 'wb') as legacy_file:
                legacy_file.write(key)
            return
        with open(filename, 'a') as f:
            f.write(key+'\t'+str(len(set(merged_texts)))+'\n')




