# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class BookItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
    exc_tax = scrapy.Field()
    inc_tax = scrapy.Field()
    availability = scrapy.Field()
    reviews = scrapy.Field()
    img_url = scrapy.Field()
    rating = scrapy.Field()

    #Metadata
    _id = scrapy.Field()
    url = scrapy.Field()
    crawl_date = scrapy.Field()
    status = scrapy.Field()

