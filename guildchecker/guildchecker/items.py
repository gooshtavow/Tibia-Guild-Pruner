# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GuildcheckerItem(scrapy.Item):
    name = scrapy.Field()
    rank = scrapy.Field()
    last_login = scrapy.Field()
    days_offline = scrapy.Field()
