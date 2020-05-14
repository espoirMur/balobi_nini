# Chap02-03/twitter_get_home_timeline.py
import json
from tweepy import Cursor, TweepError
from scripts.twitter_client import get_twitter_client
from datetime import datetime, timedelta
from itertools import chain


def get_location(client, country):
    """
    return geolocation  of a country passed in param from tweet client api
    """
    places = client.geo_search(query=country, granularity="country")
    place_id = places[0].id
    coordinates = places[0].bounding_box.coordinates[0]
    coordinates = list(set((chain.from_iterable(coordinates))))
    return {'place': "place:{}".format(place_id), 'coordinates': coordinates}


def query_tweet(client, query=[], max_tweets=2000, country=None):
    """
    query tweets using the query list pass in parameter
    """
    if country:
        query = get_location(client, country).get('place')
    else:
        query = ' OR '.join(query)
        print('query', query)
    for status in Cursor(
            client.search,
            q=query,
            include_rts=True).items(max_tweets):
        yield status


def get_home_timeline(client):
    with open('../data/home_timeline.jsonl', 'w') as f:
        for page in Cursor(
                client.home_timeline,
                count=200,
                include_rts=True).pages(4):
            for status in page:
                # Process a single status
                f.write(json.dumps(status._json) + "\n")
