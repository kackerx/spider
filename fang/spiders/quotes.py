# -*- coding: utf-8 -*-
import scrapy

# from scrapy_test.items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]

    def parse(self, response):
        quotes = response.xpath('//div[@class="quote"]')

        for quote in quotes:
            item = QuoteItem()
            item["text"] = quote.xpath('.//span[@class="text"]/text()').extract_first()
            item["author"] = quote.xpath(".//small/text()").extract_first()
            item["tags"] = quote.xpath('./div[@class="tags"]/a/text()').extract()
            yield item

        next = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next:
            url = response.urljoin(next)

            yield scrapy.http.Request(url=url, callback=self.parse)

