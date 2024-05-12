import os

PublishersAPI = 'https://crawler.ritamdigital.org/services/crawler/api/publishers?page=0&size=10000'
Publisher_URL = 'https://crawler.ritamdigital.org/services/crawler/api/publishers/languages?language={}&size=10000'
ArticlesAPI = 'https://crawler.ritamdigital.org/services/crawler/api/articlelinks/publisher/{}'
Save_postAPI = 'https://crawler.ritamdigital.org/services/crawler/api/posts/external/news-feeds'
Remove_postAPI = 'https://crawler.ritamdigital.org/services/crawler/api/articlelinks/{}'
Save__DHARMAWIKIpostAPI = 'https://crawler.ritamdigital.org/services/crawler/api/posts/external/dharmaWikiPost'
# AUTH_URL = 'http://{}:{}/api/authenticate'
DHARMAWIKI_POSTS_TITLE_URL = 'https://crawler.ritamdigital.org/services/crawler/api/dhama-wiki-articles'
DHARMAWIKI_GET_ARTICLE_URL = 'https://dharmawiki.org/api.php?action=parse&page={}&format=json'
DHARMAWIKI_GET_ARTICLE_CATEGORY_URL = 'https://dharmawiki.org/api.php?action=query&format=json&titles={}&prop=categories'
DHARMAWIKI_GET_ARTICLE_IMAGE_URL = 'https://dharmawiki.org/api.php?action=query&generator=images&titles={}&prop=imageinfo&&iiprop=url&iiurlwidth=220&format=json'
SewaGatha='https://www.sewagatha.org/api/v1/news?publish=true&limit=6&page=1'

def getHeaders():
    return {'Content-Type': 'application/json'}

HEADERS = {
    'Content-type': 'application/json'
}

def getCredentials():
    return {
        'username': os.environ['USERNAME'],
        'password': os.environ['PASSWORD']
    }
