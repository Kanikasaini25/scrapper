import json
import os

import requests
import scrapy

from urlscrapper.constants import Publisher_URL, getHeaders, Publisher_URL_ID


class PublisherService:

    def __init__(self):
        pass

    @classmethod
    def getPublishers(self):
        res = requests.get(Publisher_URL)
        # res=requests.get('https://crawler.ritamdigital.org/services/crawler/api/publishers?size=10000')
        if res.status_code == 200:
            return json.loads(res.text)
        else:
            raise scrapy.exceptions.DropItem("Failed to get publishers")

    @classmethod
    def getPublisherByPublisherId(self, publisherId):
        res = requests.get(Publisher_URL_ID.format( publisherId))
        #res = requests.get(f'https://ritamdigital.org/services/crawler/api/publishers/{publisherId}?page=0&size=500')
        if res.status_code == 200:
            return json.loads(res.text)
        else:
            raise scrapy.exceptions.DropItem("Failed to get publishers")
