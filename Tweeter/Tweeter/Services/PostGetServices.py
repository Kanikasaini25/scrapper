import requests
import logging
from bs4 import BeautifulSoup
from Tweeter.constants import  user_agent_header, twitter_trends_url, api_headers,ritam_api_url
from scrapy.utils.serialize import ScrapyJSONEncoder

_encoder = ScrapyJSONEncoder()

class PostGetServices:


    def __init__(self):
        self.logger = logging.getLogger(__name__)


    def CreatePost(self, list):
        print("Start creating post")
        return self.save_trending_tags(_encoder.encode(list))



    def GetTwitterTrendingTopics(self,url):
        try:
            print("Start scraping------")
            response = requests.get(url, headers=user_agent_header)
            soup = BeautifulSoup(response.text, 'html.parser')

            trend_tags = soup.select("table tbody tr th:nth-child(2) a")
            total_tweets = soup.select("table tbody tr th:nth-child(3)")

            tags = [element.text for element in trend_tags]
            tweets = [element.text for element in total_tweets]

            TotalTweets=self.convert_list_to_integers(tweets)
            print("Scraping completed successfully")
            return tags, TotalTweets

        except requests.RequestException as e:
            print(f"Error in scraping: {e}")
            return [], []


    def convert_list_to_integers(self,values):
        converted_values = []

        for value in values:
            if value.lower() == 'under 10k':
                # Handle the case where the value is 'Under 10k'
                converted_values.append(10000)
            else:
                # Remove 'k' if present and convert to integer
                converted_values.append(int(float(value.replace('k', ''))) * 1000)

        return converted_values



    def save_trending_tags(self,list):
        try:
            print("Saving post")
            print(list)
            response = requests.post(ritam_api_url, data=list, headers=api_headers)
            print(f"API Response: {response.status_code}")
            if response.status_code == 200 or 201:
                print("Post saved successfully")
            else:
                print(f"Failed to save post. Response: {response.content}")

        except requests.RequestException as e:
            print(f"Error in saving post: {e}")

