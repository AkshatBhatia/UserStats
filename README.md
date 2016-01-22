# UserStats
This is a Web app that provides a framework for visualization of data from various 3rd party resources like Twitter, Gmail etc.

Currently this repository only provides a way to analyze twitter stats. In future there are plans to add email stats, linkedin stats, facebook stats etc as well. 

The backend of the project provides REST APIs to fetch the stats of data from 3rd party services. The backend dependencies are:
1. Django
2. Django rest framework
3. Tweepy
4. NLTK

The frontend is a single page application. The dependencies for front end are:
1. Backbone js
2. D3.js
3. Bootstrap

To manage python dependencies we use virtualenv and pip. If you are not familiar with those tools below is a good read:
http://www.dabapps.com/blog/introduction-to-pip-and-virtualenv-python/

To test this webapp locally (tested on mac), go throught the following steps:
1. you need to create your own twitter app. Goto https://apps.twitter.com/ to create one.
2. Install Mysql server on your local machine and create a userstats database.
3. Add mysql to your path. Usually its found in /usr/local/mysql/bin. export PATH=$PATH:/usr/local/mysql/bin
4. virtualenv userstats
5. pip install -r requirements.txt
   : Note that sometimes you might see failures when installing MYSQL_python, because it unable to find mysql config.
   To resolve that issue, make sure mysql is in your path. If the issue persists, checkout http://stackoverflow.com/questions/5178292/pip-install-mysql-python-fails-with-environmenterror-mysql-config-not-found
6. sudo install_name_tool -change libmysqlclient.18.dylib /usr/local/mysql/lib/libmysqlclient.18.dylib $VIRTUAL_ENV/lib/python2.7/site-packages/_mysql.so
7. Copy settings_local.template to settings_local.py
8. Insert the correct consumer_token and consumer_secret in settings_local.py.
9. Fill in all the required fields for Database settings in setting_local.py.
10. run python manage.py migrate
11: run python manage.py runserver

To test the server hit the url:

localhost:8000/twitterstats/tweets

You should see some stats about your latest tweets. Try typing elonmusk in the search box and see the changes.



