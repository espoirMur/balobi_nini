# Chap02-03/twitter_client.py
import os
import sys
import json
from tweepy import API
from tweepy import OAuthHandler


def read_credential(filename):
    """
    read json file with twitter credentials into a python dictionary
    """
    with open(filename) as f_in:
        return(json.load(f_in))


def get_twitter_auth():
    """Setup Twitter authentication.

    Return: tweepy.OAuthHandler object
    """
    try:
        credentials = read_credential('credentials.json')
        consumer_key = credentials['TWITTER_CONSUMER_KEY']
        consumer_secret = credentials['TWITTER_CONSUMER_SECRET']
        access_token = credentials['TWITTER_ACCESS_TOKEN']
        access_secret = credentials['TWITTER_ACCESS_SECRET']
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
