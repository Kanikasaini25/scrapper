import os

Publisher_URL = 'https://crawler.ritamdigital.org/services/crawler/api/publishers?size=10000'
Publisher_URL_ID = 'https://crawler.ritamdigital.org/services/crawler/api/publishers/{}?page=0&size=500'
ARTICLE_URL = 'https://crawler.ritamdigital.org/services/crawler/api/articlelinks/saveList'
AUTH_URL = 'https://crawler.ritamdigital.org/api/authenticate'
DHARMAWIKI_GET_TITLE_URL = 'https://dharmawiki.org/api.php?action=query&list=allpages&format=json&aplimit=500'
DHARMAWIKI_SAVE_TITLE_URL = 'https://crawler.ritamdigital.org/services/crawler/api/dhamaWikiArticle/saveList'
DHARMAWIKI_GET_TITLE_URL_WITH_APCONTINUE = 'https://dharmawiki.org/api.php?action=query&list=allpages&format=json&aplimit=500&apcontinue={}'


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
