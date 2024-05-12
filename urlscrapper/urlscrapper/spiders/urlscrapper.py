import os

import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TCPTimedOutError

from urlscrapper.service.postservice import PostService
from urlscrapper.service.publisherservice import PublisherService


class UrlSpider(scrapy.Spider):
    name = 'urlspider'
    postService = PostService()
    publisherService = PublisherService()

    def start_requests(self):
        try:
            publishers = self.publisherService.getPublishers()
            print('Total Publishers found ' + str(len(publishers)))
            i = 1
            for publisher in publishers:

                 if publisher['publisherName'] != '':
                    try:
                        print(publisher)
                        i = i + 1
                        print(
                            'Starting to scrape post for publisher ' + publisher['publisherName'] + ' at index ' + str(
                                i))
                        spider_config = publisher['metaDataConfiguration']['urlConfigurations']
                        for config in spider_config or []:
                            yield scrapy.Request(url=config['url'], meta={'publisherName': publisher['publisherName'],
                                                                          'publisherId': publisher['id'],
                                                                          'config': config,
                                                                          'regions': config['regions']

                                                                          },
                                                 callback=self.parse, errback=self.checkError)
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


class UrlSpiderByPublisherId(scrapy.Spider):
    name = 'urlspiderbypublisherid'
    postService = PostService()
    publisherService = PublisherService()

    def start_requests(self):

        try:
            # publisher = self.publisherService.getPublisherByPublisherId(os.environ['PUBLISHER_ID'])
            publisher = self.publisherService.getPublisherByPublisherId('dd61593c-348a-470f-9550-dcaafe642350')
            publishers = [publisher]
            for publisher in publishers:
                if publisher.languages is not None and 'Tamil' in publisher.languages:
                    spider_config = publisher['metaDataConfiguration']['urlConfigurations']
                    print(publisher['publisherName'])
                    for config in spider_config or []:
                        yield scrapy.Request(url=config['url'], meta={'publisherName': publisher['publisherName'],
                                                                      'publisherId': publisher['id'], 'config': config},
                                             callback=self.parse, errback=self.checkError)

        except Exception as e:
            print('Exception---------------------------')
            print(e)
            pass

    def parse(self, response, **kwargs):
        # self.postService.parseFromService(response)
        print('')

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

class DharmawikiSpider(scrapy.Spider):
    name = 'dharmawiki'
    postService = PostService()
    publisherService = PublisherService()

    def start_requests(self):
        apContinue = None
        try:
            response = self.postService.getDharmawikiTitles()
            dharmawikiTitles = response['query']['allpages']
            if 'continue' in response and 'apcontinue' in response['continue']:
                apContinue = response['continue']['apcontinue']
            [title.pop('ns', None) for title in dharmawikiTitles]
            # print("----------------------------------",apContinue)
            # print("--------------------------------------------------", dharmawikiTitles)

            for title in dharmawikiTitles:
                # print(title)
                title['pageid'] = str(title['pageid'])
                # print(title['pageid'])
            # dharmawikiTitles = [{'pageId': '104407', 'title': 'Indian Agricultural Systems (भारतीय कृषि दृष्टि)'}, {'pageId': '5325', 'title': 'Indian Approach on Languages (धार्मिक भाषा दृष्टि)'}, {'pageId': '104429', 'title': 'Indian Approach on Languages (भारतीय भाषा दृष्टि)'}]

            self.postService.saveDharmawikiTitleList(dharmawikiTitles)
            while True:
                if apContinue is None:
                    break
                apContinue = self.getMoreArticles(apContinue)
        except Exception as e:
            print('Exception---------------------------')
            print(e)
            pass

    def getMoreArticles(self, apContinue):
        try:
            response = self.postService.getDharmawikiTitlesWithApContinue(apContinue)

            dharmawikiTitles = response['query']['allpages']
            if 'continue' in response and 'apcontinue' in response['continue']:
                apContinue = response['continue']['apcontinue']
            else:
                apContinue = None
            [title.pop('ns', None) for title in dharmawikiTitles]

            for title in dharmawikiTitles:
                title['pageid'] = str(title['pageid'])
            # dharmawikiTitles = [{'pageId': '104407', 'title': 'Indian Agricultural Systems (भारतीय कृषि दृष्टि)'}, {'pageId': '5325', 'title': 'Indian Approach on Languages (धार्मिक भाषा दृष्टि)'}, {'pageId': '104429', 'title': 'Indian Approach on Languages (भारतीय भाषा दृष्टि)'}]

            self.postService.saveDharmawikiTitleList(dharmawikiTitles)
        except Exception as e:
            print('Exception---------------------------')
            print(e)
        return apContinue