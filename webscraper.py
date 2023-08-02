from urllib.request import urlopen
import json

class DnDCharacterScraper:
    def __init__(self, urls):
        self.urls = urls
        
    def getCurrentHP(self):
        ret = []
        for url in self.urls:
            response = urlopen(url)
            data_json = json.loads(response.read())
            ret.append(data_json)
        return ret