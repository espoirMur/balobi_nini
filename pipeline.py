"""
this pipeline will do 4 main actions
- get the data from Twitter
- clean them
- save it in a database
- Load the data from the database and genearate a word cloud (this will be save in a database)
I will need an endpoint which once call will pull all the data for the given day and generate a world cloud
"""
from scripts.twitter_query_data import query_tweet
from scripts.twitter_client import get_twitter_client
from tweepy import TweepError
from tweets_cleaner.TweetsCleaner import TweetsCleaner
from app.model import CleannedTweet
from app import db
from datetime import datetime

if __name__ == "__main__":
    client = get_twitter_client()
    try:
        for tweet in query_tweet(
            client,
            max_tweets=2000,
            query=[
                'RDC',
                'RDCongo',
                'DRC',
                'DRCongo']):
            cleaner = TweetsCleaner('.')
            cleaned_tweet = cleaner.prepocess_tweet(tweet.get('text'))
            tweet_date = tweet.get('created_at'),
            # TODO This can be done as a celery task
            cleaned_tweet_model = CleannedTweet(
                id=tweet.id, text=" ".join(cleaned_tweet), created_at=tweet_date)
            db.session.add(cleaned_tweet_model)
        db.session.commit()

    except TweepError as e:
        print(e, '====')
