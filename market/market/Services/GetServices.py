from market.constants import headers, url
from lxml import etree
import requests
import json
from bs4 import BeautifulSoup

class MarketDataService:

    def _init_(self):
        pass



    @classmethod
    def GetMarketData(self):
        print('=====Getting Data==================')
        res = requests.get(url, headers=headers)
        # print("========",res.status_code)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'html.parser')
            script_tag = soup.find('script', text=lambda t: t and 'window.headerData' in t)
            if script_tag:
                start_index = script_tag.text.find('{')
                end_index = script_tag.text.rfind('}') + 1
                header_data = script_tag.text[start_index:end_index]
                return json.loads(header_data)
            else:
                print('Error: window.headerData not found in the HTML content.')
        else:
            print('Error: Failed to retrieve data from the API.')



    @classmethod
    def BseTopGainers(self, bse_Gainer):
        res = requests.get(bse_Gainer)
        print(res.status_code)
        topGainers = []
        if res.status_code == 200:
            tree = etree.HTML(res.text)
            names = tree.xpath("//td//span[@class='gld13 disin']//a[1]/@title")
            prices = tree.xpath('//tbody//tr/td[4]/text()')
            changes = tree.xpath('//tbody//tr/td[7]/text()')
            for name, price, change in zip(names, prices, changes):
                topGainersObject = {
                    'symbol': name.replace('.', ''),
                    'lastPrice': price,
                    'pChange': change,
                    'type': "topGainers"
                }
                topGainers.append(topGainersObject)
            return topGainers
        else:
            print('Exception ===========')



    @classmethod
    def BseTopLosers(self, bse_Loser):
        res = requests.get(bse_Loser)
        topLosers = []

        if res.status_code == 200:
            tree = etree.HTML(res.text)
            names = tree.xpath("//td//span[@class='gld13 disin']//a[1]/@title")
            prices = tree.xpath('//tbody//tr/td[4]/text()')
            changes = tree.xpath('//tbody//tr/td[7]/text()')
            for name, price, change in zip(names, prices, changes):
                topLoserObject = {
                    'symbol': name.replace('.', ''),
                    'lastPrice': price,
                    'pChange': change,  # doubt
                    'type': "topLosers"
                }
                topLosers.append(topLoserObject)
            return topLosers
        else:
            print('Exception ==============================')