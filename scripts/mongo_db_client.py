from pymongo import MongoClient
from datetime import datetime


def get_database(host='localhost', port=27017):
    """
    connect to the database
    Return :
    mongo database connection
    """
    try:
        client = MongoClient(host, port)
        db = client.tweets_db
        return db
    except Exception as identifier:
        pass


def insert_tweet(tweet):
    """
    insert tweet into the database

    Args:
        tweet (json): tweet to insert
    """
    try:
        tweet_date = datetime.strptime(
            tweet.get('created_at'),
            '%a %b %d %H:%M:%S %z %Y')
        print(tweet_date, '==')
        tweet['created_at'] = tweet_date
        db = get_database()
        tweets = db.tweet
        result = tweets.insert_one(tweet)
        print('data inserted', result.inserted_id, tweet.get('created_at'))
        return result.inserted_id
    except Exception as e:
        print(e, '=====')


def get_tweets(start_date, end_date):
    """
    get all tweets from the database given a time range

    Args:
        start_date (date): the staring date of tweets in this format DD-MM-YYYY
        end_date (date): the end date of tweets in this format DD-MM-YYYY
    Returns :
        A resultset set of tweets
    """
    try:
        start_date = datetime.strptime(start_date, "%d-%m-%Y")
        end_date = datetime.strptime(end_date, "%d-%m-%Y")
        db = get_database()
        tweets = db.tweet
        results = tweets.find(
            {'created_at': {'$lte': end_date, '$gte': start_date}})
        return results
    except Exception as ex:
        print(ex, '=====')
