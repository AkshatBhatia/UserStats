from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.TweetDetails.as_view(), name='twitterstats'),
    url(r'^auth/$', views.auth, name='authenticate'),
    url(r'^api/$', views.api_root),
]
