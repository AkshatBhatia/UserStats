from rest_framework import serializers

class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()

class TweetSerializer(serializers.Serializer):
    author = serializers.CharField(max_length=300)
    text = serializers.CharField(max_length=140)
    favorite_count = serializers.IntegerField()
    retweet_count = serializers.IntegerField()

