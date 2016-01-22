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

To test this webapp locally, you need to create your own twitter app. Goto https://apps.twitter.com/ to create one.
Once that app is created:
1. Copy settings_local.template to settings_local.py
2. insert the correct consumer_token and consumer_secret in settings_local.py.

To get started with the server:
1. virtualenv userstats
2. pip install -r requirements.txt
3. python manage.py runserver

To test the server hit the url:

localhost:8000/twitterstats/tweets

You should see some stats about your latest tweets.



