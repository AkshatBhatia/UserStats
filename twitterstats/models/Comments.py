from datetime import datetime


class Comment(object):
        def __init__(self, email, content, created=None):
            self.email = email
            self.content = content
            self.created = created or datetime.now()

comment = Comment(email='leila@example.com', content='foo bar')
