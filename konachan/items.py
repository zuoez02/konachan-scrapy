# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KonachanItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    tag = scrapy.Field()
    folder = scrapy.Field()
    file_urls = scrapy.Field()

class YandereItem(scrapy.Item):
    id = scrapy.Field()
    tag = scrapy.Field()
    folder = scrapy.Field()
    file_urls = scrapy.Field()