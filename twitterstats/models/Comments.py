from datetime import datetime


class Comment(object):
    def __init__(self, email, content, created=None):
        self.email = email
        self.content = content
        self.created = created or datetime.now()

class Tweet(object):
    def __init__(self, author, text, fav_count, retweet_count):
        self.author = author
        self.text = text
        self.favorite_count = fav_count
        self.retweet_count = retweet_count

comment = Comment(email='leila@example.com', content='foo bar')
