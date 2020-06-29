# -*- coding: utf-8 -*-

# Define here the models for your scraped items
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose


class EsfItem(scrapy.Item):
    province = scrapy.Field()
    city = scrapy.Field()
    name = scrapy.Field()
    area = scrapy.Field()
    price = scrapy.Field()
    unit = scrapy.Field()
    floor = scrapy.Field()
    toward = scrapy.Field()
    year = scrapy.Field()
    address = scrapy.Field()
    rooms = scrapy.Field()
    origin_url = scrapy.Field()


class NewHouseItem(scrapy.Item):
    province = scrapy.Field()
    city = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    rooms = scrapy.Field()
    area = scrapy.Field()
    address = scrapy.Field()
    district = scrapy.Field()
    sale = scrapy.Field()
    origin_url = scrapy.Field()


def pri(value):
    return value[1:]


class BookItem(scrapy.Item):
    name = scrapy.Field(input_processor=MapCompose(str.upper))  # 数名
    price = scrapy.Field(input_processor=MapCompose(lambda x: x[1:6]))  # 价格
    review_rating = scrapy.Field(input_processor=MapCompose(lambda x: x.split(" ")[1]))  # 评价等级
    review_num = scrapy.Field(input_processor=MapCompose(lambda x: int(x)))  # 评价数量
    upc = scrapy.Field()  # 产品编码
    stock = scrapy.Field()  # 库存
    img_url = scrapy.Field()


class BookItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

