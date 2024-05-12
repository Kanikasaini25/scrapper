import gc
import os
import datetime
import requests
import json
import scrapy
from newsscrapper.news_constants import Save_postAPI, DHARMAWIKI_POSTS_TITLE_URL, Save__DHARMAWIKIpostAPI,DHARMAWIKI_GET_ARTICLE_URL, DHARMAWIKI_GET_ARTICLE_CATEGORY_URL, DHARMAWIKI_GET_ARTICLE_IMAGE_URL, Remove_postAPI

class PostRepository:
    count=0
    def __init__(self):
        pass


    @classmethod
    def savePost(self,posts):
        # print('posts saving-----------------------')
        # print(posts)
        try:
            # print(Save_postAPI.format(os.environ['POST_IP'], os.environ['PORT']))
            # print(posts)
            res = requests.post(Save_postAPI , data = posts, headers = {'Content-Type': 'application/json'}, timeout=30,verify=False)
            # res = requests.post('https://crawler.ritamdigital.org/services/crawler/api/posts/external/news-feeds', data = posts, headers = {'Content-Type': 'application/json'}, timeout=30,verify=False)
            # res = requests.post('https://staging.ritamdigital.org/services/crawler/api/posts/external/news-feeds', data = posts, headers = {'Content-Type': 'application/json','Authorization':'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ6aW1vZ2dnaGVyIiwiYXV0aCI6IlJPTEVfRURJVE9SLFJPTEVfUklUQU1fU1VQRVJfQURNSU4iLCJleHAiOjE2OTU3Nzg4NzZ9.Njiypdd8DOD_1Vi9raJxOj6xPO89D3eVjlxt9e8VZvf7i9lpXfa7d9zYzpHU2P6WIl3Ut0fGs2NFqm2VHeUecw'}, timeout=30,verify=False)
            # print("res.status_code============= ")
            print(res.status_code)
            if res.status_code == 200:
                print('post saved on ----------------------',datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
                PostRepository.count = PostRepository.count + 1
                print("saved post --------------------------------------index at",PostRepository.count)
            else:
                print('exception while saving post=======================')
                print(res.text)
                raise scrapy.exceptions.DropItem(f"Failed to post item with {posts['title']} ")
        except Exception as e:
            print("Error while saving post -----------------------")
            print(e)

    @classmethod
    def saveDharmaWikiPost(self ,posts):
        print('posts-----------------------')
        # print(posts)
        try:
            res = requests.post(Save__DHARMAWIKIpostAPI, data = posts, headers = {'Content-Type': 'application/json'}, timeout=30)
            # res = requests.post('https://ritamdigital.org/services/crawler/api/articlelinks/saveList', data = posts, headers = {'Content-Type': 'application/json'}, timeout=30)
            if res.status_code == 200:
                print('post saved----------------------')
            else:
                print('exception while saving post=======================')
                print(res.text)
                raise scrapy.exceptions.DropItem(f"Failed to post item with {posts['title']} ")
        except Exception as e:
            print("Error while saving post -----------------------")
            print(e)

    @classmethod
    def removePost(self, posts):
        # print('posts removed------------article-----------')
        # print(posts)
        try:
            # print(Remove_postAPI.format(os.environ['POST_IP'], os.environ['PORT'],os.environ['PORT'], posts))
            res = requests.delete(Remove_postAPI.format(posts), timeout=30,verify=False)
            # res = requests.delete(f'https://crawler.ritamdigital.org/services/crawler/api/articlelinks/{posts}', timeout=30,headers = {'Authorization':'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJiYnVlYWx1dnZtIiwiYXV0aCI6IlJPTEVfRURJVE9SLFJPTEVfUklUQU1fU1VQRVJfQURNSU4iLCJleHAiOjE2OTcyNDg1MjN9.b1UG02N0GCl6orzfbTegxFrht70JrLXLaES3idLpeZI5WVsjsc5jL1Sq5ldYYhc5r7zcgJgN2XqyO3HhJb9pIw'})
            # print(res)
            # print('res.status_code==============')
            print(res.status_code)
            if res.status_code == 204:
                print('post deleted----------------------')
            else:
                print('exception while deleting post=======================')
                # print(res.text)
                raise scrapy.exceptions.DropItem(f"Failed to post item with {posts} ")
        except Exception as e:
            print("Error while deleting post -----------------------")
            print(e)

    @classmethod
    def getDharmaWikiPostTitles(self):
        res = requests.get(DHARMAWIKI_POSTS_TITLE_URL)
        # res = requests.get('http://crawler-staging.ritamdigital.org/services/crawler/api/publishers')
        # res = requests.get('https://dharmawiki.org/api.php?action=query&list=allpages&format=json&aplimit=500')
        # res=requests.get("https://crawler-staging.ritamdigital.org/services/crawler/api/dhama-wiki-articles")
        # print(res.text)
        if res.status_code == 200:
            return json.loads(res.text)
        else:
            print('exception while getting dharmawiki posts------------')
            print(res.text)
            raise scrapy.exceptions.DropItem("Failed to get publishers")


    @classmethod
    def getPostCategoryByTitle(self, title):
        res = requests.get(DHARMAWIKI_GET_ARTICLE_CATEGORY_URL.format(title))
        # res = requests.get(f'https://dharmawiki.org/api.php?action=query&format=json&titles={title}&prop=categories')
        if res.status_code == 200:
            return json.loads(res.text)
        else:
            print('exception while getting dharmawiki category by post title------------')
            print(res.text)
            raise scrapy.exceptions.DropItem("Failed to get publishers")

    @classmethod
    def getPostImageByTitle(self, title):
        res = requests.get(DHARMAWIKI_GET_ARTICLE_IMAGE_URL.format(title))
        # res = requests.get(f'https://dharmawiki.org/api.php?action=query&generator=images&titles={title}&prop=imageinfo&&iiprop=url&iiurlwidth=220&format=json')
        if res.status_code == 200:
            return json.loads(res.text)
        else:
            print('exception while getting dharmawiki images by post title------------')
            print(res.text)
            raise scrapy.exceptions.DropItem("Failed to get publishers")


