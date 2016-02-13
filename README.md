# Doonia.org 

This is the source behind doonia.org website. This website is intended to
aggregate RSS feeds and nicely print them using Zurb Foundation.

I have worked on this project in collaboration with Alban Thiébaut (@albeu) and Tarek Abi Aad (@tareh).

The architecture is:
- Mongodb database
- Python Flask web framework
- Zurb Foundation CSS
- Python Scrapy for scrapping the websites

Feel free to use any/whole part of this website. The code is distributed
under the WTFPL license.

In order to install doonia.org, follow these steps:

* Clone the repo

``` git clone git@github.com:ghantoos/doonia.org.git```

* Intsall the Python requirements

```bash
cd doonia.org
virtualenv --no-site-packages py
source py/bin/activate
pip install -r requirements.txt
```

* Install rvm

```bash
cd doonia.org
curl -L https://get.rvm.io | bash -s stable --ruby
rvm install ree-1.8.7-2012.02
rvm --rvmrc --create use ree-1.8.7-2012.02@mkt
```

* Install the required gems

``` gem install zurb-foundation -v 3.2.5```

* Install mongodb
```
apt-get install mongodb
```

* Create mongodb databases/collection and user
```
mongo
> use doonia
> db.createCollection("production")
> db.createCollection("dev")
> db.createUser(
    {
      user: "doonia",
      pwd: "someothersecret",
      roles: ["readWrite"]
    }
)
```

* Add user/name password to configuration file
```
cp website/config/doonia.conf-example website/config/doonia.conf
vim website/config/doonia.conf

Look for 'SECRET_KEY'

```

* Edit the RSS spider configuration file
```
vim spiders/config/start_urls
```

* Edit the spider configuration if needed. It uses the doonia db, and production collection by default
```
vim spiders/doonia/settings.py
```

* Run the crawler to gather information and store in the mongo db
```
./crawlrss.sh
```

* Run the Flask server

```bash
cd doonia.org
python doonia.py runserver -t 0.0.0.0 -p 5000
```

* Add the crawler and db purge to the crontab
```
*/15 * * * * /home/ghantoos/doonia.org/crawlrss.sh 2>&1 >/dev/null
0 0 * * * /home/ghantoos/doonia.org/purgedb.sh
```
