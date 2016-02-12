# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import pymongo

from scrapy.exceptions import DropItem
from scrapy.conf import settings
from scrapy import log


class DooniaPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoDBPipeline(object):
  def __init__(self):
    connection = pymongo.Connection(settings['MONGODB_SERVER'],
                                    settings['MONGODB_PORT'])
    self.db = connection[settings['MONGODB_DB']]
   
  def process_item(self, item, spider):
    valid = True
    collection = self.db[settings['MONGODB_COLLECT_PRODUCTION']]
    collection_archive = self.db[settings['MONGODB_COLLECT_ARCHIVE']]
    for data in item:
      # here we only check if the data is not null
      # but we could do any crazy validation we want
      if not data:
        valid = False
        raise DropItem("Missing %s info from %s" %(data, item['source']))
    if valid:
      dicitem = dict(item)

      # fill all new RSS items in collection
      collection.update({'source'  : '%s' % dicitem['source'],
                         'link'    : '%s' % dicitem['link'],
                         'category': '%s' % dicitem['category'],
                         'country' : '%s' % dicitem['country'],
                         'lang'    : '%s' % dicitem['lang']},
                         dict(item), upsert=True)
      log.msg("Item wrote to MongoDB database %s/%s" %
              (settings['MONGODB_DB'], settings['MONGODB_COLLECT_PRODUCTION']),
              level=log.DEBUG, spider=spider)

      # archive all the RSS items to the _archive collection
      collection_archive.update({ 'source':'%s' % dicitem['source'], 
                          'link':'%s' % dicitem['link']}, 
                          dict(item), upsert=True)
      log.msg("Item wrote to MongoDB database %s/%s" %
              (settings['MONGODB_DB'], settings['MONGODB_COLLECT_ARCHIVE']),
              level=log.DEBUG, spider=spider)

    return item
