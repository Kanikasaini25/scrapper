import json

import gc
import os

import requests
import scrapy

from urlscrapper.constants import getHeaders, ARTICLE_URL, DHARMAWIKI_SAVE_TITLE_URL, DHARMAWIKI_GET_TITLE_URL, DHARMAWIKI_GET_TITLE_URL_WITH_APCONTINUE
from urlscrapper.repository.user_repository import UserRepository


class PostRepository:
    userRepository = UserRepository()

    def __init__(self):
        pass

    @classmethod
    def savePost(self,posts):
        gc.collect()
        print(posts)
        # token = self.userRepository.getToken()
        res = requests.post(ARTICLE_URL ,data = posts, headers = getHeaders(),timeout=30,verify=False)
        #res = requests.post('https://crawler.ritamdigital.org/services/crawler/api/articlelinks/saveList', data = posts, headers = getHeaders(),timeout=30)
        if res.status_code == 200:
            print('posts saved------------------------------')
        else:
            print('exception===========')
            print(res.text)
            raise scrapy.exceptions.DropItem("Failed to post item with title")



    @classmethod
    def getDharmawikiPostTitles(self):
        print('getting Titles-----------')
        res = requests.get(DHARMAWIKI_GET_TITLE_URL)
        #res =requests.get("https://dharmawiki.org/api.php?action=query&list=allpages&format=json&aplimit=500")
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
        res = requests.post(DHARMAWIKI_SAVE_TITLE_URL, data=dharmawikiTitles, headers=getHeaders(), timeout=30)
        #res=requests.post("https://crawler.ritamdigital.org/services/crawler/api/dhamaWikiArticle/saveList")
        if res.status_code == 200:
            print('Dharmawiki Titles Saved------------------')
        else:
            print('Dharmawiki Title List Saving Error--------------------')
            print(res.text)
            raise scrapy.exceptions.DropItem("Failed to Save Dharmawiki Title List")

