# -*- coding: utf-8 -*-
import scrapy

from dytt.items import DyttItem


class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['www.ygdy8.net']   #网址域名要统一
    start_urls = ['http://www.ygdy8.net/html/gndy/dyzz/index.html']

    def parse(self, response):
        table_list=response.xpath('//div[@class="co_content8"]/ul//table')
        print('---------------------------------')
        print(len(table_list))
        for table in table_list:
            item = DyttItem()
            item['move_name'] = table.xpath('.//a[@class="ulink"]/text()').extract_first()
            item['move_info'] = table.xpath('.//tr[last()]/td/text()').extract_first()
            move_href ="http://www.ygdy8.net"+table.xpath('.//a[@class="ulink"]/@href').extract_first()
            print(move_href,item['move_name'],item['move_info'])
            yield scrapy.Request(url=move_href,callback=self.next_page,meta={'item':item})


    def next_page(self,response):
        #获取传递过来的参数
        item =response.meta['item']
        item['img_url'] = response.xpath('//div[@id="Zoom"]//p/img[1]/@src').extract_first()
        # item['download_url'] = response.xpath('//div[@id="Zoom"]//table//a/text()').extract_first()
        item['download_url'] = response.xpath('//td[@bgcolor="#fdfddf"]/a/text()').extract_first()
        yield  item