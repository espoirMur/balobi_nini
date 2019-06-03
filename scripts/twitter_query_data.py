# Chap02-03/twitter_get_home_timeline.py
import json
from tweepy import Cursor, TweepError
from twitter_client import get_twitter_client
from datetime import datetime, timedelta


def get_location(client, country):
    """
    return geolocation  of a country passed in param from tweet client api
    """
    places = client.geo_search(query=country, granularity="country")
    place_id = places[0].id
    query = "place:{}".format(place_id)
    return query


def query_tweet(client, query=[], max_tweets=2000, country=None):
    """
    query tweets using the query list pass in parameter
    """
    name = ''
    if country:
        query = get_location(client, country)
        name = 'by_country_coordinate_'
    else:
        query = ' OR '.join(query)
        name = 'by_hashtags_'
    now = datetime.now()
    today = now.strftime("%d-%m-%Y-%H-%M")
    with open('data/query_drc_{}_{}.jsonl'.format(name, today), 'w') as f:
        for status in Cursor(
                client.search,
                q=query,
                include_rts=True).items(max_tweets):
            f.write(json.dumps(status._json) + "\n")


def get_home_timeline(client):
    with open('../data/home_timeline.jsonl', 'w') as f:
        for page in Cursor(
                client.home_timeline,
                count=200,
                include_rts=True).pages(4):
            for status in page:
                # Process a single status
                f.write(json.dumps(status._json) + "\n")


if __name__ == '__main__':
    client = get_twitter_client()
    try:
        query_tweet(client, max_tweets=2000, query=['RDC', 'RDCongo', 'DRC', 'DRCongo', 'Kinshasa'])
    except TweepError as e:
        print(e, '====')
