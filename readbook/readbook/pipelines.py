# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class ReadbookPipeline(object):
    def open_spider(self,spider):
        self.f=open('book.json','w',encoding='utf-8')


    def process_item(self, item, spider):
        obj=dict(item)
        str_=json.dumps(obj,ensure_ascii=False)
        self.f.write(str_+'\n')
        return item

    def close_spider(self):
        self.f.close()
