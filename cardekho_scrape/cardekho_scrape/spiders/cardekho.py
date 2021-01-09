import scrapy
import pandas as pd


base_url = "https://www.cardekho.com/api/v1/usedcar/recommendation?&cityId=8&connectoid=befa0b91-eb33-81d8-7eee-f6df4425d37e&sessionid=fa5eca1f8fb841d073761ec725dcc63a&lang_code=en&regionId=0&usedcarid={}"
class CardekhoSpider(scrapy.Spider):
    name = 'cardekho'
    start_urls = [
        base_url.format(2890172)
    ]

    def __init__(self):
        self.data = pd.read_csv("cardekho.csv")

    def getData(self, index):
        return self.data['ucid'][index]

    def getShape(self):
        return self.data.shape[0]    

    def parse(self, response):
        data = response.json()

        for i in range(len(data['data'])):
            yield data['data'][i]

        current_page = self.getData(0)

        if current_page:
            for i in range(1, self.getShape()):
                next_page_url = base_url.format(self.getData(i))
                yield scrapy.Request(next_page_url)