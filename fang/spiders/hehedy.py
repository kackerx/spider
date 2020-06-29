from scrapy import signals
from loguru import logger

# -*- coding: utf-8 -*-
import scrapy


class HehedySpider(scrapy.Spider):
    name = "hehedy"
    allowed_domains = ["hehedy.com"]
    start_urls = ["https://www.hehedy.com/"]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self):
        logger.success("success")

    def parse(self, response):
        # bid_req = scrapy.Request(url="https://www.baidu.com", callback=self.parse_detail)
        # resp = yield self.crawler.engine.download(bid_req, self)
        # print(resp)
        print(response.url)

    def parse_detail(self, response):
        print(response)

