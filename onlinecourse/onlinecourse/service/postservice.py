
from lxml import etree
from scrapy.utils.serialize import ScrapyJSONEncoder

from onlinecourse.repository.post_repository import PostRepository
_encoder = ScrapyJSONEncoder()

class PostService:
    postRepository = PostRepository()

    @classmethod
    def getOnlineCoursePlaylist(self):
        OnlineCourseList = self.postRepository.getOnlineCoursePlaylist()
        return OnlineCourseList

    def saveOnlineCourseData(self, OnlineCourseList):
        if OnlineCourseList:
            self.postRepository.saveOnlineCourseList(_encoder.encode(OnlineCourseList))

        else:
            print('Online Course Api Not Found--------------------------------')

