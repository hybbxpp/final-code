# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class LeedsdigItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Article(scrapy.Item):
    通用名称 = scrapy.Field()
    主要功能 = scrapy.Field()
    性状 = scrapy.Field()

