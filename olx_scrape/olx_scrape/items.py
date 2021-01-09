# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OlxScrapeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #length = scrapy.Field()
    myear = scrapy.Field()
    bt = scrapy.Field()
    ft = scrapy.Field()
    km = scrapy.Field()
