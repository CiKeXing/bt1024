# -*- coding: utf-8 -*-
import scrapy


class Bt1024Item(scrapy.Item):
    category = scrapy.Field()
    date = scrapy.Field()
    comments = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    bt_url = scrapy.Field()
    hash = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
