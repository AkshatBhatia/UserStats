from serializers.CommentSerializer import TweetListSerializer
from serializers.CommentSerializer import TwitterUserSerializer
from models.Comments import Tweet
from models.Comments import TweetList
from models.Comments import TwitterUser
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.shortcuts import redirect
import tweepy

consumer_token = 'Jjv00qLJ2AcGvf0HHLyc6kPhm'
consumer_secret = 'VXHkcX1SzPb8ubzcBHhR9FmFwx7BTdKpmogEszHJiosRCSUGPq'

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

            # user_tweets = api.user_timeline()
            # tweets = []
            # for tweet in user_tweets:
            #     tweets.append(Tweet(author=tweet.author.screen_name,
            #                         text=tweet.text,
            #                         fav_count=tweet.favorite_count,
            #                         retweet_count=tweet.retweet_count))
            #
            # serializer = TweetListSerializer(TweetList(tweets))
            return Response(serializer.data)


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
    return redirect(reverse('twitterstats'))

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
        'twitterstats': reverse('twitterstats', request=request, format=format),
    })
