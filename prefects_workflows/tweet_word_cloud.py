from datetime import date
from typing import List

from prefect import flow, task
from sqlalchemy import Date, select
from sqlalchemy.orm import Session

from logger_config import logger
from model import CleanedTweet
from prefects_workflows.data_collectors.sql_flows import connect_to_db
from tweets_queries.tweets_actions import tweet_words_count
from tweets_queries.twitter_client import get_twitter_client
from utils.wordcloud import generate_today_word_cloud


@task(name="retrieve today cleaned tweets", description="retrieve today cleaned tweets")
def retrieve_today_cleaned_tweets(engine) -> List[str]:
    """retrieve today cleaned tweets"""
    with Session(engine) as session:
        statement = select(CleanedTweet.text).filter(CleanedTweet.created_at.cast(Date) == date.today())
        cleaned_tweets = session.execute(statement).all()
        return cleaned_tweets


@task(name="generate world cloud", description="generate world cloud for today terms")
def generate_image(cleaned_tweets: List[str]):
    # Pull
    world_cloud = generate_today_word_cloud(cleaned_tweets)
    return world_cloud


@task(name="tweet worldcloud image", description="tweet worldcloud image")
def tweet_image(image_path):
    client = get_twitter_client()
    if image_path:
        tweet_words_count(client, image_path)
    else:
        logger.warning("No image generated")


@flow(name="Tweet word cloud", description="Tweet word cloud")
def tweet_word_cloud():
    engine = connect_to_db()
    cleaned_tweets = retrieve_today_cleaned_tweets(engine)
    world_cloud_path = generate_image(cleaned_tweets)
    tweet_image(world_cloud_path)
