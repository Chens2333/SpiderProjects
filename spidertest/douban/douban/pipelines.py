# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class DoubanPipeline(object):
    def open_spider(self, spider):
        self.f = open('douban.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        obj = dict(item)
        str_ = json.dumps(obj, ensure_ascii=False)
        self.f.write(str_ + '\n')
        return item

    def close_spider(self,spider):
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
        sql = 'insert into douban(movie_name,img_url,  movie_pl,movie_info,movie_IMDb,movie_actor) values("%s", "%s", "%s", "%s", "%s", "%s")' % (
            item['movie_name'], item['img_url'], item['movie_pl'], item['movie_info'], item['movie_IMDb'],
            item['movie_actor'])
        # 执行sql语句
        self.cursor.execute(sql)
        return item

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()
        self.cursor.close()
