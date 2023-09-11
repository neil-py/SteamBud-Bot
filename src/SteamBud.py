import requests
import stores
import re
from urllib.parse import unquote
from stores import StoreLookUp


class SearchAPI():

    def __init__(self):
        self.url_endpoint = "https://www.cheapshark.com/api/1.0/"
        self.headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        'content-type': "application/json",
		'connection': "keep-alive"
    }
        self.StoreLookup = StoreLookUp()

    def __cheapDealSearchID(self,deal_id) -> tuple:
        req_get_store_id = requests.get(f"{self.url_endpoint}deals", 
                                        headers=self.headers,
                                        params ={
                                            'id': unquote(deal_id)
                                        }
                                        )
        json_respons = req_get_store_id.json()
        store_id = json_respons['gameInfo']['storeID']

        deal_link = f"https://cheapshark.com/redirect?dealID={deal_id}&k=1"

        return store_id, deal_link
    
    def __steam(self, steamappid) -> list:

        req = requests.get(f"{self.url_endpoint}games", 
                           headers=self.headers,
                           params={
                               'steamAppID': steamappid
                           }
                           )

        info_response = []

        for g in req.json():
            game_title = g['external']
            cheapest_price = g['cheapest']
            cheapest_deal_id = g['cheapestDealID']
            game_thumbnail = g['thumb']

            #endpoint for taking info about cheapest deal
            deal_search = self.__cheapDealSearchID(cheapest_deal_id)
            store_id = deal_search[0]
            deal_redirect_link = deal_search[1]

            game_data = {
                'game_title': game_title,
                'cheapset_price': cheapest_price,
                'cheapest_store': self.StoreLookup.lookup_req(int(store_id)-1)['storeName'],
                'thumbnail': game_thumbnail,
                'deal_link': deal_redirect_link
                        }
            info_response.append(game_data)

        return info_response

    
    def generalSearch(self, game_name, amount=0) -> list:
        
        game = game_name.replace(" ", "%20")
        req = requests.get(f"{self.url_endpoint}games", 
                           headers=self.headers,
                           params={
                               'title': unquote(game)
                           }
                           )

        info_response = []
        count = 0

        for g in req.json():
            if amount != 0 and count >= amount:
                break
            elif amount == 0 and count >= 10:
                break
            game_id = g['gameID']
            game_title = g['external']
            cheapest_price = g['cheapest']
            cheapest_deal_id = g['cheapestDealID']
            game_thumbnail = g['thumb']

            deal_search = self.__cheapDealSearchID(cheapest_deal_id)
            store_id = deal_search[0]
            deal_redirect_link = deal_search[1]

            game_data = {
                'gameID': game_id,
                'game_title': game_title,
                'cheapset_price': cheapest_price,
                'cheapest_store': self.StoreLookup.lookup_req(int(store_id)-1)['storeName'],
                'cheapest_store_banner': f"https://www.cheapshark.com{self.StoreLookup.lookup_req(int(store_id)-1)['images']['banner']}",
                'thumbnail': game_thumbnail,
                'deal_link': deal_redirect_link
                        }
            info_response.append(game_data)
            count+=1

        return info_response
    
    
    def finddeals(self, game_id, amount=0) -> dict:

        req = requests.get(f"{self.url_endpoint}games", 
                           headers=self.headers,
                           params={
                               'id': game_id
                           }
                           )
        game_info = req.json()
        
        game_title = game_info['info']['title']
        store_id = 0
        deal_redirect_link = ""
        game_thumbnail = game_info['info']['thumb']
        savings = 0
        count = 0

        game_data = {'game_title': game_title, 'thumbnail': game_thumbnail, 'other_deals': []}
        for deals in game_info['deals']:
            if amount != 0 and count > 10:
                break
            if count < 10:
                if count==0:
                    game_data['cheapest_price'] = deals['price']
                    deal_search = self.__cheapDealSearchID(deals['dealID'])
                    store_id = deal_search[0]
                    link = f"https://www.cheapshark.com{self.StoreLookup.lookup_req(int(store_id)-1)['images']['banner']}"
                    game_data['cheapest_store_banner'] =  link
                    game_data['cheapest_store'] = self.StoreLookup.lookup_req(int(store_id)-1)['storeName']
                    game_data['deal_link'] = deal_search[1]
                    savings = deals['savings']
                    game_data['savings'] = int(float(savings))
                    
                else:
                    deal_search = self.__cheapDealSearchID(deals['dealID'])
                    store_id = deal_search[0]
                    deal_redirect_link = deal_search[1]
                    deal_saving =  deals['savings']
                    link_1 = f"https://www.cheapshark.com{self.StoreLookup.lookup_req(int(store_id)-1)['images']['logo']}"
                    game_data['other_deals'].append(
                        {
                            'store': self.StoreLookup.lookup_req(int(store_id)-1)['storeName'],
                            'price': deals['price'],
                            'deal_link': deal_redirect_link,
                            'store_thumb': link_1,
                            'savings': int(float(deal_saving))
                        }
                    )
            count+=1

        return game_data
    
    def dealsLookUp(self, storeID, lowerPrice=None, upperPrice=None) -> dict:
        deal_loop_up_req = requests.get(
            url=f"{self.url_endpoint}deals",
            headers=self.headers,
            params={
                'storeID': storeID,
                'lowerPrice': lowerPrice,
                'upperPrice': upperPrice
            }
        )
        top_deals = []
        count=0
        json_response = deal_loop_up_req.json()
        while count <= 9:
            deal = json_response[count]
            game_title = deal['title']
            sale_price = deal['salePrice']
            savings = deal['savings']
            thumbnail = deal['thumb']
            dealID = deal['dealID']
            storeID = deal['storeID']
            deal_data = {
                'game_title': game_title,
                'sale_price': sale_price,
                'savings': int(float(savings)),
                'thumb': thumbnail,
                'deal_link': self.__cheapDealSearchID(dealID)[1]
            }
            top_deals.append(deal_data)
            count+=1

        return {
            'store_name': self.StoreLookup.lookup_req(int(storeID)-1)['storeName'],
            'store_banner': f"https://www.cheapshark.com{self.StoreLookup.lookup_req(int(storeID)-1)['images']['banner']}",
            'deals': top_deals
        }
    
    def steamID(self, steamID) -> dict:
        return self.__steam(steamID)
    
    def steamlink(self, steamlink) -> dict:
        parse_steam_link = re.findall("\d+", steamlink)[0]
        return self.__steam(parse_steam_link)

    def available_stores(self) -> list:
        available_stores = []
        req = requests.get(f"{self.url_endpoint}stores", headers=self.headers)
        for store in req.json():
            if store['isActive'] == 1:
                available_stores.append(store)
        return available_stores
    