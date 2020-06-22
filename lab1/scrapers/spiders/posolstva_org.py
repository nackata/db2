# -*- coding: utf-8 -*-
from scrapy.http.response import Response
import scrapy


class PosolstvaSpider(scrapy.Spider):
    name = 'posolstva_org'
    allowed_domains = ['posolstva.org.ua']
    start_urls = ['http://www.posolstva.org.ua/']

    def parse(self, response: Response):

        pictures = response.xpath("//img/@src[starts-with(., 'http')]")
        strings = response.xpath("//*[not(self::script)][not(self::style)][string-length(normalize-space(text())) > 30]/text()")

        yield {'url': response.url,
               'payload': [{'type': 'text', 'data': text.get().strip()} for text in strings] +
                       [{'type': 'image', 'data': image.get()} for image in pictures]}

        if response.url == self.start_urls[0]:

            refs = response.xpath("//a/@href")
            ref = [refs.get() for r in refs][:15]
            for r in ref:
                yield scrapy.Request('http://www.posolstva.org.ua' + r, self.parse)