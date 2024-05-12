import json

import gc
import os

import requests
import scrapy

from onlinecourse.constants import getHeaders,ONLINE_COURSE_GET_PLAYLIST, ONLINE_COURSE_POST_VIDEO,HEADERS
from onlinecourse.repository.user_repository import UserRepository


class PostRepository:
    userRepository = UserRepository()

    def __init__(self):
        pass

    @classmethod
    def getOnlineCoursePlaylist(self):

        print('getting OnlineCourseList-----------')
        res = requests.get(ONLINE_COURSE_GET_PLAYLIST,verify=True,headers=HEADERS)
        print(res.text)
        if res.status_code == 200:
            return json.loads(res.text)
        else:
            raise scrapy.exceptions.DropItem("Failed to get Online Course Titles")

    def saveOnlineCourseList(self, OnlineCourseList):
        print("post saving---------------------------")
        # print(OnlineCourseList)
        res = requests.post(ONLINE_COURSE_POST_VIDEO, data=OnlineCourseList, headers=HEADERS,verify=True)
        print(res.text)
        print(res.status_code)
        if res.status_code == 200 or 201:
            print('Online Course Saved------------------')

        else:
            print('Online Course List Saving Error--------------------')
            # print(res.text)
            raise scrapy.exceptions.DropItem("Failed to Save Online Course List")