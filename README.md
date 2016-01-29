# UserStats
This is a Web app that provides a framework for visualization of data from various 3rd party resources like Twitter, Gmail etc.

Currently this repository only provides a way to analyze twitter stats. In future there are plans to add email stats, linkedin stats, facebook stats etc as well. 

The backend of the project provides REST APIs to fetch the stats of data from 3rd party services. The backend dependencies are: 
* Django
* Django rest framework 
* Tweepy
* NLTK

The frontend is a single page application. The dependencies for front end are:
* Backbone js
* D3.js
* Bootstrap

To manage python dependencies we use virtualenv and pip. If you are not familiar with those tools below is a good read:
http://www.dabapps.com/blog/introduction-to-pip-and-virtualenv-python/

To test this webapp locally (tested on mac), go throught the following steps:
* You need to create your own twitter app. Goto https://apps.twitter.com/ to create one. 
  Set your callback url to http://127.0.0.1:8000/twitterstats/auth
* Install Mysql server on your local machine and create a userstats database.
* Add mysql to your path. Usually its found in /usr/local/mysql/bin. export PATH=$PATH:/usr/local/mysql/bin
* virtualenv userstats
* pip install -r requirements.txt
   : Note that sometimes you might see failures when installing MYSQL_python, because it unable to find mysql config.
   To resolve that issue, make sure mysql is in your path. If the issue persists, checkout http://stackoverflow.com/questions/5178292/pip-install-mysql-python-fails-with-environmenterror-mysql-config-not-found
* sudo install_name_tool -change libmysqlclient.18.dylib /usr/local/mysql/lib/libmysqlclient.18.dylib $VIRTUAL_ENV/lib/python2.7/site-packages/_mysql.so
* Copy settings_local.template to settings_local.py
* Insert the correct consumer_token and consumer_secret in settings_local.py.
* Fill in all the required fields for Database settings in setting_local.py.
* Setup proper permissions on your mysql directory
   :sudo chown -R mysql:mysql /usr/local/mysql/
    sudo chmod -R 755 /usr/local/mysql/
* brew install memcached
* run memcached
* run python manage.py migrate
* run python manage.py runserver

To test the server hit the url:

localhost:8000/twitterstats/tweets

You should see some stats about your latest tweets. Try typing elonmusk in the search box and see the changes.


Serving content via nginx.
For this project we have decided to use nginx as our web server. Following are the steps to enable nginx on your development box.

* Make sure pip list show that uWSGI is installed as a dependency. It is part of requirements.txt and should have been installed already. If not install it.
* Make sure homebrew is installed.
* In your twitter app, change your callback url to http://127.0.0.1/twitterstats/auth.
* brew install nginx. 
  Note: This installs nginx under /usr/local/Cellar/nginx directory.
* Change all the paths in userstats_nginx.conf to point to your project directory.
* Run command python manage.py collectstatic. This should create a static folder in your root project directory.
* If a site_enabled directory does not exist under nginx, create one. The location should be similar to /usr/local/Cellar/nginx/1.8.0/sites_enabled.
* sudo ln -s ~/path/to/your/userstats/userstats_nginx.conf /usr/local/Cellar/nginx/1.8.0/sites_enabled/
* Edit nginx.conf located at /usr/local/etc/nginx/nginx.conf:
    Remove the entire server configuraton under http. Instead add "include /usr/local/Cellar/nginx/1.8.0/sites_enabled/*;"
* from userstats virtual env start uwsgi using command: uwsgi --socket userstats.sock --module userstats.wsgi --chmod-socket=666
* sudo nginx

to test: goto usr localhost/twitterstats

If nginx does not work, you can try to debug the issue by looking at logs located at:
/usr/local/Cellar/nginx/1.8.0/logs/error.log

This project is hosted live at:
http://ec2-54-69-110-112.us-west-2.compute.amazonaws.com/twitterstats



