# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TestscraperItem(scrapy.Item):
    url = scrapy.Field()
    publisherId = scrapy.Field()
    category = scrapy.Field()
    createdAt = scrapy.Field()
    region = scrapy.Field()
