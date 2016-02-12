# Scrapy settings for doonia project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'doonia'

SPIDER_MODULES = ['doonia.spiders']
NEWSPIDER_MODULE = 'doonia.spiders'

# Crawl responsibly by identifying yourself (and your website) on the
# user-agent
# USER_AGENT = 'doonia (+http://www.yourdomain.com)'

# log settings
LOG_FILE  = "log/scrapy.log"
LOG_LEVEL = "ERROR"

# write results to mongodb database
ITEM_PIPELINES = ['doonia.pipelines.MongoDBPipeline',]

# mongodb details
MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "doonia"
MONGODB_COLLECT_PRODUCTION = "production"
MONGODB_COLLECT_ARCHIVE = "archive"

# use http/1.1
DOWNLOADER_HTTPCLIENTFACTORY = 'doonia.downloader.HTTPClientFactory'
