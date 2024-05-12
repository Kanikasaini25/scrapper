import feedparser
import datetime
import time
import json
import requests

import scrapy
from bs4 import BeautifulSoup


class RssSpiderSpider(scrapy.Spider):
    name = "rss_spider"

    def start_requests(self):
        while True:
                time.sleep(60*1)
                print("scrapping===========================")
                today_date = datetime.datetime.today().strftime('%d-%m-%Y')
                rss_feed_url = 'https://ritamdigital.com/feed'
                feed = feedparser.parse(rss_feed_url)

                entries = feed.entries if 'entries' in feed else []

                for entry in entries:
                    title = entry.title
                    link = entry.link
                    description = entry.summary if 'summary' in entry else ''
                    pubDate = entry.published_parsed if 'published_parsed' in entry else None
                    category = entry.category if 'category' in entry else ''
                    img = entry.get('thumbnail', '')

                    # Handle the case when pubDate is None
                    if pubDate is not None:
                        formatted_pubDate = datetime.datetime.utcfromtimestamp(time.mktime(pubDate)).strftime(
                            '%d-%m-%Y %H:%M:%S')
                    else:
                        formatted_pubDate = None
                    post = {
                            "title": title,
                            "postRedirectUrl": link,
                            "publisherName": 'Ritam Digital English',
                            "description": description,
                            'pubDate': formatted_pubDate,
                            "publisherId": '71674e8f-ffeb-4acf-b20c-f10317639eca',
                            "category": category,
                            "language": 'English',
                            "posterUrl": img,
                            "region": "",
                            "postType": "news",
                            'dateFormat': 'dd-MM-yyyy HH:mm:ss',
                            "countWords": 'Greater'
                        }

                    post_json = json.dumps(post)
                    print('posts saving-----------------------')

                    try:
                            print(post)
                            res = requests.post('https://crawler.ritamdigital.org/services/crawler/api/posts/external/news-feeds',
                                data=post_json, headers={'Content-Type': 'application/json',}, timeout=30, verify=False)

                            print(res.status_code)

                            if res.status_code == 200:

                                print(f'post saved on {datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")}')
                            else:
                                print('exception while saving post=======================')
                                print(res.text)
                                raise scrapy.exceptions.DropItem(f"Failed to post item with {post['title']} ")
                                continue
                    except requests.RequestException as e:
                            print("Error while saving post -----------------------")
                            print(e)
                            continue









class RssSpiderSpiderHindi(scrapy.Spider):
    name = "rss_spider_hindi"

    def start_requests(self):
        while True:
                time.sleep(60*1)
                print("scrapping===========================")
                today_date = datetime.datetime.today().strftime('%d-%m-%Y')
                rss_feed_url = 'https://ritamdigital.in/feed'
                feed = feedparser.parse(rss_feed_url)
                entries = feed.entries if 'entries' in feed else []

                for entry in entries:
                    title = entry.title
                    link = entry.link
                    description = entry.summary if 'summary' in entry else ''
                    pubDate = entry.published_parsed if 'published_parsed' in entry else None
                    category = entry.category if 'category' in entry else ''
                    img_url = entry.content[0].value if entry.get('content') else None
                    soup = BeautifulSoup(img_url, 'html.parser')
                    img = soup.find('img').get('src') if soup.find('img') else None
                    soup = BeautifulSoup(description, 'html.parser')
                    cleaned_description = ' '.join(soup.stripped_strings)


                    if pubDate is not None:
                        formatted_pubDate = datetime.datetime.utcfromtimestamp(time.mktime(pubDate)).strftime(
                            '%d-%m-%Y %H:%M:%S')
                    else:
                        formatted_pubDate = None

                    post = {
                            "title": title,
                            "postRedirectUrl": link,
                            "publisherName": 'Ritam Digital Hindi',
                            "description": cleaned_description,
                            'pubDate': formatted_pubDate,
                            "publisherId": 'd5c7ff4f-cf0c-4c83-9cff-681fd3ebbd7f',
                            "category": category,
                            "language": 'Hindi',
                            "posterUrl": img,
                            "region": "",
                            "postType": "news",
                            'dateFormat': 'dd-MM-yyyy HH:mm:ss',
                            "countWords": 'Greater'
                        }

                    post_json = json.dumps(post)
                    print('posts saving-----------------------')

                    try:
                            print(post)
                            res = requests.post('https://crawler.ritamdigital.org/services/crawler/api/posts/external/news-feeds',
                                data=post_json, headers={'Content-Type': 'application/json'}, timeout=30, verify=False)

                            print(res.status_code)

                            if res.status_code == 200:
                                print(f'post saved on {datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")}')
                            else:
                                print('exception while saving post=======================')
                                print(res.text)
                                raise scrapy.exceptions.DropItem(f"Failed to post item with {post['title']} ")
                                continue
                    except requests.RequestException as e:
                            print("Error while saving post -----------------------")
                            print(e)
                            continue


class LiveUpTodayHindi(scrapy.Spider):
    name = "live_uptoday"

    def start_requests(self):
        while True:
            time.sleep(60*1)
            print("Scraping===========================")
            rss_feed_url = 'https://liveuptoday.com/feed/'
            feed = feedparser.parse(rss_feed_url)
            entries = feed.entries if 'entries' in feed else []

            for entry in entries:
                title = entry.title
                link = entry.link
                description = entry.summary if 'summary' in entry else ''
                pubDate = entry.published_parsed if 'published_parsed' in entry else None
                category = entry.category if 'category' in entry else ''
                img_url = entry.content[0].value if entry.get('content') else None
                soup = BeautifulSoup(img_url, 'html.parser')
                img = soup.find('img').get('src') if soup.find('img') else None
                soup = BeautifulSoup(description, 'html.parser')
                cleaned_description = ' '.join(soup.stripped_strings)

                if pubDate is not None:
                    formatted_pubDate = datetime.datetime.utcfromtimestamp(time.mktime(pubDate)).strftime(
                        '%d-%m-%Y %H:%M:%S')
                else:
                    formatted_pubDate = None

                post = {
                    "title": title,
                    "postRedirectUrl": link,
                    "publisherName": 'LIVE UP TODAY',
                    "description": cleaned_description,
                    'pubDate': formatted_pubDate,
                    "publisherId": '1bb5e732-24a2-4d84-9dd5-6e702d6a1f34',
                    "category": category,
                    "language": 'Hindi',
                    "posterUrl": img,
                    "region": "",
                    "postType": "news",
                    'dateFormat': 'dd-MM-yyyy HH:mm:ss',
                    "countWords": 'Greater'
                }

                post_json = json.dumps(post)
                print('Posts saving-----------------------')

                try:
                    print(post)
                    res = requests.post('https://crawler.ritamdigital.org/services/crawler/api/posts/external/news-feeds',
                                        data=post_json, headers={'Content-Type': 'application/json'}, timeout=30, verify=False)

                    print(res.status_code)

                    if res.status_code == 200:
                        print(f'Post saved on {datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")}')
                    else:
                        print('Exception while saving post=======================')
                        print(res.text)
                        continue
                except requests.RequestException as e:
                    print("Error while saving post -----------------------")
                    print(e)
                    continue