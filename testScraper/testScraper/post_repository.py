import json

import gc
import os

import requests
import scrapy

from testScraper.constants import getHeaders, ARTICLE_URL, DHARMAWIKI_SAVE_TITLE_URL, DHARMAWIKI_GET_TITLE_URL, DHARMAWIKI_GET_TITLE_URL_WITH_APCONTINUE


class PostRepository:

    def __init__(self):
        pass

    @classmethod
    def savePost(self,posts):
        gc.collect()
        # token = self.userRepository.getToken()
        res = requests.post(ARTICLE_URL.format(os.environ['POST_IP'], os.environ['PORT']), data = posts, headers = getHeaders(),timeout=30)

        if res.status_code == 200:
            print('posts saved------------------------------')

        else:
            print('exception===========')
            print(res.text)
            raise scrapy.exceptions.DropItem("Failed to post item with title ")



    @classmethod
    def getDharmawikiPostTitles(self):
        print('getting Titles-----------')
        res = requests.get(DHARMAWIKI_GET_TITLE_URL)
        if res.status_code == 200:
            return json.loads(res.text)
        else:
            raise scrapy.exceptions.DropItem("Failed to get Dharmawiki Titles")


    @classmethod
    def getDharmawikiPostTitlesWithApContinue(self, apContinue):
        print('getting Titles-----------')
        res = requests.get(DHARMAWIKI_GET_TITLE_URL_WITH_APCONTINUE.format(apContinue))
        if res.status_code == 200:
            return json.loads(res.text)
        else:
            raise scrapy.exceptions.DropItem("Failed to get Dharmawiki Titles")


    @classmethod
    def saveDharmawikiTitleList(self, dharmawikiTitles):
        res = requests.post(DHARMAWIKI_SAVE_TITLE_URL.format(os.environ['POST_IP'], os.environ['PORT']), data=dharmawikiTitles, headers=getHeaders(), timeout=30)

        if res.status_code == 200:
            print('Dharmawiki Titles Saved------------------')

        else:
            print('Dharmawiki Title List Saving Error--------------------')
            print(res.text)
            raise scrapy.exceptions.DropItem("Failed to Save Dharmawiki Title List")

