
from lxml import etree
from scrapy.utils.serialize import ScrapyJSONEncoder

from atharvaForum.repository.post_repository import PostRepository
_encoder = ScrapyJSONEncoder()

class PostService:
    postRepository = PostRepository()

    @classmethod
    def getAtharvaPlaylist(self):
        athravaForumList = self.postRepository.getAtharvaForumPlaylist()
        return athravaForumList

    def saveAtharvaForumData(self, athravaList):
        if athravaList:
            self.postRepository.saveAthravaForumList(_encoder.encode(athravaList))

        else:
            print('Atharva Forum Api Not Found--------------------------------')

