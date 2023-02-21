from datetime import datetime
from itertools import chain
from random import randint

from tweepy import Cursor
from tweepy.errors import TweepyException

from logger_config import logger


def get_location(client, country):
    """
    return geolocation  of a country passed in param from tweet client api
    """
    places = client.geo_search(query=country, granularity="country")
    place_id = places[0].id
    coordinates = places[0].bounding_box.coordinates[0]
    coordinates = list(set((chain.from_iterable(coordinates))))
    return {"place": "place:{}".format(place_id), "coordinates": coordinates}


def query_tweets(client, query=[], max_tweets=2000, country=None):
    """
    query tweets using the query list pass in parameter
    """
    if country:
        query = get_location(client, country).get("place")
    else:
        query = " OR ".join(query)
        logger.info(f"The query is{query}")

    try:
        for status in Cursor(client.search_tweets, q=query, include_rts=True).items(max_tweets):
            logger.info("data received from twitter")
            tweet = {
                "text": status.text,
                "created_at": datetime.timestamp(status.created_at),
                "id": status.id,
            }
            yield tweet
    except TweepyException as exec:
        logger.error(f"Error while querying tweets {exec}")
        pass


def query_fake_tweets(client, query=[], max_tweets=2000, country=None):
    """
    query tweets using the query list pass in parameter
    """
    if country:
        query = get_location(client, country).get("place")
    else:
        query = " OR ".join(query)
        logger.info("query", query)
    for status in range(randint(9, 11), randint(14, 20)):
        tweet = {
            "text": "Fake test",
            "created_at": datetime.timestamp(datetime.now()),
            "id": randint(1000, 2000),
        }
        yield tweet
