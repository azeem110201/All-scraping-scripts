import scrapy

base_url = "https://cricketapi-icc.pulselive.com/fixtures?matchTypes=OTHER%2CT20I%2CT20%2CTEST%2CODI%2CFIRST_CLASS%2CLIST_A&tournamentTypes=I%2CWI&teamTypes=b%2Cm&matchStates=C&page={}&pageSize=20&sort=desc"
class ImagescraperSpider(scrapy.Spider):
    name = 'imagescraper'
    start_urls = [
        base_url.format(0)
    ]

    def parse(self, response):
        data = response.json()
        for i in range(20):
            yield data['content'][i]
        current_page = data['pageInfo']['page']
        
        if data['pageInfo']['numPages']:
            next_page_url = base_url.format(current_page+1)
            yield scrapy.Request(next_page_url)


