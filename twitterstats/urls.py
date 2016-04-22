from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^user/$', views.UserDetails.as_view(), name='userinfo'),
    url(r'^tweets/$', views.user_tweets, name='usertweets'),
    url(r'^summary/$', views.tweet_summary, name='usertweets'),
    url(r'^auth/$', views.auth, name='usertweets'),
    url(r'^api/$', views.api_root),
    url(r'^test/$', views.test, name='test'),
]
