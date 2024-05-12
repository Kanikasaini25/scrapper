import requests
import scrapy
from scrapy.utils.serialize import ScrapyJSONEncoder
_encoder = ScrapyJSONEncoder()
from market.constants import bse_data,Save_url,header




class PostServices:

    def _init_(self):
        pass


    @classmethod
    def SaveMarketData(self, mergeList):
        if mergeList:
            self.PostMarketData(_encoder.encode(mergeList))
        else:
            print('StatusList Not Found--------------------------------')




    @classmethod
    def PostMarketData(self, mergeList):
        print('=====Saving Data==================')
        print(mergeList)
        res = requests.post(Save_url, data=mergeList, headers=header)
        print(res.status_code)
        if res.status_code == 200:
            print('List Saved------------------')
        else:
            print('List Saving Error--------------------')
            raise scrapy.exceptions.DropItem("Failed to Save List")



    @classmethod
    def SaveBseData(self, mergeList):
        print('=====Saving Data==================')
        print(mergeList)
        res = requests.post(bse_data, data=mergeList, headers=header)
        print(res.status_code)
        if res.status_code == 200:
            print('List Saved------------------')
        else:
            print('List Saving Error--------------------')
            raise scrapy.exceptions.DropItem("Failed to Save List")




    @classmethod
    def EncodeBseData(self, mergeList):
        if mergeList:
            self.SaveBseData(_encoder.encode(mergeList))
        else:
            print('StatusList Not Found--------------------------------')