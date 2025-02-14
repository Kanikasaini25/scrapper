# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UrlscrapperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    publisherId = scrapy.Field()
    category = scrapy.Field()
    createdAt = scrapy.Field()
    region = scrapy.Field()
