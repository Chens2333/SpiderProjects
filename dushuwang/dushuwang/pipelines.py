# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class DushuwangPipeline(object):
    def open_spider(self,spider):
        self.f=open('book1.json','w',encoding='utf-8')


    def process_item(self, item, spider):
        obj=dict(item)
        str_=json.dumps(obj,ensure_ascii=False)
        self.f.write(str_+'\n')
        return item

    def close_spider(self):
        self.f.close()

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
        sql = 'insert into book(book_img_url, book_name, book_author,book_info) values("%s", "%s", "%s", "%s")' % (item['book_img_url'], item['book_name'], item['book_author'], item['book_info'])
        # 执行sql语句
        self.cursor.execute(sql)
        return item

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()
        self.cursor.close()