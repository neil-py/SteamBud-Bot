import requests

class StoreLookUp:
    def __init__(self):
        self.headers={
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            'content-type': "application/json",
            'connection': "keep-alive"
        }

    def lookup_req(self, index) -> list:
       store_lookUp_req = requests.get("https://www.cheapshark.com/api/1.0/stores", headers=self.headers).json()
       return store_lookUp_req[index]