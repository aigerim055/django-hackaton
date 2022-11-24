# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    genre = scrapy.Field()
    slug = scrapy.Field()
    # slug = scrapy.Field()