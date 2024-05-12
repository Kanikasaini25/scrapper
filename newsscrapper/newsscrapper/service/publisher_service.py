import json
import os

import requests
import scrapy
from newsscrapper.news_constants import ArticlesAPI, Publisher_URL, PublishersAPI

class PublisherService:

    def _init_(self):
        pass

    @classmethod
    def getPublishers(self):
        res = requests.get(PublishersAPI,verify=True)
        # res = requests.get('https://crawler.ritamdigital.org/services/crawler/api/publishers?size=10000',verify=True)
        # res = requests.get('https://staging.ritamdigital.org/services/ritam/api/publishers?size=10000')
        if res.status_code == 200:
            # print(res.text)
            return json.loads(res.text)
        else:
            print('exception while getting publishers------------')
            print(res.text)
            raise scrapy.exceptions.DropItem("Failed to get publishers")

    @classmethod
    def getPublishersByLanguage(self, language):
        url = Publisher_URL.format(language)
        res = requests.get(url)
        if res.status_code == 200:
            return json.loads(res.text)
        else:
            raise scrapy.exceptions.DropItem("Failed to get publishers")

    @classmethod
    def getSewaPost(self, lang_id):
        url = Publisher_URL.format(lang_id)
        # url = 'https://www.sewagatha.org/api/v1/podcasts'
        # url='https://www.sewagatha.org/api/v1/news'
        # url = f'https://www.sewagatha.org/api/v1/news?publish=true&language={lang_id}&limit=6&page=1'
        res = requests.get(url)
        if res.status_code == 200:

            return json.loads(res.text)
        else:
            raise scrapy.exceptions.DropItem("Failed to get publishers")

    @classmethod
    def getPosts(self, id):
        res = requests.get(ArticlesAPI.format( id))
        # res = requests.get(f'https://crawler.ritamdigital.org/services/crawler/api/articlelinks/publisher/{id}')
        if res.status_code == 200:
            # print('article links received======================')
            print(res.text)
            return json.loads(res.text)
        else:
            print('exception while getting article links-------------------')
            print(res.text)
            raise scrapy.exceptions.DropItem("Failed to get publishers")

