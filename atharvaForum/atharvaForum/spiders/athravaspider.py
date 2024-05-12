import time

import scrapy

import googleapiclient.discovery

from atharvaForum.constants import API_KEY, DATE_FORMAT
from atharvaForum.service.postservice import PostService



class AtharvaForurmSpider(scrapy.Spider):
    name = 'atharvaforum'
    postService = PostService()


    def start_requests(self):

        while True:
            print('sleeping')
            time.sleep(60*15)
            youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = API_KEY)
            athravaList = []
            try:
                response = self.postService.getAtharvaPlaylist()
                # print(response)
                for article in response:
                    if article['postRedirectUrl'] == "1234":
                        continue
                    else:
                        request = youtube.playlistItems().list(
                            part="snippet",
                            playlistId='PLKzbJcWBKkbNnHUg12HiBtwLo_0Kx9CMV',
                            # playlistId=article['postRedirectUrl'],
                            maxResults=150
                        )
                        responsedata = request.execute()
                        responsedata = responsedata['items']

                        for playlist in responsedata:
                            playlistData = playlist['snippet']
                            resourcearticle = playlistData['resourceId']
                            videoLink= resourcearticle['videoId']
                            athravaObject= {
                                'title': playlistData['title'],
                                'videoLink': 'https://www.youtube.com/watch?v='+videoLink,
                                'publishedDate':playlistData['publishedAt'].format(DATE_FORMAT),
                                'videoPlaylistId':article['id'],
                                'language':article['language'],
                                'contributorName': article['publisher'],
                                'type': 'atharva_furum'
                            }
                            athravaList.append(athravaObject)
                            # print("---------------------------------------------------",athravaObject)
                self.postService.saveAtharvaForumData(athravaList)



            except Exception as e:
                print('Exception Occurred------------')
                print(e)
                pass


