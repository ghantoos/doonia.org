#!/usr/bin/env python

from flask import Flask, request, render_template, redirect
from flask.ext.mongoengine import MongoEngine
from flask.ext.mail import Mail, Message
from flask.ext.script import Manager
from models import Khabar
from functions import *
from flask_debugtoolbar import DebugToolbarExtension

from mongoengine import *
from datetime import datetime, timedelta

# init app
app = Flask(__name__)
app.config.from_pyfile('config/doonia.conf')

# add debugging toolbar
if app.config['MONGODB_DEBUG_TOOLBAR']:
  toolbar = DebugToolbarExtension(app)

# init mongodb plugin
db = MongoEngine(app)

# init mail plugin
mail = Mail(app)

# init manager plugin
manager = Manager(app)

@app.route('/<language>/<country>/<category>/')
def doonia(language='en', category='alaune', country=None):
  # get items that are maximum 3 days old, and order by date
  twodaysago = datetime.now() - timedelta(days=3)

  # get domain list for scrapy config instead of the
  # mongo db. This way we can control the out from the csv file
  domains = listdomains(app.config['SCRAPY_CSV'])

  # set the limit of articles per page, per column
  limit        = app.config['PER_COLUMN_LIMIT']
  limit_mob = app.config['MOBILE_PER_COLUMN_LIMIT']

  # only show listed countries
  countries    = app.config['COUNTRY_LIST']

  # get the minimum limit to show column
  column_min   = app.config['PER_COLUMN_MIN']

  # get article description size
  desc_size = app.config['DESC_SIZE']

  # get grid size
  gridsize = app.config['GRID_SIZE']

  # get language settings
  langset  = app.config['LANGUAGES']

  # get navbar categories
  navbar   = app.config['NAVBAR']

  if language not in langset or category not in navbar \
        or country not in countries:
    return ''

  # get list of articles sorted by pubdate - for large screens
  articles = {}
  if domains.has_key(country):
    for domain in domains[country].keys():
      articles[domain] = Khabar.objects( country      = country,
                                         category     = category,
                                         domain       = domain,
                                       ).order_by('-date', '-pubdate').limit(limit)

  # get list of articles sorted by pubdate - for mobiles
  articles_mob = Khabar.objects( country      = country,
                                 category     = category,
                                 pubdate__gte = twodaysago,
                               ).order_by('-pubdate')

  # calculate number of columns
  columns = len(articles.values())
  for col in articles.values():
    if len(col) < app.config['PER_COLUMN_MIN']:
      columns -= 1

  # calculate css column properties
  if columns > app.config['PER_COLUMN_MIN']:
    css_props = css_columns(gridsize, columns)
  else:
    # if country is not published
    css_props = {}

  try:
    domains_cnt = domains[country]
  except KeyError:
    domains_cnt = {None:None}

  return render_template( 'newsfeed.html', 
                          country      = country,
                          category     = category,
                          articles     = articles,
                          articles_mob = articles_mob,
                          navbar       = navbar,
                          navbar_order = app.config['NAVBAR_ORDER'],
                          column_min   = column_min,
                          limit_mob    = limit_mob,
                          css_props    = css_props,
                          countries    = countries,
                          langset      = langset,
                          desc_size    = desc_size,
                          language     = language )

@app.route('/feedback/', methods=['GET','POST'])
def feedback():
      if request.method == 'POST':
        # init message
        msg = Message(subject    = "New feedback comment",
                      sender     = app.config['EMAIL_FROM'],
                      recipients = app.config['EMAIL_TO'])

        # build the message body
        msg.body = "Subject: %s\nEmail: %s\nReferrer: %s\nMessage:\n%s" \
                      %( request.form['subject'],
                         request.form['email'],
                         request.referrer,
                         request.form['message'])
        # send the email
        mail.send(msg)

        # redirect to referrer
        return redirect(request.referrer)
      elif request.method == 'GET':
        return ''

@app.route('/status/', methods=['GET'])
def status():
  if request.method == 'GET':
    return 'OK running'

if __name__ == '__main__':
  manager.run()
