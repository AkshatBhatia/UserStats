from serializers.CommentSerializer import TweetListSerializer, TwitterUserSerializer, TweetCacheSerializer, TweetSummarySerializer
from sets import Set
from django.core.cache import cache
from django.http import HttpResponse
from django.template import RequestContext, loader
from models.Comments import MentionsCount, Tweet, TweetCache, TweetList, TwitterUser, TweetSummary
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.shortcuts import redirect
import operator
import tweepy
import datetime

consumer_token = 'Jjv00qLJ2AcGvf0HHLyc6kPhm'
consumer_secret = 'YOUR_CONSUMER_SECRET'

class UserDetails(APIView):
    def __init__(self):
        self.myname = "Akshat"

    def get(request, format=None):
        if not check_key(request.request):
            return redirect(get_redirect_url(request.request))
        else:
            api = get_api(request.request)
            user_details = api.me()

            user = TwitterUser(user_details.id_str, user_details.name, user_details.screen_name,
                        user_details.location, user_details.created_at, user_details.profile_image_url,
                        user_details.followers_count, user_details.favourites_count, user_details.statuses_count)

            serializer = TwitterUserSerializer(user)

            return Response(serializer.data)

@api_view(('GET',))
def user_tweets(request):
    if not check_key(request):
        return redirect(get_redirect_url(request))
    else:
        user = request.GET.get('user', '')
        filters = request.GET\
            .get('filters', "Tweet Type=Original Tweets;Media Type=Photos,Videos;Timeline=UserTimeline").split(";")

        filterMap = {}
        for f in filters:
            tokens = f.split("=")
            filterMap[tokens[0]] = Set(tokens[1].split(","))

        timeline = filterMap.get(u"Timeline").pop()

        original_tweets, retweets, replies = get_tweets(request, user, timeline)

        total_tweets = filter_by_tweet_type(filterMap, original_tweets, replies, retweets)

        serializer = TweetListSerializer(TweetList(total_tweets))
        return Response(serializer.data)


def filter_by_tweet_type(filterMap, original_tweets, replies, retweets):
    total_tweets = []
    tweet_type = filterMap.get(u"Tweet Type")
    if u"Original Tweets" in tweet_type:
        total_tweets += original_tweets
    if u"Retweets" in tweet_type:
        total_tweets += retweets
    if u"Replies" in tweet_type:
        total_tweets += replies
    return total_tweets


@api_view(('GET',))
def tweet_summary(request):
    if not check_key(request):
        return redirect(get_redirect_url(request))
    else:
        user = request.GET.get('user', u'')
        timeline = u"UserTimeline"
        original_tweets, retweets, replies = get_tweets(request, user, timeline)

        hashtags = {}
        user_mentions = {}
        tweets_with_hashtags, tweets_with_mentions, photos, videos, animated_gif = 0, 0, 0, 0, 0
        for tweet in original_tweets + retweets + replies:
            entities = tweet.get(u'entities')
            tags = entities.get(u'hashtags')
            if len(tags) > 0:
                tweets_with_hashtags += 1

            for hashtag in tags:
                count = hashtags.get(hashtag.get(u'text'), 0) + 1
                hashtags[hashtag.get(u'text')] = count

            mentions = entities.get(u'user_mentions')
            if len(mentions) > 0:
                tweets_with_mentions += 1

            for mention in mentions:
                mention_user = mention.get(u'screen_name')
                count = user_mentions.get(mention_user, 0) + 1
                user_mentions[mention_user] = count

        sorted_mentions = sorted(user_mentions.items(), key=operator.itemgetter(1))
        sorted_mentions.reverse()
        sorted_limited_mentions = sorted_mentions[:10]
        mentions = []
        for key, val in sorted_limited_mentions:
            mentions.append(MentionsCount(key, val))

        serializer = TweetSummarySerializer(TweetSummary(
            len(original_tweets),
            len(retweets),
            len(replies),
            tweets_with_hashtags,
            tweets_with_mentions,
            mentions))

        return Response(serializer.data)

def get_tweets(request, user, timeline):
    cache_key = user + "_" + timeline
    data_cached, original_tweets, retweets, replies = get_cached_tweets(cache_key)
    if data_cached:
        print u'Got data from cache!!'
        return original_tweets, retweets, replies
    else:
        api = get_api(request)
        api_function = api.user_timeline
        if u"HomeTimeline" == timeline:
            api_function = api.home_timeline

        if user:
            user_tweets = tweepy.Cursor(api_function, id=user, count=200).items(1000)
        else:
            user_tweets = tweepy.Cursor(api_function, count=200).items(1000)

        retweets = []
        replies = []
        original_tweets = []
        latest_id = u"1"
        for tweet in user_tweets:
            if tweet.id_str > latest_id:
                latest_id = tweet.id_str
            t = Tweet(id_str=tweet.id_str,
                      author=tweet.author.screen_name,
                      text=tweet.text,
                      fav_count=tweet.favorite_count,
                      retweet_count=tweet.retweet_count,
                      created_at=getEpochTime(tweet.created_at),
                      entities =tweet.entities)
            if tweet.text.startswith("RT"):
                retweets.append(t)
            elif tweet.text.startswith("@"):
                replies.append(t)
            else:
                original_tweets.append(t)

        save_to_cache(cache_key, original_tweets, retweets, replies, latest_id)

        return original_tweets, retweets, replies

def get_cached_tweets(cache_key):
    cached_data = cache.get(cache_key)
    if cached_data:
        serializer = TweetCacheSerializer(data=cached_data)
        serializer.is_valid()
        if serializer.is_valid():
            original_tweets = serializer.validated_data.get('original_tweets')
            retweets = serializer.validated_data.get('retweets')
            replies = serializer.validated_data.get('replies')
            return True, original_tweets, retweets, replies

    return False, None, None, None

def save_to_cache(key, original_tweets, retweets, replies, latest_id):
    serializer = TweetCacheSerializer(TweetCache(
        getEpochTime(datetime.datetime.now()),
        latest_id,
        original_tweets,
        retweets,
        replies))

    cache.set(key, serializer.data)


def getEpochTime(date):
    return int((date - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)


# @api_view(('GET',))
# def tweet_stats_by_month(request):
#     if not check_key(request):
#         return redirect(get_redirect_url(request))
#     else:
#         api = get_api(request)
#         user = request.GET.get('user', None)


@api_view(('GET',))
def auth(request):
    verifier = request.GET.get('oauth_verifier')
    oauth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    token = request.session.get('unauthed_token_tw', None)
    # remove the request token now we don't need it
    request.session.delete('unauthed_token_tw')
    oauth.request_token = token
    # get the access token and store
    try:
        oauth.get_access_token(verifier)
    except tweepy.TweepError:
        print 'Error, failed to get access token'

    request.session['access_key_tw'] = oauth.access_token
    request.session['access_secret_tw'] = oauth.access_token_secret
    return redirect(reverse('index'))

def check_key(request):
    """
    Check to see if we already have an access_key stored, if we do then we have already gone through
    OAuth. If not then we haven't and we probably need to.
    """
    try:
        access_key = request.session.get('access_key_tw', None)
        if not access_key:
            return False
    except KeyError:
        return False
    return True

def get_redirect_url(request):
    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)

    try:
        redirect_url = auth.get_authorization_url(True)
    except tweepy.TweepError:
        print 'error! failed to get request token.'

    request.session['unauthed_token_tw'] = auth.request_token

    return redirect_url

def get_api(request):
    oauth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    access_key = request.session['access_key_tw']
    access_secret = request.session['access_secret_tw']
    oauth.set_access_token(access_key, access_secret)
    api = tweepy.API(oauth)
    return api

@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'userinfo': reverse('userinfo', request=request, format=format),
        'tweets': reverse('usertweets', request=request, format=format),
    })

def index(request):
    template = loader.get_template('twitterstats/index.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))
