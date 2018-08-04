# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class TengxunshipinPipeline(object):
    def __init__(self):
        self.fw=open('dm2.json','w',encoding='utf-8')

    #处理每一个Item
    def process_item(self, item, spider):
        obj=dict(item)
        str = json.dumps(obj,ensure_ascii=False)
        self.fw.write(str+"\n")
        return item

    def close_spider(self,spider):
        self.fw.close()

from scrapy.utils.project import get_project_settings

import pymysql


# 添加如下新的管道，用于数据库文件操作

class MysqlPipeline(object):
    """docstring for MysqlPipeline"""
    def __init__(self):
        settings = get_project_settings()
        self.host = settings['DB_HOST']
        self.port = settings['DB_PORT']
        self.user = settings['DB_USER']
        self.pwd = settings['DB_PWD']
        self.name = settings['DB_NAME']
        self.charset = settings['DB_CHARSET']

        self.connect()

    def connect(self):
        self.conn = pymysql.connect(host=self.host,
                             port=self.port,
                             user=self.user,
                             password=self.pwd,
                             db=self.name,
                             charset=self.charset)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql = 'insert into txvideo(name,url) values( "%s", "%s")' % (item['name'], item['url'])
        # 执行sql语句
        self.cursor.execute(sql)
        return item

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()
        self.cursor.close()