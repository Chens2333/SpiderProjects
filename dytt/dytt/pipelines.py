# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class DyttPipeline(object):
    def __init__(self):
        self.fw=open('move.json','w',encoding='utf-8')

    #处理每一个Item
    def process_item(self, item, spider):
        obj=dict(item)
        str = json.dumps(obj,ensure_ascii=False)
        self.fw.write(str+"\n")
        return item

    def close_spider(self,spider):
        self.fw.close()
