
from lxml import etree
from scrapy.utils.serialize import ScrapyJSONEncoder
import datetime


from urlscrapper.repository.post_repository import PostRepository
_encoder = ScrapyJSONEncoder()

class PostService:
    postRepository = PostRepository()

    @classmethod
    def extractUrl(self, response, config, publisherId, publisherName, region):
        articleList = []
        urlList = []
        tree = etree.HTML(response.text)
        urls = tree.xpath(config['xpath'])
        # print('urls----------------' + publisherName)
        # print(urls)
        baseUrl = config['baseUrl']
        if(len(urls) > 0):
            for url in urls:
                if baseUrl is not None:
                    url = baseUrl + url
                if 'http' in url:
                    if not urlList.__contains__(url):
                        article = {
                            'url': url,
                            'category': config['categoryName'],
                            'publisherId': publisherId,
                            'region': region,
                        }
                        urlList.append(url)
                        articleList.append(article)

                else:
                    print('---invalid url for publisher: ' + publisherName)
        print('articleList')
        print(len(articleList))
        return articleList

    @classmethod
    def parseFromService(self, response):
        config = response.meta['config']
        publisherId = response.meta['publisherId']
        publisherName = response.meta['publisherName']
        regions = response.meta['regions']
        articlesUrls = self.extractUrl(response, config, publisherId, publisherName, regions)

        if articlesUrls:
            self.postRepository.savePost(_encoder.encode(articlesUrls))
            print('Saved ' + str(len(articlesUrls)) + ' for publisher ' + publisherName+ ' at ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        else:
            print('no articles link found for publisher ' + publisherName)

    @classmethod
    def getDharmawikiTitles(self):
        dharmawikiPostTitles = self.postRepository.getDharmawikiPostTitles()
        return dharmawikiPostTitles

    @classmethod
    def getDharmawikiTitlesWithApContinue(self, apContinue):
        dharmawikiPostTitles = self.postRepository.getDharmawikiPostTitlesWithApContinue(apContinue)
        return dharmawikiPostTitles

    @classmethod
    def saveDharmawikiTitleList(self, dharmawikiTitles):
        if dharmawikiTitles:
            self.postRepository.saveDharmawikiTitleList(_encoder.encode(dharmawikiTitles))

        else:
            print('Dharmawiki Titles Not Found--------------------------------')

