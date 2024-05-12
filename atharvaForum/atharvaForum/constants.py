import os

AUTH_URL = 'http://crawler.ritamdigital.org/api/authenticate'
ATHRVA_FORUM_GET_PLAYLIST = 'http://crawler.ritamdigital.org/services/crawler/api/atharvaPlaylist'
ATHRVA_FORUM_POST_VIDEO = 'http://crawler.ritamdigital.org/services/crawler/api/posts/external/athravaFurum/list'

API_KEY = 'AIzaSyBQhimNGSF4jNFHrX782Njh_-dTLwLX53U'
YOUTUBE_BASE_URL = 'https://www.youtube.com'

DATE_FORMAT = 'd MMM yyyy HH:mm:ss zzz'


def getHeaders():
    return {'Content-Type': 'application/json'}

def getAuthorizationToken(token):
    return {'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(token)
            }

HEADERS = {
    'Content-type': 'application/json',
    'Authorization': 'Bearer '
}

def getCredentials():
    return {
        'username': os.environ['USERNAME'],
        'password': os.environ['PASSWORD']
    }