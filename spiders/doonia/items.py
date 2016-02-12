# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field


class RSSItem(Item):
    title       = Field()
    link        = Field()
    description = Field()
    img         = Field()
    date        = Field()
    pubdate     = Field()
    source      = Field()
    domain      = Field()
    country     = Field()
    category    = Field()
    lang        = Field()
