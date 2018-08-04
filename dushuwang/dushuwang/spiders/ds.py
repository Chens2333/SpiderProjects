# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from dushuwang.items import DushuwangItem


class DsSpider(CrawlSpider):
    name = 'ds'
    allowed_domains = ['www.dushu.com']
    start_urls = ['https://www.dushu.com/book/1206.html']

    # 链接提取规则。allow写正则
    rules = (
        Rule(LinkExtractor(allow=r'/book/1206_\d+\.html'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        book_list = response.xpath('//div[@class="bookslist"]/ul/li')
        for book in book_list:
            item = DushuwangItem()
            item['book_img_url'] = book.xpath('.//img/@data-original').extract_first()
            item['book_name'] = book.xpath('.//h3/a/text()').extract_first()
            item['book_author'] = book.xpath('.//p[1]/a/text()').extract_first()
            item['book_info'] = book.xpath('.//p[2]/text()').extract_first()
            yield item
