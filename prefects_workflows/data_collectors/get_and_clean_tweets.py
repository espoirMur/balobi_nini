from datetime import timedelta
from typing import List

from prefect import flow, task
from prefect.task_runners import SequentialTaskRunner
from prefect.tasks import task_input_hash

from tweets_cleaner.TweetsCleaner import TweetsCleaner
from tweets_queries.twitter_client import get_twitter_client
from tweets_queries.twitter_query_data import query_tweets


@task(name="Get tweets", description="Get tweets from twitter API with the given keywords")
def get_tweets(max_tweets: int, keywords: List[str]) -> List[dict]:
    client = get_twitter_client()
    tweets = query_tweets(client, max_tweets=max_tweets, query=keywords)
    return tweets


@task(
    name="clean tweets",
    description="Clean tweets and return the cleaned tweets",
    cache_key_fn=task_input_hash,
    cache_expiration=timedelta(minutes=30),
)
def clean_tweets(tweets: List[dict]) -> List[dict]:
    cleaner = TweetsCleaner()
    cleaned_tweets = cleaner.clean_tweets(tweets)
    return cleaned_tweets


@flow(name="Get and clean tweets", task_runner=SequentialTaskRunner())
def get_and_clean_tweets(keywords: List[str], max_tweets: int) -> List[dict]:
    tweets = get_tweets(max_tweets=max_tweets, keywords=keywords)
    cleaned_tweets = clean_tweets(tweets, wait_for=[tweets])
    return cleaned_tweets
