# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DyttItem(scrapy.Item):
    # define the fields for your item here like:
    #电影名称
    move_name = scrapy.Field()
    #电影简介
    move_info = scrapy.Field()
    #电影海报
    img_url = scrapy.Field()
    #下载地址
    download_url = scrapy.Field()
