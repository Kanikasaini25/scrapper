import os

import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TCPTimedOutError

from testScraper.postservice import PostService
from testScraper.publisherservice import PublisherService

class TestSpider(scrapy.Spider):
    name = 'testspider'
    postService = PostService()
    publisherService = PublisherService()

    def start_requests(self):
            try:
                language = os.environ['TESTING_LANGUAGE']
                if language is None:
                    language = 'Tamil'
                publishers = self.publisherService.getPublishersByLanguage(language)
                print('Total Publishers found ' + str(len(publishers)))
                i = 1
                for publisher in publishers:
                  try:
                    i = i + 1
                    print('Starting to scrape post for publisher ' + publisher['publisherName'] + ' at index ' + str(i))
                    spider_config = publisher['metaDataConfiguration']['urlConfigurations']
                    for config  in spider_config or []:
                            yield scrapy.Request(url=config['url'], meta={'publisherName': publisher['publisherName'], 'publisherId': publisher['id'], 'config': config}, callback=self.parse, errback=self.checkError)
                  except Exception as e:
                      print('Exception #1001 ' + publisher['publisherName'])
                      print(e)
                      continue
            except Exception as e:
                print('Exception--------------------------- ')
                print(e)
                pass

    def parse(self, response, **kwargs):
        self.postService.parseFromService(response)

    def checkError(self, failure):
        print('Spider Yield callback error----------------------------- ' + repr(failure.request.url))
        print(repr(failure))
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            print('HttpError on %s', response.url)
            self.logger.error('HttpError on %s', response.url)
            print('HttpError status code %s', response.status)
            self.logger.error('HttpError status code %s', response.status)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            print('DNSLookupError on %s', request.url)
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            print('TimeoutError on %s', request.url)
            self.logger.error('TimeoutError on %s', request.url)