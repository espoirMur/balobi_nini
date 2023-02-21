from typing import List

from prefect import flow

from .get_and_clean_tweets import get_and_clean_tweets
from .sql_flows import save_tweets_to_db_flow


@flow(name="collect tweets data", description="main workflow to collect tweets data with the given keywords")
def collect_tweets_data_flow(keywords: List, max_tweets: int):
    cleaned_tweets = get_and_clean_tweets(keywords, max_tweets)
    save_tweets_to_db_flow(cleaned_tweets, wait_for=[cleaned_tweets])
