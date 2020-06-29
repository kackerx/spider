# -*- coding: utf-8 -*-
import scrapy
import re
from ..items import NewHouseItem, EsfItem


class FangSpider(scrapy.Spider):
    name = "fang"
    allowed_domains = ["fang.com"]
    start_urls = ["https://www.fang.com/SoufunFamily.htm"]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    # https://anqing.newhouse.fang.com/house/s/
    # https://anqing.esf.fang.com/

    # https://anqing.fang.com
    def parse(self, response):
        province = ""
        for tr in response.xpath('//table[@id="senfe"]//tr')[:-1]:
            tds = tr.xpath(".//td")
            print(len(tds))
            province_text = tds[1].xpath(".//strong/text()").extract_first()
            if province_text:
                province_text = province_text.replace("\xa0", "")
            if province_text:
                province = province_text
            for city in tds[2].xpath(".//a"):
                city_url = city.xpath(".//@href").extract_first()
                city_name = city.xpath(".//text()").extract_first()
                newhouse = re.sub("(http://\w+\.)", "\\1newhouse.", city_url).replace(
                    "http:", "https:"
                )
                esf = re.sub("(http://\w+\.)", "\\1esf.", city_url).replace("http:", "https:")
                yield scrapy.Request(
                    url=newhouse + "house/s/",
                    callback=self.parse_newhouse,
                    headers=self.headers,
                    meta={"info": (city_name, province)},
                )
                yield scrapy.Request(
                    url=esf,
                    callback=self.parse_esf,
                    headers=self.headers,
                    meta={"info": (city_name, province)},
                )

    def parse_esf(self, response):
        city, province = response.meta.get("info")
        for dl in response.xpath("//dl[@class='clearfix' and @dataflag='bg']"):
            name = dl.xpath(".//p[@class='add_shop']/a/@title").extract_first()
            address = dl.xpath(".//p[@class='add_shop']/span/text()").extract_first()
            price = dl.xpath(
                ".//dd[@class='price_right']/span[@class='red']/b/text()"
            ).extract_first()
            unit = dl.xpath(".//dd[@class='price_right']/span[not(@class)]/text()").extract_first()
            origin_url = dl.xpath(".//h4[@class='clearfix']/a/@href").extract_first()
            origin_url = response.urljoin(origin_url)
            info = dl.xpath(".//p[@class='tel_shop']/text()").extract()
            rooms = info[0].strip()
            area = info[1].strip()
            floor = info[2].strip()
            toward = info[3].strip()
            try:
                year = info[4].strip()
            except:
                year = "暂无年份"
            # item
            item = EsfItem(
                name=name,
                city=city,
                province=province,
                rooms=rooms,
                origin_url=origin_url,
                address=address,
                year=year,
                toward=toward,
                floor=floor,
                price=price,
                unit=unit,
                area=area,
            )
            yield item
        next_page = response.xpath("//a[contains(text(), '下一页')]/@href").extract_first()
        if next_page:
            yield scrapy.Request(
                url=response.urljoin(next_page),
                callback=self.parse_esf,
                meta={"info": (city, province)},
            )

    def parse_newhouse(self, response):
        lis = response.xpath("//div[@id='newhouse_loupai_list']/ul/li[not(@style)]")
        for li in lis:
            city, province = response.meta.get("info")
            name = li.xpath(".//div[@class='nlcd_name']/a/text()").extract_first().strip()
            price = li.xpath(".//div[@class='nhouse_price']/span/text()").extract_first()
            rooms = li.xpath(".//div[@class='house_type clearfix']/a/text()").extract()
            area = li.xpath(".//div[@class='house_type clearfix']/text()")
            address = li.xpath(".//div[@class='address']/a/@title").extract_first()
            district = li.xpath(".//div[@class='address']/a//text()")
            sale = li.xpath(".//div[starts-with(@class, 'fangyuan')]/span/text()").extract_first()
            origin_url = li.xpath(".//div[@class='nlcd_name']/a/@href").extract_first().strip()
            # 处理
            area = area[-1].extract().replace("－", "").strip()
            ret = re.search("\[(.*?)\]", district.extract_first())
            if ret:
                district = ret.group(1)
            else:
                district = "暂无相关信息"
            rooms = "/".join(rooms)
            # item
            item = NewHouseItem(
                name=name,
                city=city,
                price=price,
                rooms=rooms,
                district=district,
                province=province,
                area=area,
                address=address,
                sale=sale,
                origin_url=origin_url,
            )
            yield item

        # 下一页
        next_url = response.xpath('//a[contains(text(), "下一页")]/@href').extract_first()
        if next_url:
            yield scrapy.Request(
                url=response.urljoin(next_url),
                headers=self.headers,
                callback=self.parse_newhouse,
                meta={"info": (city, province)},
            )

