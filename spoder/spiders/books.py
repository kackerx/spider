# -*- coding: utf-8 -*-
import scrapy
from ..items import BookItem, BookItemLoader


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]

    def parse(self, response):
        lis = response.css("li.col-xs-6.col-sm-4.col-md-3.col-lg-3")
        for li in lis:
            title = li.css("h3 a::text").extract_first()
            img_url = li.css("img.thumbnail::attr('src')").extract_first()
            price = li.css(".price_color::text").extract_first()
            content_url = li.css("div.image_container > a::attr('href')").extract_first()
            yield scrapy.Request(
                url=response.urljoin(content_url),
                callback=self.parse_detail,
                meta={"price": price, "img_url": img_url},
            )

    def parse_detail(self, response):
        book_loader = BookItemLoader(item=BookItem(), response=response)

        book_loader.add_xpath(
            "review_num", "//table[@class='table table-striped']//tr[last()]/td/text()"
        )
        book_loader.add_xpath(
            "stock", "//table[@class='table table-striped']//tr[last() - 1]/td/text()"
        )
        book_loader.add_xpath("upc", "//table[@class='table table-striped']//tr[1]/td/text()")
        book_loader.add_xpath("review_rating", "//i[@class='icon-star']/../@class")
        book_loader.add_xpath("name", "//div[@class='col-sm-6 product_main']/h1/text()")
        book_loader.add_value("price", response.meta.get("price"))
        book_loader.add_value("img_url", response.meta.get("img_url"))

        item = book_loader.load_item()

        yield item

