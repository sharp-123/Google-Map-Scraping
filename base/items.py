# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BaseItem(scrapy.Item):
    # define the fields for your item here like:
    Title  = scrapy.Field()
    Reviews  = scrapy.Field()
    Address  = scrapy.Field()
    Website  = scrapy.Field()
    Phone  = scrapy.Field()
    PlusCode  = scrapy.Field()
    Monday  = scrapy.Field()
    Tuesday  = scrapy.Field()
    Wednesday  = scrapy.Field()
    Thursday  = scrapy.Field()
    Friday  = scrapy.Field()
    Saturday  = scrapy.Field()
    Sunday = scrapy.Field()
    
    
