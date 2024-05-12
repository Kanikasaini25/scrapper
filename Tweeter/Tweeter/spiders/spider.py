import scrapy
from datetime import datetime
import time
from Tweeter.Services.PostGetServices import PostGetServices
from Tweeter.constants import world_api, twitter_trends_url

class TwitterSpider(scrapy.Spider):
    name = "twitter_trends"
    post_service = PostGetServices()

    def start_requests(self):
        print("Sleeping before starting...")

        while True:
            time.sleep(60*1)
            try:
                total_tweets = []

                tags, tweets = self.post_service.GetTwitterTrendingTopics(twitter_trends_url)
                list_india = self.parse(tags, tweets, "India")
                total_tweets.extend(list_india)

                tags, tweets = self.post_service.GetTwitterTrendingTopics(world_api)
                list_world = self.parse(tags, tweets, "World")
                total_tweets.extend(list_world)

                print("Creating Posts...")
                self.post_service.CreatePost(total_tweets)

            except Exception as e:
                print(f"Error in spider: {e}")

            print("Sleeping between iterations...")
            time.sleep(60 * 10)

    def parse(self, tags, tweets, country):
        post_list = []
        for tag, tweet_count in zip(tags, tweets):
            date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            post = {
                "title": tag,
                "redirectUrl": f'http://twitter.com/search?q={tag}',
                "country": country,
                "disabled": False,
                "createdAt": date,
                "totalTweets": tweet_count,
                "displayOrder": 0
            }
            post_list.append(post)
        return post_list
