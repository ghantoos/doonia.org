""" Functions used by the doonia webserver """

import csv
from urlparse import urlparse

def listdomains(csvfile):
  """ Returns a dict of domains by cournty """
  domains = {}
  for line in csv.reader(open(csvfile, "rb"), delimiter=','):
    # if line is not empty, and no commented
    if len(line) == 5 and not line[0].startswith('#') and line[0]:
      # columns 1: country
      country    = line[0].strip()

      # column 2: category list
      categories = line[1].split(',')

      # column 3: rss domain; strip only domain name
      domain      = urlparse(line[2].strip()).netloc

      # column 4: feed language
      lang     = line[3].strip()

      # init dict by country
      if not domains.has_key(country):
        domains[country] = {}

      # build dict with domain, language, and categories by country
      if not domains[country].has_key(domain):
        domains[country][domain] = {'domain'    : domain,
                                    'lang'      : lang,
                                    'categories': [] }

      # insert categories in category list by domain
      for category in categories:
        category = category.strip()
        if category not in domains[country][domain]['categories']:
          domains[country][domain]['categories'].append(category)

  return domains

def css_columns(gridsize, columns):
  """ returns a dict of 3 values containing:
        - the size of the left empty column
        - the size of each news feed column
        - the size of the the right empty column
  """
  NUM = {
    0  : '',
    1  : 'one',
    2  : 'two',
    3  : 'three',
    4  : 'four',
    5  : 'five',
    6  : 'six',
    7  : 'seven',
    8  : 'eight',
    9  : 'nine',
    10 : 'ten',
    11 : 'eleven',
    12 : 'twelve',
    13 : 'thirteen',
    14 : 'fourteen',
    15 : 'fifteen',
    16 : 'sixteen',
    17 : 'seventeen',
    18 : 'eighteen',
    19 : 'nineteen',
    20 : 'twenty',
    21 : 'twentyone',
    22 : 'twentytwo',
    23 : 'twentythree',
    24 : 'twentyfour',
    25 : 'twentyfive',
    26 : 'twentysix',
    27 : 'twentyseven',
  }

  # set left margin to one column
  left  = 1

  # calculate with minumum 2 columns for the margins (left + right)
  feed  = (gridsize - 2) / columns

  # put what's rest in the right margin
  right = gridsize - columns * feed - left

  return {'right': NUM[right],
          'left' : NUM[left],
          'feed' : NUM[feed]
         }
