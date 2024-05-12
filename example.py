import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['tweeter.com']
    start_urls = ['http://tweeter.com/']

    def parse(self, response):
        pass
