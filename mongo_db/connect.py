from pymongo import MongoClient


def get_database(host='localhost', port=27017):
    """
    connect to the database and return
    Return :

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
        db = get_database()
        tweets = db.tweet
        result = tweet.insert_one(tweet)
        return result.inserted_id
    except Exception as e:
        print(e, '=====')


