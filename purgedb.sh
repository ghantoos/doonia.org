#!/bin/bash

date=`date -d"1 month ago" +"%Y%m%d"`
mongo --quiet doonia << EOF
db.production.remove( { date : {"\$lt" : "$date-" } })
db.dev.remove( { date : {"\$lt" : "$date-" } })
EOF

exit 0
