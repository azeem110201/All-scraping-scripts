#E:\scrapy\olx_scrape\cardekho.csv
import scrapy
from ..items import OlxScrapeItem

base_url = "https://www.cardekho.com/api/v1/usedcar/search?&cityId=338&connectoid=befa0b91-eb33-81d8-7eee-f6df4425d37e&sessionid=fa5eca1f8fb841d073761ec725dcc63a&lang_code=en&regionId=0&searchstring=used-cars%2B0-lakh-to-50-lakh%2Bin%2Bkolkata&pagefrom={}&sortby=updated_date&sortorder=asc&mink=0&maxk=200000&dealer_id=&regCityNames=&regStateNames="
class OlxSpider(scrapy.Spider):
    name = 'olx'
    start_urls = [
        base_url.format(40)
    ]

    def parse(self, response):
        data = response.json()

        for i in range(len(data['data']['cars'])):
            yield data['data']['cars'][i]

        current_page = data['data']['from']

        if data['data']['from'] and len(data['data']['cars']) != 0:
            next_page_url = base_url.format(current_page+1)
            yield scrapy.Request(next_page_url)
