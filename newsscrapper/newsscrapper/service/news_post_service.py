import datetime
import json
import logging
import datefinder
from langdetect import detect
from bs4 import BeautifulSoup
from ftfy import fix_text
from lxml import etree
from newsscrapper.repository import PostRepository
from scrapy.utils.serialize import ScrapyJSONEncoder

_encoder = ScrapyJSONEncoder()
class NewsPostService:
    postRepository = PostRepository()
    count=0

    @classmethod
    def createPost(self, posts):
        self.postRepository.savePost(_encoder.encode(posts))

    @classmethod
    def removePost(self, articleId):
        self.postRepository.removePost(articleId)

    @classmethod
    def parseFromService(self, response, category, publisherId, publisherName, url, config, region, articleId,lang_name):
        html = response.text
        print("==============================response==============================")
        soup = BeautifulSoup(html, features='lxml')
        if config is not None and len(config) > 1:
            meta_config = config[0]
        else:
            meta_config = config
        title = self.extract_title(soup, response, meta_config, publisherName)
        description,countWords = self.extract_description(soup, response, meta_config, publisherName)
        image_url = self.extract_image(soup, response, meta_config, publisherName)
        language_title = self.lang_detect(title,lang_name)
        language_desc = self.lang_detect(description,lang_name)
        region = region
        language = language_title
        # print("language_title-----------------",language_title)
        # print("language_desc------------------", language_desc)
        today = self.dateFormat()
        createdAt=self.date_time(soup, response, meta_config, publisherName)
        # createdAt = self.date_time(soup, publisherName)
        post = self.constructPost(title, language, description, image_url, publisherName, publisherId, createdAt,
                                  category, region, url,countWords)
        print(post)
        # print('post saving scraping ------------------------------')
        if  description and title is not None:
                if url is not None:
                                        if createdAt is None:
                                            # print(f'post saving without date ----------publisherName: {publisherName}--------------------')
                                            # self.createPost(post)
                                            self.removePost(articleId)
                                            # logging.info('post saving without date ----------publisherName %s',publisherName)

                                        else:
                                            if today == createdAt.split('T')[0]:
                                                # NewsPostService.count = NewsPostService.count + 1
                                                if language_desc == language_title :
                                                            # print(f'post saving with date ------publisherName: {publisherName}------------------')
                                                            self.createPost(post)
                                                            # logging.info('post saved on %s', today)
                                                            # self.removePost(articleId)
                                                else:
                                                    # print(f'post not save due to language miss match ------publisherName: {publisherName}------------------')
                                                    # self.createPost(post)
                                                    self.removePost(articleId)
                                            else:
                                                # print("-----------------------------------------",createdAt)
                                                # print(f'post not saved due to date ----------publisherName: {publisherName}--------------------')
                                                self.removePost(articleId)
                                                # logging.info('post not saved due to date ----------publisherName %s', publisherName)
                                                # self.createPost(post)
                else:
                                        # NewsPostService.count = NewsPostService.count + 1
                                        # print(f'post not saved due to Url ----------publisherName: {publisherName}--------------------')
                                        # pass
                                        # logging.info('post not saved due to language miss match ----------publisherName %s',publisherName)
                                        self.removePost(articleId)
                                        # self.createPost(post)
        else:
            # print(f'post not saved due to Title and Description ----------publisherName:{publisherName}--------------------')
            self.removePost(articleId)
            # logging.info('post not saved due to Title and Description ----------publisherName', publisherName)
            # self.createPost(post)

    @classmethod
    def sewaPost(self, title, description, image_url, language, createdAt, area, id, url):
        publisherName = "Sewagatha"
        category = "Top Stories"
        region = area
        url = f'https://www.sewagatha.org/news/{url}'
        publisherId = '1823cf8a-dd63-4dd9-a3ff-4aacc44dbccd'
        # print("constructing post-----")
        post = self.constructPost(title, language, description, image_url, publisherName, publisherId, createdAt,
                                  category, region, url)
        self.createPost(post)

    @classmethod
    def dateFormat(self):
        a_datetime = datetime.date.today()
        # formatted_datetime = a_datetime.isoformat()
        return str(a_datetime)

    @classmethod
    def constructPost(self, title, language, description, image_url, publisherName, publisherId, createdAt, category,
                      region,url,countWords):
        global dateformat
        dateformat = "dd-MM-yyyy HH:mm:ss"
        if createdAt != None:
            if publisherName == "Sewagatha":
                dateformat = "dd-MM-yyyy HH:mm a"
                date = createdAt
            else:
                createdAt = createdAt.split('+')[0]
                date = datetime.datetime.strptime(createdAt, '%Y-%m-%dT%H:%M:%S')
                date = date.strftime("%d-%m-%Y %H:%M:%S")
                dateformat = "dd-MM-yyyy HH:mm:ss"
        else:
            date = None
        post = {"title": title, "language": language, "description": description, "posterUrl": image_url,
                "publisherName": publisherName, 'pubDate': date, "publisherId": publisherId, "category": category,
                "postRedirectUrl": url
            , "region": region, "postType": "news", 'dateFormat': dateformat,"countWords":countWords}
        return post

    @classmethod
    def extract_title(self, soup, response, config, publisherName):
        if config != None and len(config) >= 1:
                # print("-------------------------title------------------")
            # if config[0]['fetchedByMetaTags'] == False or config[0]['fetchedByMetaTags'] == "":
                if config[0]["title"] != None and config[0]["title"] != "":
                    tree = etree.HTML(response.text)
                    data = tree.xpath(config[0]['title'])
                    text_content = [text.strip() for text in data if text.strip()]
                    if (len(data) > 0):
                        return text_content[0]
                    else:
                        pass
                        # print("---------------Title configration is invalid for: " + publisherName)
                else:
                    # print("-----title-----meta")
                    data = soup.find("meta", property="og:title")
                    if (data):
                            data = data['content']
                            if (data is not None):
                                data = fix_text(str(data))
                                return data

        else:
            # print("No configuration available -------title----------- getting from meta tags : " + publisherName)
            data = soup.find("meta", property="og:title")
            if (data):
                data = data['content']
                if (data is not None):
                    data = fix_text(str(data))
                    return data

    @classmethod
    def date_time(self,soup, response, config, publisherName):
        # print("No configuration available -------date----------- getting from meta tags : " + publisherName)
        # data = soup.find("meta", property="article:published_time")
        # if (data):
        #     data = data['content']
        #     if (data is not None):
        #         data = fix_text(str(data))
        #         return data
        if config != None and len(config) >= 1:
            if config[0]["date"] != None and config[0]["date"] != "":
                tree = etree.HTML(response.text)
                data = tree.xpath(config[0]['date'])
                # print("date", data)
                if len(data) > 0:
                    dates = []
                    for item in data:
                        matches = list(datefinder.find_dates(item))
                        if len(matches) > 0:
                            match = matches[0]
                            formatted_date = match.strftime('%Y-%m-%dT%H:%M:%S+P')
                    return formatted_date

                else:
                    print("---------------Date configration is invalid for: " + publisherName)
            else:
                data = soup.find("meta", property="article:published_time")
                if (data):
                    data = data['content']
                    if (data is not None):
                        data = fix_text(str(data))
                        return data

        else:
            # print("No configuration available -------date----------- getting from meta tags : " + publisherName)
            data = soup.find("meta", property="article:published_time")
            if (data):
                data = data['content']
                if (data is not None):
                    data = fix_text(str(data))
                    return data



    @classmethod
    def lang_detect(self, title,lang_name):
        text_content = f'{title}'
        if lang_name == 'Odiya':
            language=self.odiya_detection(text_content)
            return language
        elif lang_name == 'Sanskrit':
            return "Sanskrit"

        else :
        #         # _, _, detected_language, _ = cld.detect(text_content, returnVectors=True)
                # print('===============================================',detected_language)
                # # print(detected_language)
                # if detected_language[0][0] == 'ORIYA':
                #     detected_language = 'Odiya'
                #     return detected_language
                # else:
                #     return detected_language[0][0].capitalize()
                language_code = detect(text_content)
                language_names = {'en': 'English', 'hi': 'Hindi', 'bn': 'Bengali', 'gu': 'Gujarati', 'kn': 'Kannada',
                                  'ml': 'Malayalam', 'mr': 'Marathi', 'ne': 'Nepali', 'pa': 'Punjabi', 'ta': 'Tamil',
                                  'te': 'Telugu', 'ur': 'Urdu'}
                language_name = language_names.get(language_code, 'Unknown')
                return language_name


    @classmethod
    def odiya_detection(self,text):
        try:
            if text != None:
                    text_content = set()
                    for letter in text:
                        text_content.add(letter)
                    odia_vocab = {'ଅ', 'ଆ', 'ଇ', 'ଈ', 'ଉ', 'ଊ', 'ଋ', 'ୠ', 'ଌ', 'ୡ', 'ଏ', 'ଐ', 'ଓ', 'ଔ','କ', 'ଖ', 'ଗ', 'ଘ', 'ଙ', 'ଚ', 'ଛ', 'ଜ', 'ଝ', 'ଞ', 'ଟ', 'ଠ', 'ଡ', 'ଢ', 'ଣ','ତ', 'ଥ', 'ଦ', 'ଧ', 'ନ', 'ପ', 'ଫ', 'ବ', 'ଭ', 'ମ', 'ଯ', 'ର', 'ଲ', 'ଵ', 'ଶ','ଷ', 'ସ', 'ହ', 'ଳ', 'କ୍ଷ', 'ଜ୍ଞ'}
                    common_word=text_content.intersection(odia_vocab)
                    if common_word != None and common_word != set():
                        return "Odiya"
                    else:
                        language_code = detect(text)
                        language_names = {'en': 'English', 'hi': 'Hindi', 'bn': 'Bengali', 'gu': 'Gujarati', 'kn': 'Kannada',
                                          'ml': 'Malayalam', 'mr': 'Marathi', 'ne': 'Nepali', 'pa': 'Punjabi', 'ta': 'Tamil',
                                          'te': 'Telugu', 'ur': 'Urdu'}
                        language_name = language_names.get(language_code, 'Unknown')
                        return language_name
            else:
                 return "Unknown"
        except:

                return "Unknown"

    @classmethod
    def extract_description(self, soup, response, config, publisherName):
        if config != None and len(config) >= 1:
            print("----------------------description-------------------------")
            # if config[0]['fetchedByMetaTags'] == False or config[0]['fetchedByMetaTags'] == "":
            if config[0]["description"] != None and config[0]["description"] != "":
                tree = etree.HTML(response.text)
                data = tree.xpath(config[0]['description'])
                # print(data)
                modified_data = []

                for text in data:
                    text_content = text.strip()

                    if text_content:
                        # Check if the text has more than two words and does not start with a comma
                        if len(text_content.split()) >= 5 and not text_content.startswith(","):
                            modified_text = f'<p>{text_content}</p><br>'
                            modified_data.append(modified_text)
                        else:
                            print("==============================")
                            remove_word = "</p><br>"
                            if modified_data and modified_data[-1].endswith(remove_word):
                                modified_text = modified_data[-1][
                                                :-len(remove_word)].strip() + f'{text_content}</p><br>'
                                modified_data[-1] = modified_text

                result = ' '.join(modified_data)
                countWords = "Greater"
                if len(modified_data) > 0:
                    return result, countWords


                else:
                    print(f"----------------- Description configuration is invalid for {publisherName}")
                    data = soup.find("meta", property="og:description")
                    if (data):
                        data = data['content']
                        countWords = "Less"
                        if (data is not None):
                            data = fix_text(str(data))
                            # data = self.cleanText(data)
                            return data, countWords
            else:
                print("=====meta=========")
                data = soup.find("meta", property="og:description")
                if (data):
                    data = data['content']
                    countWords = "Less"
                    if (data is not None):
                        data = fix_text(str(data))
                        # data = self.cleanText(data)
                        return data, countWords

        else:
            # print("No configuration available ---------description--------- getting from meta tags")
            data = soup.find("meta", property="og:description")
            if (data):
                data = data['content']
                countWords = "Less"
                if (data is not None):
                    data = fix_text(str(data))
                    # data = self.cleanText(data)
                    return data, countWords

    @classmethod
    def extract_image(self, soup, response, config, publisherName):
        if config != None and len(config) >= 1:
            # if config[0]['fetchedByMetaTags'] == False or config[0]['fetchedByMetaTags'] == "":
                if config[0]["image"] != None:
                    tree = etree.HTML(response.text)
                    data = tree.xpath(config[0]['image'])
                    if (len(data) > 0):
                        # print("image configration is correct ------")
                        return data[0]
                    else:
                        print(f"----------------- image configration is invalid for {publisherName}")
                else:
                       data = soup.find("meta", property="og:image")
                       if (data):
                            data = data['content']
                            if "http" in data:
                                return data
                            else:
                                f"invalid image url: {data}"

            # else:
                # data = soup.find("meta", property="og:image")
                # if (data):
                #     data = data['content']
                #     if "http" in data:
                #         return data
                #     else:
                #         f"invalid image url: {data}"
        else:
            # print("No configuration available -------image----------- getting from meta tags")
            data = soup.find("meta", property="og:image")
            if (data):
                data = data['content']
                if "http" in data:
                    return data
                else:
                    f"invalid image url: {data}"

    @classmethod
    def getDharmawikiTitles(self):
        dharmawikiPostTitles = self.postRepository.getDharmaWikiPostTitles()
        return dharmawikiPostTitles

    @classmethod
    def constructDharmaWikiPostFromResponse(self, response):
        # print("--------------------------------",response)
        title = None
        externalPostId = None
        description = None
        content = None
        postRedirectUrl = None
        if response is not None and 'parse' in response:
            parse = response['parse']
            # print("------------------------------",parse['pageid'])
            # if 'pageid' in response:
            if 'pageid' in parse:
                externalPostId =parse['pageid']
                # externalPostId = response['pageid']
            if 'title' in parse:
                title = parse['title']
                postRedirectUrl = 'https://dharmawiki.org/index.php/' + title
                description = parse['title']
            if 'text' in parse:
                text = parse['text']
                if '*' in text:
                    content = text['*']
        categories = self.getPostCategoryByTitle(title, id)
        posterUrl = self.getPostImageByTitle(title)
        post = {"title": title, "description": description, "externalPostId": externalPostId, "content": content,
                'tags': categories, 'category': ', '.join(categories), "posterUrl": posterUrl,
                "postRedirectUrl": postRedirectUrl}
        # print('Constructed Post with title ' + post['title'] + ' category ' + post['category'])

        return post

    @classmethod
    def createDharmaWikiPost(self, response):
        posts = self.constructDharmaWikiPostFromResponse(json.loads(response))
        print(posts)
        self.postRepository.saveDharmaWikiPost(_encoder.encode(posts))

    @classmethod
    def getPostCategoryByTitle(self, title, id):
        categories = []
        response = self.postRepository.getPostCategoryByTitle(title)
        if response is not None and 'query' in response:
            query = response['query']
            if 'pages' in query:
                pages = query['pages']
                for key in pages.keys():
                    pageId = pages[key]
                    if 'categories' in pageId:
                        for category in pageId['categories']:
                            if 'title' in category:
                                newCategory = str(category['title']).replace('Category:', '')
                                categories.append(newCategory)
        return categories

    @classmethod
    def getPostImageByTitle(self, title):
        posterUrl = None
        response = self.postRepository.getPostImageByTitle(title)
        if response is not None and 'query' in response:
            query = response['query']
            if 'pages' in query:
                pages = query['pages']
                for key in pages.keys():
                    page = pages[key]
                    if 'imageinfo' in page and len(page['imageinfo']) > 0:
                        imageinfo = page['imageinfo'][0]
                        if 'url' in imageinfo:
                            posterUrl = imageinfo['url']

        return posterUrl



