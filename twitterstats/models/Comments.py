from datetime import datetime
import tweepy

class Comment(object):
    def __init__(self, email, content, created=None):
        self.email = email
        self.content = content
        self.created = created or datetime.now()

class TwitterUser(object):
    def __init__(self, id_str, name, screen_name, location, created_at,
                 profile_image_url, followers_count, favorite_count, statuses_count):
        self.id_str = id_str
        self.name = name
        self.screen_name = screen_name
        self.location = location
        self.created_at = created_at
        self.profile_image_url = profile_image_url
        self.follower_count = followers_count
        self.favorite_count = favorite_count
        self.statuses_count = statuses_count

class Tweet(object):
    def __init__(self, id_str, author, text, fav_count, retweet_count, created_at):
        self.id_str = id_str
        self.author = author
        self.text = text
        self.favorite_count = fav_count
        self.retweet_count = retweet_count
        self.created_at = created_at

class TweetList(object):
    def __init__(self, tweets):
        self.tweets = tweets

comment = Comment(email='leila@example.com', content='foo bar')
