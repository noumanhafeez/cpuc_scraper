# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CpucItem(scrapy.Item):
    # define the fields for your item here like:
    # define the fields for your item here like:
    title = scrapy.Field()
    doc_type = scrapy.Field()
    doc_path = scrapy.Field()
    doc_link = scrapy.Field()
    filed_by = scrapy.Field()
    industry = scrapy.Field()
    filling_date = scrapy.Field()
    category = scrapy.Field()
    status = scrapy.Field()
    description = scrapy.Field()
    alj = scrapy.Field()
    commissioner = scrapy.Field()
    