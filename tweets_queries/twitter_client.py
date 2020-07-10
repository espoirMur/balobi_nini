import os
import sys
import json
from tweepy import API
from tweepy import OAuthHandler
from dotenv import load_dotenv


load_dotenv()


def get_twitter_auth():
    """Setup Twitter authentication.

    Return: tweepy.OAuthHandler object
    """
    try:
        consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
        consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
        access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        access_secret = os.getenv('TWITTER_ACCESS_SECRET')
    except KeyError:
        sys.stderr.write("TWITTER_*  not found\n")
        sys.exit(1)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    return auth


def get_twitter_client():
    """Setup Twitter API client.

    Return: tweepy.API object
    """
    auth = get_twitter_auth()
    client = API(auth)
    return client
