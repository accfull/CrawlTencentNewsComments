# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item,Field

class NewsItem(Item):
    source = Field()
    date = Field()
    newsId = Field()
    cmtId = Field()
    contents = Field()
    comments = Field()

