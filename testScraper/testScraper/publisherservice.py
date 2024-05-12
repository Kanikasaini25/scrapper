import json
import os

import requests
import scrapy

from testScraper.constants import Publisher_URL, Publisher_URL_ID


class PublisherService:

    def __init__(self):
        pass

    @classmethod
    def getPublishersByLanguage(self, language):
        url = Publisher_URL.format(os.environ['POST_IP'], os.environ['PORT'], language)
        res = requests.get(url)
        if res.status_code == 200:
            return json.loads(res.text)
        else:
            raise scrapy.exceptions.DropItem("Failed to get publishers")

    @classmethod
    def getPublisherByPublisherId(self, publisherId):
        res = requests.get(Publisher_URL_ID.format(os.environ['POST_IP'], os.environ['PORT'], publisherId))
        if res.status_code == 200:
            return json.loads(res.text)
        else:
            raise scrapy.exceptions.DropItem("Failed to get publishers")
