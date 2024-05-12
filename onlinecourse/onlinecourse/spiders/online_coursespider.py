import time

import scrapy

import googleapiclient.discovery

from onlinecourse.constants import API_KEY, DATE_FORMAT
from onlinecourse.service.postservice import PostService



class OnlineCourseSpider(scrapy.Spider):
    name = 'onlinecourse'
    postService = PostService()


    def start_requests(self):

        while True:
            print('sleeping')
            time.sleep(60*30)
            youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = API_KEY)
            OnlineCourseList = []
            try:
                response = self.postService.getOnlineCoursePlaylist()
                # print(response)
                for article in response:
                        request = youtube.playlistItems().list(
                            part="snippet",
                            playlistId=article["playlistId"],
                            maxResults=100000
                        )
                        responsedata = request.execute()
                        responsedata = responsedata['items']

                        for playlist in responsedata:
                            playlistData = playlist['snippet']
                            resourcearticle = playlistData['resourceId']
                            videoLink= resourcearticle['videoId']
                            OnlineCourseObject= {
                                "title": playlistData['title'],
                                "category": article["category"],
                                "mediaUrl": 'https://www.youtube.com/watch?v='+videoLink,
                                'createdAt':playlistData['publishedAt'].format(DATE_FORMAT),
                                'onlineCoursePlaylistId':article['id'],
                                'playlistId':article['playlistId'],
                                'onlineCoursePlaylistTitle':article["title"],
                                'language':article['language'],
                                "disabled": False,
                                'contributorName': article["contributorName"]
                            }
                            OnlineCourseList.append(OnlineCourseObject)
                        self.postService.saveOnlineCourseData(OnlineCourseList)
                time.sleep(60 * 30)



            except Exception as e:
                print('Exception Occurred------------')
                print(e)
                pass


