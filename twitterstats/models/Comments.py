from datetime import datetime

class Comment(object):
    def __init__(self, email, content, created=None):
        self.email = email
        self.content = content
        self.created = created or datetime.now()

comment = Comment(email='leila@example.com', content='foo bar')

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
    def __init__(self, id_str, author, text, fav_count, retweet_count, created_at, entities):
        self.id_str = id_str
        self.author = author
        self.text = text
        self.favorite_count = fav_count
        self.retweet_count = retweet_count
        self.created_at = created_at
        self.entities = entities

class TweetList(object):
    def __init__(self, tweets):
        self.total_count = len(tweets)
        self.tweets = tweets

class TweetSummary(object):
    def __init__(self, original_count, retweet_count, replies_count,
                 tweets_with_hashtags, tweets_with_mentions):
        self.original_tweet_count = original_count
        self.retweet_count = retweet_count
        self.replies_count = replies_count
        self.tweets_with_hashtags = tweets_with_hashtags
        self.tweets_with_mentions = tweets_with_mentions

class TweetCache(object):
    def __init__(self, timestamp, latest_id, original_tweets, retweets, replies):
        self.timestamp = timestamp
        self.latest_id = latest_id
        self.original_tweets = original_tweets
        self.retweets = retweets
        self.replies = replies

