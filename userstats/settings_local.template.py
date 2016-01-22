__author__ = 'akbhatia'

CONSUMER_TOKEN = 'YOUR APP TOKEN'
CONSUMER_SECRET = 'YOUR CONSUMER SECRET'

DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'userstats',
        'USER': 'YOUR USER NAME',
        'PASSWORD': 'YOUR PASSWORD',
        'HOST': 'YOUR HOST NAME',
        'PORT': 'YOUR PORT'
    }
}