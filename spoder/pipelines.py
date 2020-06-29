# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

import pymongo
import MySQLdb


class ScrapyTestPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    def __init__(self, username, password, dbname):
        self.connect = MySQLdb.connect(user=username, passwd=password, host="127.0.0.1", db=dbname)
        self.cursor = self.connect.cursor()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            crawler.settings["MYSQL_USER"], crawler.settings["PASSWORD"], crawler.settings["DBNAME"]
        )

    def process_item(self, item, spider):
        sql = "insert into book (title, img_url) values (%s, %s)"
        self.cursor.execute(sql, (item["title"], item["img_url"]))
        self.connect.commit()
        return item

    def open_spider(self, spider):
        self.cursor = self.connect.cursor()

    def close_spider(self, spider):
        self.connect.close()


class MyTextPipeline(object):
    def process_item(self, item, spider):
        print("===" * 10)
        return item


class TextPipeline(object):
    def __init__(self):
        self.limit = 50

    def process_item(self, item, spider):
        if item["text"]:
            if len(item["text"]) > self.limit:
                item["text"] = item["text"][0 : self.limit].rstrip() + "..."
            return item
        else:
            return DropItem("Missing Text")


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get("MONGO_URI"), (crawler.settings.get("MONGO_DB")))

    def open_spider(self, spider):
        """spider开启时调用, 初始化操作"""
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        """处理item数据函数"""
        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        return item

    def close_spider(self, spider):
        """spider关闭时被调用, 处理连接关闭操作"""
        self.client.close()

