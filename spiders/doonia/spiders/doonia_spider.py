import csv
from scrapy import log
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.conf import settings
from scrapy.exceptions import CloseSpider
from datetime import datetime
from dateutil import parser
from urlparse import urlparse
from re import sub
from doonia.items import RSSItem
import feedparser
import socket

class DooniaSpider(BaseSpider):
  name = "doonia"

  def __init__(self, start_urls_file=None, **kwargs):
    """ add argument to set url list file """
    # start logging
    log.start( logfile=settings['LOG_FILE'],
               loglevel=settings['LOG_LEVEL'],
               logstdout=None )

    if start_urls_file:
      self.start_urls_file = start_urls_file
      self.urls = {}

    # get date as UID
    self.date = datetime.now().strftime("%Y%m%d-%H:%M:%S.%f")

    # set request timeout
    socket.setdefaulttimeout(60)

  def start_requests(self):
    """ Read RSS urls from start_urls_file file"""
    for line in csv.reader(open(self.start_urls_file, "rb"), delimiter=','):
      if len(line) >= 3 and not line[0].startswith('#') and line[0]:
        self.urls[line[2].strip()] = { 'country' :line[0].strip(), 
                                       'category':line[1].split(','),
                                       'lang'    :line[3].strip()}
        yield Request(line[2].strip(), self.parse)

  def parse(self, response):
    # log url scraping start
    log.msg("Processing '%s' starting in category list %s" \
              % ( response.url, self.urls[response.url]['category']),
              level=log.WARNING)

    # parse feed
    feed = feedparser.parse(response.url)

    # initialize item list
    articles = []

    # set the crawling starting point
    items = feed['entries']

    for item in items:
      for cat in self.urls[response.url]['category']:
        # initialize article
        article = RSSItem()

        # get content if article
        for key in ['title', 'link', 'image']:
          if item.has_key(key):
            article[key] = item[key]

        if item.has_key('description'):
          # get description, and strip extra html tags
          article['description'] = sub('<.*?>','', item['description'])
        else: article['description'] = ''

        # get published date
        article['pubdate'] = ''
        for key in ['updated', 'pubdate', 'published']:
          if item.has_key(key):
            article['pubdate'] = parser.parse(item[key], fuzzy=True)
            break

        article['date']     = self.date
        article['domain']   = urlparse(response.url).netloc
        article['source']   = response.url
        article['country']  = self.urls[response.url]['country']
        article['lang']     = self.urls[response.url]['lang']

        # put result for all categories
        article['category'] = cat.strip()

        # append results to the articlelist
        articles.append(article)

    # log url scraping end
    log.msg("Processing '%s' finished" % response.url, level=log.WARNING)

    return articles

  def lts(self, item):
    """ keep list's first item """
    if type(item) is list and len(item) > 0:
      return item[0].strip()
    else:
      return item

SPIDER = DooniaSpider()
