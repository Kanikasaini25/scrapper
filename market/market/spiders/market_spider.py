import time
import scrapy
from market.Services.GetServices import  MarketDataService
from market.Services.PostService import PostServices
from market.constants import Save_url,bse_Loser,bse_Gainer




class MarketSpider(scrapy.Spider):
    name = "market_spider"
    MarketDataService = MarketDataService()
    PostServices =PostServices()

    def start_requests(self):
        try:
            while True:
                print("slepping time-----")

                time.sleep(1*60)
                data = self.MarketDataService.GetMarketData()
                print(data)
                topLosers = set()
                topGainers = set()
                topVolume = set()
                topValue = set()
                mergeList = []

                for res in data['indexDataInfo']:
                    timestamp = res['timestamp']
                    for key, value in res.items():
                        if key == 'topLosers':
                            for element in value['data']:
                                identifier = element['identifier']
                                if identifier not in topLosers:
                                    topLosers.add(identifier)
                                    mergeList.append({
                                        'symbol': element['symbol'],
                                        'identifier': identifier,
                                        'lastPrice': element['lastPrice'],
                                        'pChange': element['pChange'],
                                        'totalTradedVolume': element['totalTradedVolume'],
                                        'totalTradedValue': element['totalTradedValue'],
                                        "timestamp": timestamp,
                                        'type': 'topLosers'
                                    })
                        elif key == 'topGainers':
                            for element in value['data']:
                                identifier = element['identifier']
                                if identifier not in topGainers:
                                    topGainers.add(identifier)
                                    mergeList.append({
                                        'symbol': element['symbol'],
                                        'identifier': identifier,
                                        'lastPrice': element['lastPrice'],
                                        'pChange': element['pChange'],
                                        'totalTradedVolume': element['totalTradedVolume'],
                                        'totalTradedValue': element['totalTradedValue'],
                                        "timestamp": timestamp,
                                        'type': 'topGainers'
                                    })
                        elif key == 'topVolume':
                            for element in value['data']:
                                identifier = element['identifier']
                                if identifier not in topGainers:
                                    topVolume.add(identifier)
                                    mergeList.append({
                                        'symbol': element['symbol'],
                                        'identifier': identifier,
                                        'lastPrice': element['lastPrice'],
                                        'pChange': element['pChange'],
                                        'totalTradedVolume': element['totalTradedVolume'],
                                        'totalTradedValue': element['totalTradedValue'],
                                        "timestamp": timestamp,
                                        'type': 'topVolume'
                                    })
                        elif key == 'topValue':
                            for element in value['data']:
                                identifier = element['identifier']
                                if identifier not in topGainers:
                                    topValue.add(identifier)
                                    mergeList.append({
                                        'symbol': element['symbol'],
                                        'identifier': identifier,
                                        'lastPrice': element['lastPrice'],
                                        'pChange': element['pChange'],
                                        'totalTradedVolume': element['totalTradedVolume'],
                                        'totalTradedValue': element['totalTradedValue'],
                                        "timestamp": timestamp,
                                        'type': 'topValue'
                                    })

                self.PostServices.SaveMarketData(mergeList)

        except Exception as e:
            print(f"Exception: {str(e)}")





class BseDataSpider(scrapy.Spider):
    name = "BseDataSpider"
    MarketDataService = MarketDataService()
    PostServices = PostServices()



    def start_requests(self):
        try:
            while True:
                print("slepping time-----")
                time.sleep(1*60)

                topGainer=self.MarketDataService.BseTopGainers(bse_Gainer)
                topLoser= self.MarketDataService.BseTopLosers(bse_Loser)
                mergeList= topLoser+topGainer
                self.PostServices.EncodeBseData(mergeList)


        except Exception as e:
            print(f"Exception: {str(e)}")


