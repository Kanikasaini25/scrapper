import json

import gc
import os

import requests
import scrapy

from atharvaForum.constants import getHeaders,ATHRVA_FORUM_GET_PLAYLIST, ATHRVA_FORUM_POST_VIDEO
from atharvaForum.repository.user_repository import UserRepository


class PostRepository:
    userRepository = UserRepository()

    def __init__(self):
        pass

    @classmethod
    def getAtharvaForumPlaylist(self):

        print('getting athravaForumList-----------')
        # res= requests.get("https://crawler.ritamdigital.org/services/crawler/api/atharvaPlaylist",verify=True)
        res = requests.get(ATHRVA_FORUM_GET_PLAYLIST,verify=True)
        if res.status_code == 200:
            return json.loads(res.text)
        else:
            raise scrapy.exceptions.DropItem("Failed to get Dharmawiki Titles")

    def saveAthravaForumList(self, atharvaList):
        print("post saving---------------------------")
        # print(atharvaList)
        res = requests.post(ATHRVA_FORUM_POST_VIDEO, data=atharvaList, headers=getHeaders(), timeout=30,verify=False)
        # res= requests.post('https://crawler.ritamdigital.org/services/crawler/api/posts/external/athravaFurum/list',verify=False,data=atharvaList,headers=getHeaders())
        # print(res.text)
        if res.status_code == 200:
            print('Atharva Forum Saved------------------')

        else:
            print('Atharva Forum List Saving Error--------------------')
            # print(res.text)
            raise scrapy.exceptions.DropItem("Failed to Save Atharva Forum List")