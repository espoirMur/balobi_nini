from typing import List

from prefect import flow, task

from constants import KEYWORD_LIST, MAX_TWEETS
from tweets_cleaner.TweetsCleaner import TweetsCleaner
from tweets_queries.twitter_client import get_twitter_client
from tweets_queries.twitter_query_data import query_tweets


@task(name="Get tweets", description="Get tweets from twitter API with the given keywords")
def get_tweets(max_tweets: int, keywords: List[str]) -> List[dict]:
    client = get_twitter_client()
    tweets = query_tweets(client, max_tweets=max_tweets, query=keywords)
    return tweets


@task(name="clean tweets", description="Clean tweets and return the cleaned tweets")
def clean_tweets(tweets: List[dict]) -> List[dict]:
    cleaner = TweetsCleaner()
    cleaned_tweets = cleaner.clean_tweets(tweets)
    return cleaned_tweets


@flow(name="Get and clean tweets")
def get_and_clean_tweets(keywords: List[str], max_tweets):
    tweets = get_tweets(max_tweets=max_tweets, keywords=keywords)
    cleaned_tweets = clean_tweets(tweets)
    # should have a task to save the cleaned tweets in a database
    return cleaned_tweets


get_and_clean_tweets(KEYWORD_LIST, MAX_TWEETS)
