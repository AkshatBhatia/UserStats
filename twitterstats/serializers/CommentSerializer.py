from rest_framework import serializers

class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()

class TwitterUserSerializer(serializers.Serializer):
    id_str = serializers.CharField()
    name = serializers.CharField(max_length=300)
    screen_name = serializers.CharField(max_length=300)
    location = serializers.CharField()
    created_at = serializers.DateTimeField()
    profile_image_url = serializers.URLField()
    follower_count = serializers.IntegerField()
    favorite_count = serializers.IntegerField()
    statuses_count = serializers.IntegerField()


class TweetSerializer(serializers.Serializer):
    id_str = serializers.CharField()
    author = serializers.CharField(max_length=300)
    text = serializers.CharField(max_length=200)
    favorite_count = serializers.IntegerField()
    retweet_count = serializers.IntegerField()
    created_at = serializers.IntegerField()
    entities = serializers.DictField()

class MentionsSerializer(serializers.Serializer):
    mention = serializers.CharField()
    count = serializers.IntegerField()

class TweetSummarySerializer(serializers.Serializer):
    original_tweet_count = serializers.IntegerField()
    retweet_count = serializers.IntegerField()
    replies_count = serializers.IntegerField()
    tweets_with_hashtags = serializers.IntegerField()
    tweets_with_mentions = serializers.IntegerField()
    mentions = MentionsSerializer(many=True)

class TweetListSerializer(serializers.Serializer):
    total_count = serializers.IntegerField()
    tweets = TweetSerializer(many=True)

class TweetCacheSerializer(serializers.Serializer):
    timestamp = serializers.IntegerField()
    latest_id = serializers.CharField()
    original_tweets = TweetSerializer(many=True)
    retweets = TweetSerializer(many=True)
    replies = TweetSerializer(many=True)

