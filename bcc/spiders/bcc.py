# -*- coding: utf-8 -*-
from scrapy.spider import Spider, Request
from scrapy import FormRequest
import urllib
import os

class BccSpider(Spider):
    name = 'bcc'
    allowed_domains = ['bcc.blcu.edu.cn']
    count = 0
    def _get_search_keys(self):
        keys = []
        advs = []
        adjs = []
        adv_file_path = os.getenv('ADV_PATH')
        adj_file_path = os.getenv('ADJ_PATH')
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
        # print 'keys:', keys
        return keys

    def start_requests(self):
        keys = self._get_search_keys()
        for k in keys:
            yield Request(url='http://bcc.blcu.edu.cn/zh/search/0/{0}'.format(urllib.quote(k)),
                          meta={
                              'dont_filter': True,
                              'dont_merge_cookies': True
                          }
                              # 'dont_redirect': True,
                              # 'handle_httpstatus_list': [302]}
                          )
        #return [FormRequest('http://bcc.blcu.edu.cn/zh/search/0/{0}'.format(urllib.quote(k)), dont_filter=True, ) for k in keys]

    def parse_detail(self, response):
        reference = response.xpath('//body/div[@class="modal-body"]/b/text()').extract()
        key = response.xpath('//body/div[@class="modal-body"]/strong/text()').extract()
        texts = response.xpath('//body/div[@class="modal-body"]/text()').extract()
        detail_file = os.getenv('DETAIL_PATH')
        with open(detail_file, 'a') as f:
            rf = 'Reference: '+reference[0].encode('utf-8')+'\n'
            if len(texts)==3:
                pre_part = texts[1].encode('utf-8')
                after_part = texts[2].encode('utf-8')
                f.write(rf+pre_part+key[0].encode('utf-8')+after_part+'\n')

    def parse(self, response):
        original_key = response.url.split('/')[-1]
        key = urllib.unquote(original_key.split('?')[0])
        texts = response.xpath('//tbody/tr/td/text()').extract()
        filename = os.getenv('RESULT_PATH')
        texts = [t.encode('utf-8') for t in texts if '\n' not in t]
        merged_texts = []
        for i in xrange(0, len(texts)):
            index = i % 2
            if index == 0:
                merged_texts.append(texts[i]+texts[i+1]+'\n')
        # print 'lines num:', len(merged_texts)
        # not_200_path = os.getenv('NOT_200')
        # if response.status != 200:
        #     with open(key+'\t'+str(len(set(merged_texts)))+'\n')
        legacy_file_path = os.getenv('LEGACY_PATH')
        if len(merged_texts) == 100:
            with open(legacy_file_path, 'a') as legacy_file:
                legacy_file.write(key+'\n')
        with open(filename, 'a') as f:
            f.write(key+'\t'+str(len(set(merged_texts)))+'\n')
        if len(merged_texts)>0:
            detail_urls = response.xpath('//tbody/tr/td/a/@href').extract()
            for d in detail_urls:
                print "detail url is %s \n" % d
                yield Request(url='http://bcc.blcu.edu.cn{0}'.format(d),
                              meta={
                              'dont_filter': True,
                              'dont_merge_cookies': True
                          },
                              callback=self.parse_detail)




