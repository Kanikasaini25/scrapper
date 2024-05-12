import os
import scrapy
import time

from newsscrapper.news_constants import DHARMAWIKI_GET_ARTICLE_URL
from newsscrapper.service.news_post_service import NewsPostService
from newsscrapper.service.publisher_service import PublisherService
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from newsscrapper.settings import USER_AGENT

class NewsSpider(scrapy.Spider):
    name = "NewsSpider"
    postService = NewsPostService()
    publisherService = PublisherService()

    def start_requests(self):
        while(True):
            try:
                testing_with_language = None
                language = None
                if 'TEST_WITH_LANGUAGE' in os.environ and 'TESTING_LANGUAGE' in os.environ:
                    testing_with_language = os.environ['TEST_WITH_LANGUAGE']
                    language = os.environ['TESTING_LANGUAGE']
                if testing_with_language == 'True' and language is not None:
                    response = self.publisherService.getPublishersByLanguage(language)
                else:
                    response = self.publisherService.getPublishers()
                    # print(response)
                    publishers = response
                    for publisher in publishers:
                        publisherId = publisher['id']
                        publisherName = publisher["publisherName"]
                        meta = publisher["metaDataConfiguration"]["articleDomConfigurations"]
                        languages = publisher["languages"]
                        for language in languages:
                                if language !='':
                                    if publisherName !='':
                                        articleUrls = self.publisherService.getPosts(publisherId)
                                        # print(publisherName)
                                        for articleUrl in articleUrls:
                                            urls = articleUrl["url"]
                                            region = articleUrl["region"]
                                            category = articleUrl["category"]
                                            articleId = articleUrl["id"]
                                            if "http" in urls:
                                                yield scrapy.Request(url=urls, callback=self.parse, errback=self.errback_httpbin,
                                                                     cb_kwargs=dict(category=category, publisherName=publisherName,
                                                                                    publisherId=publisherId, url=urls, config=meta,
                                                                                    region=region, articleId=articleId,lang=language))
                                            else:
                                                    # f"invalid articleUrl: {urls}"
                                                    print("invalid url")

            except Exception as e:
                        print('Exception Occurred------------ ')
                        print(e)
                        pass

            break


    def parse(self, response, **kwargs):
        category = response.cb_kwargs["category"]
        publisherName = response.cb_kwargs["publisherName"]
        publisherId = response.cb_kwargs["publisherId"]
        articleId = response.cb_kwargs["publisherId"]
        url = response.cb_kwargs["url"]
        lang_name=response.cb_kwargs['lang']
        config = response.cb_kwargs["config"]
        region = response.cb_kwargs["region"]
        self.postService.parseFromService(response, category, publisherId, publisherName, url, config, region,articleId,lang_name)

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))
        # in case you want to do something special for some errors,
        # you may need the failure's type:
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)





class DharmawikiSpider(scrapy.Spider):
    name = 'dharmawikipost'
    postService = NewsPostService()
    publisherService = PublisherService()

    def start_requests(self):
        try:
            response = self.postService.getDharmawikiTitles()
            # for article in response:
            for article in response["query"]["allpages"]:
                # print("-----------------------------------------article",article)
                title = article['title']
                # print("title----------------------",title)
                yield scrapy.Request(url = DHARMAWIKI_GET_ARTICLE_URL.format(title), headers=USER_AGENT, callback=self.parse,)
        except Exception as e:
            print('Exception Occurred------------')
            print(e)
            pass


    def parse(self, response):
        self.postService.createDharmaWikiPost(response.text)

class SewaSpider(scrapy.Spider):
    name = "SewaSpider"
    postService = NewsPostService()
    publisherService = PublisherService()

    def start_requests(self):
        while(True):
            lang_id = 1
            if lang_id == 1:
                lang_id = 3
            elif lang_id == 3:
                lang_id = 1
            try:
                response = self.publisherService.getSewaPost(lang_id)
                nData = response['data']['data']
                for publisher in nData:
                    title = publisher['title']
                    area = publisher['area']
                    id = publisher['id']
                    news_content = publisher["news_content"]
                    details_page_image = publisher["details_page_image"]
                    language = publisher["language"]["name"]
                    created_date = publisher["created_at"]["nonformatted_date"]
                    created_time = publisher["created_at"]["formatted_time"]
                    url = publisher['url']
                    print("--------------------------------------language",language)
                    created_at = created_date + ' ' + created_time
                    self.postService.sewaPost(title,news_content, details_page_image, language, created_at, area, id,url)

            except Exception as e:
                print('Exception Occurred------------ ')
                print(e)
                pass



    def parse(self, response, **kwargs):
        category = response.cb_kwargs["category"]
        publisherName = response.cb_kwargs["publisherName"]
        publisherId = response.cb_kwargs["publisherId"]
        articleId = response.cb_kwargs["publisherId"]
        url = response.cb_kwargs["url"]
        config = response.cb_kwargs["config"]
        region = response.cb_kwargs["region"]
        self.postService.parseFromService(response, category, publisherId, publisherName, url,config, region,articleId)

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))
        # in case you want to do something special for some errors,
        # you may need the failure's type:
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)

class NewsSpiderHindi(scrapy.Spider):
    name = "NewsSpiderHindi"
    postService = NewsPostService()
    publisherService = PublisherService()

    def start_requests(self):
        while(True):
            try:
                testing_with_language = None
                language = None
                if 'TEST_WITH_LANGUAGE' in os.environ and 'TESTING_LANGUAGE' in os.environ:
                    testing_with_language = os.environ['TEST_WITH_LANGUAGE']
                    language = os.environ['TESTING_LANGUAGE']
                if testing_with_language == 'True' and language is not None:
                    response = self.publisherService.getPublishersByLanguage(language)
                else:
                    response = self.publisherService.getPublishers()
                    # print(response)
                    publishers = response
                    for publisher in publishers:
                        publisherId = publisher['id']
                        publisherName = publisher["publisherName"]
                        meta = publisher["metaDataConfiguration"]["articleDomConfigurations"]
                        languages = publisher["languages"]
                        for language in languages:
                                if language =='Hindi':
                                    if publisherName !='':
                                        articleUrls = self.publisherService.getPosts(publisherId)
                                        # print(publisherName)
                                        for articleUrl in articleUrls:
                                            urls = articleUrl["url"]
                                            region = articleUrl["region"]
                                            category = articleUrl["category"]
                                            articleId = articleUrl["id"]
                                            if "http" in urls:
                                                yield scrapy.Request(url=urls, callback=self.parse, errback=self.errback_httpbin,
                                                                     cb_kwargs=dict(category=category, publisherName=publisherName,
                                                                                    publisherId=publisherId, url=urls, config=meta,
                                                                                    region=region, articleId=articleId,lang=language))
                                            else:
                                                    # f"invalid articleUrl: {urls}"
                                                    print("invalid url")

            except Exception as e:
                        print('Exception Occurred------------ ')
                        print(e)
                        pass

            break

    def parse(self, response, **kwargs):
            category = response.cb_kwargs["category"]
            publisherName = response.cb_kwargs["publisherName"]
            publisherId = response.cb_kwargs["publisherId"]
            articleId = response.cb_kwargs["publisherId"]
            url = response.cb_kwargs["url"]
            lang_name = response.cb_kwargs['lang']
            config = response.cb_kwargs["config"]
            region = response.cb_kwargs["region"]
            self.postService.parseFromService(response, category, publisherId, publisherName, url, config, region,
                                              articleId, lang_name)

    def errback_httpbin(self, failure):
            # log all failures
            self.logger.error(repr(failure))
            # in case you want to do something special for some errors,
            # you may need the failure's type:
            if failure.check(HttpError):
                # these exceptions come from HttpError spider middleware
                # you can get the non-200 response
                response = failure.value.response
                self.logger.error('HttpError on %s', response.url)

            elif failure.check(DNSLookupError):
                # this is the original request
                request = failure.request
                self.logger.error('DNSLookupError on %s', request.url)

            elif failure.check(TimeoutError, TCPTimedOutError):
                request = failure.request
                self.logger.error('TimeoutError on %s', request.url)



class NewsSpiderEnglish(scrapy.Spider):
    name = "NewsSpiderEnglish"
    postService = NewsPostService()
    publisherService = PublisherService()

    def start_requests(self):
        while(True):
            try:
                testing_with_language = None
                language = None
                if 'TEST_WITH_LANGUAGE' in os.environ and 'TESTING_LANGUAGE' in os.environ:
                    testing_with_language = os.environ['TEST_WITH_LANGUAGE']
                    language = os.environ['TESTING_LANGUAGE']
                if testing_with_language == 'True' and language is not None:
                    response = self.publisherService.getPublishersByLanguage(language)
                else:
                    response = self.publisherService.getPublishers()
                    # print(response)
                    publishers = response
                    for publisher in publishers:
                        publisherId = publisher['id']
                        publisherName = publisher["publisherName"]
                        meta = publisher["metaDataConfiguration"]["articleDomConfigurations"]
                        languages = publisher["languages"]
                        for language in languages:
                                if language =='English':
                                    if publisherName !='':
                                        articleUrls = self.publisherService.getPosts(publisherId)
                                        # print(publisherName)
                                        for articleUrl in articleUrls:
                                            urls = articleUrl["url"]
                                            region = articleUrl["region"]
                                            category = articleUrl["category"]
                                            articleId = articleUrl["id"]
                                            if "http" in urls:
                                                yield scrapy.Request(url=urls, callback=self.parse, errback=self.errback_httpbin,
                                                                     cb_kwargs=dict(category=category, publisherName=publisherName,
                                                                                    publisherId=publisherId, url=urls, config=meta,
                                                                                    region=region, articleId=articleId,lang=language))
                                            else:
                                                    # f"invalid articleUrl: {urls}"
                                                    print("invalid url")

            except Exception as e:
                        print('Exception Occurred------------ ')
                        print(e)
                        pass

            break


    def parse(self, response, **kwargs):
        category = response.cb_kwargs["category"]
        publisherName = response.cb_kwargs["publisherName"]
        publisherId = response.cb_kwargs["publisherId"]
        articleId = response.cb_kwargs["publisherId"]
        url = response.cb_kwargs["url"]
        lang_name=response.cb_kwargs['lang']
        config = response.cb_kwargs["config"]
        region = response.cb_kwargs["region"]
        self.postService.parseFromService(response, category, publisherId, publisherName, url, config, region,articleId,lang_name)

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))
        # in case you want to do something special for some errors,
        # you may need the failure's type:
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)

class NewsSpiderBengali(scrapy.Spider):
    name = "NewsSpiderBengali"
    postService = NewsPostService()
    publisherService = PublisherService()

    def start_requests(self):
        while(True):
            try:
                testing_with_language = None
                language = None
                if 'TEST_WITH_LANGUAGE' in os.environ and 'TESTING_LANGUAGE' in os.environ:
                    testing_with_language = os.environ['TEST_WITH_LANGUAGE']
                    language = os.environ['TESTING_LANGUAGE']
                if testing_with_language == 'True' and language is not None:
                    response = self.publisherService.getPublishersByLanguage(language)
                else:
                    response = self.publisherService.getPublishers()
                    # print(response)
                    publishers = response
                    for publisher in publishers:
                        publisherId = publisher['id']
                        publisherName = publisher["publisherName"]
                        meta = publisher["metaDataConfiguration"]["articleDomConfigurations"]
                        languages = publisher["languages"]
                        for language in languages:
                                if language =='Bengali':
                                    if publisherName !='':
                                        articleUrls = self.publisherService.getPosts(publisherId)
                                        # print(publisherName)
                                        for articleUrl in articleUrls:
                                            urls = articleUrl["url"]
                                            region = articleUrl["region"]
                                            category = articleUrl["category"]
                                            articleId = articleUrl["id"]
                                            if "http" in urls:
                                                yield scrapy.Request(url=urls, callback=self.parse, errback=self.errback_httpbin,
                                                                     cb_kwargs=dict(category=category, publisherName=publisherName,
                                                                                    publisherId=publisherId, url=urls, config=meta,
                                                                                    region=region, articleId=articleId,lang=language))
                                            else:
                                                    # f"invalid articleUrl: {urls}"
                                                    print("invalid url")

            except Exception as e:
                        print('Exception Occurred------------ ')
                        print(e)
                        pass

            break


    def parse(self, response, **kwargs):
        category = response.cb_kwargs["category"]
        publisherName = response.cb_kwargs["publisherName"]
        publisherId = response.cb_kwargs["publisherId"]
        articleId = response.cb_kwargs["publisherId"]
        url = response.cb_kwargs["url"]
        lang_name=response.cb_kwargs['lang']
        config = response.cb_kwargs["config"]
        region = response.cb_kwargs["region"]
        self.postService.parseFromService(response, category, publisherId, publisherName, url, config, region,articleId,lang_name)

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))
        # in case you want to do something special for some errors,
        # you may need the failure's type:
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)

class NewsSpiderPunjabi(scrapy.Spider):
    name = "NewsSpiderPunjabi"
    postService = NewsPostService()
    publisherService = PublisherService()

    def start_requests(self):
        while(True):
            try:
                testing_with_language = None
                language = None
                if 'TEST_WITH_LANGUAGE' in os.environ and 'TESTING_LANGUAGE' in os.environ:
                    testing_with_language = os.environ['TEST_WITH_LANGUAGE']
                    language = os.environ['TESTING_LANGUAGE']
                if testing_with_language == 'True' and language is not None:
                    response = self.publisherService.getPublishersByLanguage(language)
                else:
                    response = self.publisherService.getPublishers()
                    # print(response)
                    publishers = response
                    for publisher in publishers:
                        publisherId = publisher['id']
                        publisherName = publisher["publisherName"]
                        meta = publisher["metaDataConfiguration"]["articleDomConfigurations"]
                        languages = publisher["languages"]
                        for language in languages:
                                if language =='Punjabi':
                                    if publisherName !='':
                                        articleUrls = self.publisherService.getPosts(publisherId)
                                        # print(publisherName)
                                        for articleUrl in articleUrls:
                                            urls = articleUrl["url"]
                                            region = articleUrl["region"]
                                            category = articleUrl["category"]
                                            articleId = articleUrl["id"]
                                            if "http" in urls:
                                                yield scrapy.Request(url=urls, callback=self.parse, errback=self.errback_httpbin,
                                                                     cb_kwargs=dict(category=category, publisherName=publisherName,
                                                                                    publisherId=publisherId, url=urls, config=meta,
                                                                                    region=region, articleId=articleId,lang=language))
                                            else:
                                                    # f"invalid articleUrl: {urls}"
                                                    print("invalid url")

            except Exception as e:
                        print('Exception Occurred------------ ')
                        print(e)
                        pass

            break


    def parse(self, response, **kwargs):
        category = response.cb_kwargs["category"]
        publisherName = response.cb_kwargs["publisherName"]
        publisherId = response.cb_kwargs["publisherId"]
        articleId = response.cb_kwargs["publisherId"]
        url = response.cb_kwargs["url"]
        lang_name=response.cb_kwargs['lang']
        config = response.cb_kwargs["config"]
        region = response.cb_kwargs["region"]
        self.postService.parseFromService(response, category, publisherId, publisherName, url, config, region,articleId,lang_name)

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))
        # in case you want to do something special for some errors,
        # you may need the failure's type:
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)

class NewsSpiderGujarati(scrapy.Spider):
    name = "NewsSpiderGujarati"
    postService = NewsPostService()
    publisherService = PublisherService()

    def start_requests(self):
        while(True):
            try:
                testing_with_language = None
                language = None
                if 'TEST_WITH_LANGUAGE' in os.environ and 'TESTING_LANGUAGE' in os.environ:
                    testing_with_language = os.environ['TEST_WITH_LANGUAGE']
                    language = os.environ['TESTING_LANGUAGE']
                if testing_with_language == 'True' and language is not None:
                    response = self.publisherService.getPublishersByLanguage(language)
                else:
                    response = self.publisherService.getPublishers()
                    # print(response)
                    publishers = response
                    for publisher in publishers:
                        publisherId = publisher['id']
                        publisherName = publisher["publisherName"]
                        meta = publisher["metaDataConfiguration"]["articleDomConfigurations"]
                        languages = publisher["languages"]
                        for language in languages:
                                if language =='Gujarati':
                                    if publisherName !='':
                                        articleUrls = self.publisherService.getPosts(publisherId)
                                        # print(publisherName)
                                        for articleUrl in articleUrls:
                                            urls = articleUrl["url"]
                                            region = articleUrl["region"]
                                            category = articleUrl["category"]
                                            articleId = articleUrl["id"]
                                            if "http" in urls:
                                                yield scrapy.Request(url=urls, callback=self.parse, errback=self.errback_httpbin,
                                                                     cb_kwargs=dict(category=category, publisherName=publisherName,
                                                                                    publisherId=publisherId, url=urls, config=meta,
                                                                                    region=region, articleId=articleId,lang=language))
                                            else:
                                                    # f"invalid articleUrl: {urls}"
                                                    print("invalid url")

            except Exception as e:
                        print('Exception Occurred------------ ')
                        print(e)
                        pass

            break


    def parse(self, response, **kwargs):
        category = response.cb_kwargs["category"]
        publisherName = response.cb_kwargs["publisherName"]
        publisherId = response.cb_kwargs["publisherId"]
        articleId = response.cb_kwargs["publisherId"]
        url = response.cb_kwargs["url"]
        lang_name=response.cb_kwargs['lang']
        config = response.cb_kwargs["config"]
        region = response.cb_kwargs["region"]
        self.postService.parseFromService(response, category, publisherId, publisherName, url, config, region,articleId,lang_name)

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))
        # in case you want to do something special for some errors,
        # you may need the failure's type:
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)

class NewsSpiderTamil(scrapy.Spider):
    name = "NewsSpiderTamil"
    postService = NewsPostService()
    publisherService = PublisherService()

    def start_requests(self):
        while(True):
            try:
                testing_with_language = None
                language = None
                if 'TEST_WITH_LANGUAGE' in os.environ and 'TESTING_LANGUAGE' in os.environ:
                    testing_with_language = os.environ['TEST_WITH_LANGUAGE']
                    language = os.environ['TESTING_LANGUAGE']
                if testing_with_language == 'True' and language is not None:
                    response = self.publisherService.getPublishersByLanguage(language)
                else:
                    response = self.publisherService.getPublishers()
                    # print(response)
                    publishers = response
                    for publisher in publishers:
                        publisherId = publisher['id']
                        publisherName = publisher["publisherName"]
                        meta = publisher["metaDataConfiguration"]["articleDomConfigurations"]
                        languages = publisher["languages"]
                        for language in languages:
                                if language =='Tamil':
                                    if publisherName !='':
                                        articleUrls = self.publisherService.getPosts(publisherId)
                                        # print(publisherName)
                                        for articleUrl in articleUrls:
                                            urls = articleUrl["url"]
                                            region = articleUrl["region"]
                                            category = articleUrl["category"]
                                            articleId = articleUrl["id"]
                                            if "http" in urls:
                                                yield scrapy.Request(url=urls, callback=self.parse, errback=self.errback_httpbin,
                                                                     cb_kwargs=dict(category=category, publisherName=publisherName,
                                                                                    publisherId=publisherId, url=urls, config=meta,
                                                                                    region=region, articleId=articleId,lang=language))
                                            else:
                                                    # f"invalid articleUrl: {urls}"
                                                    print("invalid url")

            except Exception as e:
                        print('Exception Occurred------------ ')
                        print(e)
                        pass

            break


    def parse(self, response, **kwargs):
        category = response.cb_kwargs["category"]
        publisherName = response.cb_kwargs["publisherName"]
        publisherId = response.cb_kwargs["publisherId"]
        articleId = response.cb_kwargs["publisherId"]
        url = response.cb_kwargs["url"]
        lang_name=response.cb_kwargs['lang']
        config = response.cb_kwargs["config"]
        region = response.cb_kwargs["region"]
        self.postService.parseFromService(response, category, publisherId, publisherName, url, config, region,articleId,lang_name)

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))
        # in case you want to do something special for some errors,
        # you may need the failure's type:
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)

class NewsSpiderTelugu(scrapy.Spider):
    name = "NewsSpiderTelugu"
    postService = NewsPostService()
    publisherService = PublisherService()

    def start_requests(self):
        while(True):
            try:
                testing_with_language = None
                language = None
                if 'TEST_WITH_LANGUAGE' in os.environ and 'TESTING_LANGUAGE' in os.environ:
                    testing_with_language = os.environ['TEST_WITH_LANGUAGE']
                    language = os.environ['TESTING_LANGUAGE']
                if testing_with_language == 'True' and language is not None:
                    response = self.publisherService.getPublishersByLanguage(language)
                else:
                    response = self.publisherService.getPublishers()
                    # print(response)
                    publishers = response
                    for publisher in publishers:
                        publisherId = publisher['id']
                        publisherName = publisher["publisherName"]
                        meta = publisher["metaDataConfiguration"]["articleDomConfigurations"]
                        languages = publisher["languages"]
                        for language in languages:
                                if language =='Telugu':
                                    if publisherName !='':
                                        articleUrls = self.publisherService.getPosts(publisherId)
                                        # print(publisherName)
                                        for articleUrl in articleUrls:
                                            urls = articleUrl["url"]
                                            region = articleUrl["region"]
                                            category = articleUrl["category"]
                                            articleId = articleUrl["id"]
                                            if "http" in urls:
                                                yield scrapy.Request(url=urls, callback=self.parse, errback=self.errback_httpbin,
                                                                     cb_kwargs=dict(category=category, publisherName=publisherName,
                                                                                    publisherId=publisherId, url=urls, config=meta,
                                                                                    region=region, articleId=articleId,lang=language))
                                            else:
                                                    # f"invalid articleUrl: {urls}"
                                                    print("invalid url")

            except Exception as e:
                        print('Exception Occurred------------ ')
                        print(e)
                        pass

            break


    def parse(self, response, **kwargs):
        category = response.cb_kwargs["category"]
        publisherName = response.cb_kwargs["publisherName"]
        publisherId = response.cb_kwargs["publisherId"]
        articleId = response.cb_kwargs["publisherId"]
        url = response.cb_kwargs["url"]
        lang_name=response.cb_kwargs['lang']
        config = response.cb_kwargs["config"]
        region = response.cb_kwargs["region"]
        self.postService.parseFromService(response, category, publisherId, publisherName, url, config, region,articleId,lang_name)

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))
        # in case you want to do something special for some errors,
        # you may need the failure's type:
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)

class NewsSpiderMarathi(scrapy.Spider):
    name = "NewsSpiderMarathi"
    postService = NewsPostService()
    publisherService = PublisherService()

    def start_requests(self):
        while(True):
            try:
                testing_with_language = None
                language = None
                if 'TEST_WITH_LANGUAGE' in os.environ and 'TESTING_LANGUAGE' in os.environ:
                    testing_with_language = os.environ['TEST_WITH_LANGUAGE']
                    language = os.environ['TESTING_LANGUAGE']
                if testing_with_language == 'True' and language is not None:
                    response = self.publisherService.getPublishersByLanguage(language)
                else:
                    response = self.publisherService.getPublishers()
                    # print(response)
                    publishers = response
                    for publisher in publishers:
                        publisherId = publisher['id']
                        publisherName = publisher["publisherName"]
                        meta = publisher["metaDataConfiguration"]["articleDomConfigurations"]
                        languages = publisher["languages"]
                        for language in languages:
                                if language =='Marathi':
                                    if publisherName !='':
                                        articleUrls = self.publisherService.getPosts(publisherId)
                                        # print(publisherName)
                                        for articleUrl in articleUrls:
                                            urls = articleUrl["url"]
                                            region = articleUrl["region"]
                                            category = articleUrl["category"]
                                            articleId = articleUrl["id"]
                                            if "http" in urls:
                                                yield scrapy.Request(url=urls, callback=self.parse, errback=self.errback_httpbin,
                                                                     cb_kwargs=dict(category=category, publisherName=publisherName,
                                                                                    publisherId=publisherId, url=urls, config=meta,
                                                                                    region=region, articleId=articleId,lang=language))
                                            else:
                                                    # f"invalid articleUrl: {urls}"
                                                    print("invalid url")

            except Exception as e:
                        print('Exception Occurred------------ ')
                        print(e)
                        pass

            break


    def parse(self, response, **kwargs):
        category = response.cb_kwargs["category"]
        publisherName = response.cb_kwargs["publisherName"]
        publisherId = response.cb_kwargs["publisherId"]
        articleId = response.cb_kwargs["publisherId"]
        url = response.cb_kwargs["url"]
        lang_name=response.cb_kwargs['lang']
        config = response.cb_kwargs["config"]
        region = response.cb_kwargs["region"]
        self.postService.parseFromService(response, category, publisherId, publisherName, url, config, region,articleId,lang_name)

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))
        # in case you want to do something special for some errors,
        # you may need the failure's type:
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)

class NewsSpiderMalayalam(scrapy.Spider):
    name = "NewsSpiderMalayalam"
    postService = NewsPostService()
    publisherService = PublisherService()

    def start_requests(self):
        while(True):
            try:
                testing_with_language = None
                language = None
                if 'TEST_WITH_LANGUAGE' in os.environ and 'TESTING_LANGUAGE' in os.environ:
                    testing_with_language = os.environ['TEST_WITH_LANGUAGE']
                    language = os.environ['TESTING_LANGUAGE']
                if testing_with_language == 'True' and language is not None:
                    response = self.publisherService.getPublishersByLanguage(language)
                else:
                    response = self.publisherService.getPublishers()
                    # print(response)
                    publishers = response
                    for publisher in publishers:
                        publisherId = publisher['id']
                        publisherName = publisher["publisherName"]
                        meta = publisher["metaDataConfiguration"]["articleDomConfigurations"]
                        languages = publisher["languages"]
                        for language in languages:
                                if language =='Malayalam':
                                    if publisherName !='':
                                        articleUrls = self.publisherService.getPosts(publisherId)
                                        # print(publisherName)
                                        for articleUrl in articleUrls:
                                            urls = articleUrl["url"]
                                            region = articleUrl["region"]
                                            category = articleUrl["category"]
                                            articleId = articleUrl["id"]
                                            if "http" in urls:
                                                yield scrapy.Request(url=urls, callback=self.parse, errback=self.errback_httpbin,
                                                                     cb_kwargs=dict(category=category, publisherName=publisherName,
                                                                                    publisherId=publisherId, url=urls, config=meta,
                                                                                    region=region, articleId=articleId,lang=language))
                                            else:
                                                    # f"invalid articleUrl: {urls}"
                                                    print("invalid url")

            except Exception as e:
                        print('Exception Occurred------------ ')
                        print(e)
                        pass

            break


    def parse(self, response, **kwargs):
        category = response.cb_kwargs["category"]
        publisherName = response.cb_kwargs["publisherName"]
        publisherId = response.cb_kwargs["publisherId"]
        articleId = response.cb_kwargs["publisherId"]
        url = response.cb_kwargs["url"]
        lang_name=response.cb_kwargs['lang']
        config = response.cb_kwargs["config"]
        region = response.cb_kwargs["region"]
        self.postService.parseFromService(response, category, publisherId, publisherName, url, config, region,articleId,lang_name)

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))
        # in case you want to do something special for some errors,
        # you may need the failure's type:
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)

class NewsSpiderOdiya(scrapy.Spider):
    name = "NewsSpiderOdiya"
    postService = NewsPostService()
    publisherService = PublisherService()

    def start_requests(self):
        while(True):
            try:
                testing_with_language = None
                language = None
                if 'TEST_WITH_LANGUAGE' in os.environ and 'TESTING_LANGUAGE' in os.environ:
                    testing_with_language = os.environ['TEST_WITH_LANGUAGE']
                    language = os.environ['TESTING_LANGUAGE']
                if testing_with_language == 'True' and language is not None:
                    response = self.publisherService.getPublishersByLanguage(language)
                else:
                    response = self.publisherService.getPublishers()
                    # print(response)
                    publishers = response
                    for publisher in publishers:
                        publisherId = publisher['id']
                        publisherName = publisher["publisherName"]
                        meta = publisher["metaDataConfiguration"]["articleDomConfigurations"]
                        languages = publisher["languages"]
                        for language in languages:
                                if language =='Odiya':
                                    if publisherName !='':
                                        articleUrls = self.publisherService.getPosts(publisherId)
                                        # print(publisherName)
                                        for articleUrl in articleUrls:
                                            urls = articleUrl["url"]
                                            region = articleUrl["region"]
                                            category = articleUrl["category"]
                                            articleId = articleUrl["id"]
                                            if "http" in urls:
                                                yield scrapy.Request(url=urls, callback=self.parse, errback=self.errback_httpbin,
                                                                     cb_kwargs=dict(category=category, publisherName=publisherName,
                                                                                    publisherId=publisherId, url=urls, config=meta,
                                                                                    region=region, articleId=articleId,lang=language))
                                            else:
                                                    # f"invalid articleUrl: {urls}"
                                                    print("invalid url")

            except Exception as e:
                        print('Exception Occurred------------ ')
                        print(e)
                        pass

            break


    def parse(self, response, **kwargs):
        category = response.cb_kwargs["category"]
        publisherName = response.cb_kwargs["publisherName"]
        publisherId = response.cb_kwargs["publisherId"]
        articleId = response.cb_kwargs["publisherId"]
        url = response.cb_kwargs["url"]
        lang_name=response.cb_kwargs['lang']
        config = response.cb_kwargs["config"]
        region = response.cb_kwargs["region"]
        self.postService.parseFromService(response, category, publisherId, publisherName, url, config, region,articleId,lang_name)

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))
        # in case you want to do something special for some errors,
        # you may need the failure's type:
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)

class NewsSpiderKannada(scrapy.Spider):
    name = "NewsSpiderKannada"
    postService = NewsPostService()
    publisherService = PublisherService()

    def start_requests(self):
        while(True):
            try:
                testing_with_language = None
                language = None
                if 'TEST_WITH_LANGUAGE' in os.environ and 'TESTING_LANGUAGE' in os.environ:
                    testing_with_language = os.environ['TEST_WITH_LANGUAGE']
                    language = os.environ['TESTING_LANGUAGE']
                if testing_with_language == 'True' and language is not None:
                    response = self.publisherService.getPublishersByLanguage(language)
                else:
                    response = self.publisherService.getPublishers()
                    # print(response)
                    publishers = response
                    for publisher in publishers:
                        publisherId = publisher['id']
                        publisherName = publisher["publisherName"]
                        meta = publisher["metaDataConfiguration"]["articleDomConfigurations"]
                        languages = publisher["languages"]
                        for language in languages:
                                if language =='Kannada':
                                    if publisherName !='':
                                        articleUrls = self.publisherService.getPosts(publisherId)
                                        # print(publisherName)
                                        for articleUrl in articleUrls:
                                            urls = articleUrl["url"]
                                            region = articleUrl["region"]
                                            category = articleUrl["category"]
                                            articleId = articleUrl["id"]
                                            if "http" in urls:
                                                yield scrapy.Request(url=urls, callback=self.parse, errback=self.errback_httpbin,
                                                                     cb_kwargs=dict(category=category, publisherName=publisherName,
                                                                                    publisherId=publisherId, url=urls, config=meta,
                                                                                    region=region, articleId=articleId,lang=language))
                                            else:
                                                    # f"invalid articleUrl: {urls}"
                                                    print("invalid url")

            except Exception as e:
                        print('Exception Occurred------------ ')
                        print(e)
                        pass

            break


    def parse(self, response, **kwargs):
        category = response.cb_kwargs["category"]
        publisherName = response.cb_kwargs["publisherName"]
        publisherId = response.cb_kwargs["publisherId"]
        articleId = response.cb_kwargs["publisherId"]
        url = response.cb_kwargs["url"]
        lang_name=response.cb_kwargs['lang']
        config = response.cb_kwargs["config"]
        region = response.cb_kwargs["region"]
        self.postService.parseFromService(response, category, publisherId, publisherName, url, config, region,articleId,lang_name)

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))
        # in case you want to do something special for some errors,
        # you may need the failure's type:
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)

class NewsSpiderSanskrit(scrapy.Spider):
    name = "NewsSpiderSanskrit"
    postService = NewsPostService()
    publisherService = PublisherService()

    def start_requests(self):
        while(True):
            try:
                testing_with_language = None
                language = None
                if 'TEST_WITH_LANGUAGE' in os.environ and 'TESTING_LANGUAGE' in os.environ:
                    testing_with_language = os.environ['TEST_WITH_LANGUAGE']
                    language = os.environ['TESTING_LANGUAGE']
                if testing_with_language == 'True' and language is not None:
                    response = self.publisherService.getPublishersByLanguage(language)
                else:
                    response = self.publisherService.getPublishers()
                    # print(response)
                    publishers = response
                    for publisher in publishers:
                        publisherId = publisher['id']
                        publisherName = publisher["publisherName"]
                        meta = publisher["metaDataConfiguration"]["articleDomConfigurations"]
                        languages = publisher["languages"]
                        for language in languages:
                                if language =='Sanskrit':
                                    if publisherName !='':
                                        articleUrls = self.publisherService.getPosts(publisherId)
                                        # print(publisherName)
                                        for articleUrl in articleUrls:
                                            urls = articleUrl["url"]
                                            region = articleUrl["region"]
                                            category = articleUrl["category"]
                                            articleId = articleUrl["id"]
                                            if "http" in urls:
                                                yield scrapy.Request(url=urls, callback=self.parse, errback=self.errback_httpbin,
                                                                     cb_kwargs=dict(category=category, publisherName=publisherName,
                                                                                    publisherId=publisherId, url=urls, config=meta,
                                                                                    region=region, articleId=articleId,lang=language))
                                            else:
                                                    # f"invalid articleUrl: {urls}"
                                                    print("invalid url")

            except Exception as e:
                        print('Exception Occurred------------ ')
                        print(e)
                        pass

            break


    def parse(self, response, **kwargs):
        category = response.cb_kwargs["category"]
        publisherName = response.cb_kwargs["publisherName"]
        publisherId = response.cb_kwargs["publisherId"]
        articleId = response.cb_kwargs["publisherId"]
        url = response.cb_kwargs["url"]
        lang_name=response.cb_kwargs['lang']
        config = response.cb_kwargs["config"]
        region = response.cb_kwargs["region"]
        self.postService.parseFromService(response, category, publisherId, publisherName, url, config, region,articleId,lang_name)

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))
        # in case you want to do something special for some errors,
        # you may need the failure's type:
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)

class NewsSpiderNepali(scrapy.Spider):
    name = "NewsSpiderNepali"
    postService = NewsPostService()
    publisherService = PublisherService()

    def start_requests(self):
        while(True):
            try:
                testing_with_language = None
                language = None
                if 'TEST_WITH_LANGUAGE' in os.environ and 'TESTING_LANGUAGE' in os.environ:
                    testing_with_language = os.environ['TEST_WITH_LANGUAGE']
                    language = os.environ['TESTING_LANGUAGE']
                if testing_with_language == 'True' and language is not None:
                    response = self.publisherService.getPublishersByLanguage(language)
                else:
                    response = self.publisherService.getPublishers()
                    # print(response)
                    publishers = response
                    for publisher in publishers:
                        publisherId = publisher['id']
                        publisherName = publisher["publisherName"]
                        meta = publisher["metaDataConfiguration"]["articleDomConfigurations"]
                        languages = publisher["languages"]
                        for language in languages:
                                if language =='Nepali':
                                    if publisherName !='':
                                        articleUrls = self.publisherService.getPosts(publisherId)
                                        # print(publisherName)
                                        for articleUrl in articleUrls:
                                            urls = articleUrl["url"]
                                            region = articleUrl["region"]
                                            category = articleUrl["category"]
                                            articleId = articleUrl["id"]
                                            if "http" in urls:
                                                yield scrapy.Request(url=urls, callback=self.parse, errback=self.errback_httpbin,
                                                                     cb_kwargs=dict(category=category, publisherName=publisherName,
                                                                                    publisherId=publisherId, url=urls, config=meta,
                                                                                    region=region, articleId=articleId,lang=language))
                                            else:
                                                    # f"invalid articleUrl: {urls}"
                                                    print("invalid url")

            except Exception as e:
                        print('Exception Occurred------------ ')
                        print(e)
                        pass

            break


    def parse(self, response, **kwargs):
        category = response.cb_kwargs["category"]
        publisherName = response.cb_kwargs["publisherName"]
        publisherId = response.cb_kwargs["publisherId"]
        articleId = response.cb_kwargs["publisherId"]
        url = response.cb_kwargs["url"]
        lang_name=response.cb_kwargs['lang']
        config = response.cb_kwargs["config"]
        region = response.cb_kwargs["region"]
        self.postService.parseFromService(response, category, publisherId, publisherName, url, config, region,articleId,lang_name)

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))
        # in case you want to do something special for some errors,
        # you may need the failure's type:
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)

class NewsSpiderUrdu(scrapy.Spider):
    name = "NewsSpiderUrdu"
    postService = NewsPostService()
    publisherService = PublisherService()

    def start_requests(self):
        while(True):
            try:
                testing_with_language = None
                language = None
                if 'TEST_WITH_LANGUAGE' in os.environ and 'TESTING_LANGUAGE' in os.environ:
                    testing_with_language = os.environ['TEST_WITH_LANGUAGE']
                    language = os.environ['TESTING_LANGUAGE']
                if testing_with_language == 'True' and language is not None:
                    response = self.publisherService.getPublishersByLanguage(language)
                else:
                    response = self.publisherService.getPublishers()
                    # print(response)
                    publishers = response
                    for publisher in publishers:
                        publisherId = publisher['id']
                        publisherName = publisher["publisherName"]
                        meta = publisher["metaDataConfiguration"]["articleDomConfigurations"]
                        languages = publisher["languages"]
                        for language in languages:
                                if language =='Urdu':
                                    if publisherName !='':
                                        articleUrls = self.publisherService.getPosts(publisherId)
                                        # print(publisherName)
                                        for articleUrl in articleUrls:
                                            urls = articleUrl["url"]
                                            region = articleUrl["region"]
                                            category = articleUrl["category"]
                                            articleId = articleUrl["id"]
                                            if "http" in urls:
                                                yield scrapy.Request(url=urls, callback=self.parse, errback=self.errback_httpbin,
                                                                     cb_kwargs=dict(category=category, publisherName=publisherName,
                                                                                    publisherId=publisherId, url=urls, config=meta,
                                                                                    region=region, articleId=articleId,lang=language))
                                            else:
                                                    # f"invalid articleUrl: {urls}"
                                                    print("invalid url")

            except Exception as e:
                        print('Exception Occurred------------ ')
                        print(e)
                        pass

            break


    def parse(self, response, **kwargs):
        category = response.cb_kwargs["category"]
        publisherName = response.cb_kwargs["publisherName"]
        publisherId = response.cb_kwargs["publisherId"]
        articleId = response.cb_kwargs["publisherId"]
        url = response.cb_kwargs["url"]
        lang_name=response.cb_kwargs['lang']
        config = response.cb_kwargs["config"]
        region = response.cb_kwargs["region"]
        self.postService.parseFromService(response, category, publisherId, publisherName, url, config, region,articleId,lang_name)

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))
        # in case you want to do something special for some errors,
        # you may need the failure's type:
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)