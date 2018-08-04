# -*- coding: utf-8 -*-
import scrapy

from douban.items import DoubanItem


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['movie.douban.com']
    page =0
    url='https://movie.douban.com/top250'
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        table_list = response.xpath('//div[@class="article"]//div[@class="item"]')  #电影item
        print(len(table_list))
        for table in table_list:
            item = DoubanItem()
            name= table.xpath('.//div[@class="hd"]/a/span/text()').extract()
            item['movie_name']=''
            for n in name:
                item['movie_name']+=n.strip()
            item['img_url'] = table.xpath('./div[@class="pic"]//img/@src').extract_first()
            item['movie_pl'] = table.xpath('.//div[@class="star"]/span[4]/text()').extract_first()
            movie_url = table.xpath('./div[@class="pic"]//a/@href').extract_first()
            print(movie_url, item['img_url'], item['movie_name'], item['movie_pl'])
            print('------------------------------------')
            yield scrapy.Request(url=movie_url, callback=self.next_page, meta={'item': item})

    def next_page(self, response):
        # 获取传递过来的参数
        item = response.meta['item']
        item['movie_IMDb'] = response.xpath('//div[@id="info"]//a[@rel="nofollow"]/@href').extract_first()
        item['movie_info'] = response.xpath(
            '//div[@id="link-report"]//span[@property="v:summary"]/text()').extract_first().strip()
        item['movie_actor'] = ''
        movie_actors = response.xpath('//div[@id="info"]//span[@class="attrs"]')
        for movie_acter in movie_actors:
            actor = movie_acter.xpath('.//a/text()').extract()
            for i in actor:
                item['movie_actor'] = item['movie_actor'] + i + '/'
        yield item

        self.page += 1
        if self.page <= 9:
            url = self.url+ '?start='+str(self.page*25)+'&filter='
            yield scrapy.Request(url=url, callback=self.parse)

