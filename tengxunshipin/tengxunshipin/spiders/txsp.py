# -*- coding: utf-8 -*-
import scrapy

from tengxunshipin.items import TengxunshipinItem


class TxspSpider(scrapy.Spider):
    name = 'txsp'
    allowed_domains = ['v.qq.com']
    start_urls = ['http://v.qq.com/cartoon/']

    def parse(self, response):
        dmlist=response.xpath('//div[@class="cate_list cf"]')
        for dm in dmlist:
            dmname=dm.xpath('./a/span[2]/text()').extract()
            dmurl =dm.xpath('./a/@href').extract()
            print('-----------------------------')
            print(dmurl,dmname)
            print('-----------------------------')
            for i in range(len(dmurl)):
                yield scrapy.Request(url=dmurl[i],callback=self.dm,meta={'dmname':dmname[i]})

    def dm(self,response):
        print('a1111111111111111111111111111111111')
        item = TengxunshipinItem()
        dmname = response.meta['dmname']
        urls=response.xpath('//div[@class="mod_episode"]/span/a/@href').extract()
        name=response.xpath('//div[@class="mod_episode"]/span/a/text()').extract()
        print('------------------')
        print(urls)
        print('------------------')
        for i in range(len(urls)):
            item['url']='http://v.qq.com'+urls[i]
            item['name']=dmname+name[i].strip()
            print('---------@@@@@@@@@@---------')
            print(item['url'],item['name'])
            print('----------@@@@@@@@@@@@@@--------')
            yield item