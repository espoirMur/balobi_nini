# Chap02-03/twitter_get_home_timeline.py
import json
from tweepy import Cursor, TweepError
from twitter_client import get_twitter_client
from datetime import datetime, timedelta


def query_tweet(client, query, max_tweets):
    """
    query tweets using the query list pass in parameter
    """
    query = ' OR '.join(query)
    now = datetime.now()
    today = now.strftime("%d-%m-%Y-%H-%M")
    with open('data/query_drc_{}.jsonl'.format(today), 'w') as f:
        print(query)
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
        query_tweet(client, ["DRC", "RDC", "DRCongo", "RDCongo"], 2000)
    except TweepError as e:
        print(e, '====')
