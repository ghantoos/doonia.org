#!/bin/bash

MY_PATH="`dirname \"$0\"`"
PYTHON_ACTIVATE="$MY_PATH/py/bin/activate"
SPIDER_DIR="$MY_PATH/spiders"
LOCK_FILE=/tmp/crawlrss.lock

# add a lock file
lockfile -r 0 $LOCK_FILE || exit 1

# enable python virtualenv
source $PYTHON_ACTIVATE


# launch spider
cd $SPIDER_DIR && timeout --kill-after=560 --signal=9 540 scrapy crawl doonia -a start_urls_file=config/start_urls

EXIT=$?

# rm the lock file
rm -f $LOCK_FILE

exit $EXIT
