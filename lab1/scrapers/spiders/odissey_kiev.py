# -*- coding: utf-8 -*-
from scrapy.http.response import Response
import scrapy


class OdisseySpider(scrapy.Spider):
    name = 'odissey_kiev'
    allowed_domains = ['odissey.kiev.ua']
    start_urls = ['https://odissey.kiev.ua/category_3640.html']

    def parse(self, response: Response):

        vals = response.xpath("//div[contains(@class, 'row table-row')]")[:15]

        for i in range(15):
            yield { 'description': vals.xpath("//a[contains(@class, 'pnameh')]/text()").extract()[i],
                    'price': vals.xpath("//div[contains(@class, 'pprice')]/text()").extract()[i],
                    'img': 'https://odissey.kiev.ua/' + vals.xpath("//img[contains(@class, 'thumbnail')]/@src").extract()[i] }
