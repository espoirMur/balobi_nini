import os
from typing import Any, List

from prefect import flow, task
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from config import app_config as app_configs


@task(name="connect to database and create the database engine")
def connect_to_db():
    app_config = app_configs.get(os.getenv("APP_SETTINGS"))
    DATABASE_URI = app_config.SQLALCHEMY_DATABASE_URI
    engine = create_engine(DATABASE_URI, echo=True)
    return engine


@task(name="Save tweets to database")
def save_tweets_to_db(tweets: List[Any], engine: Engine):
    for tweet in tweets:
        tweet.save_to_database(engine)


@flow(name="Save tweets to database", description="create a connection and save tweets to the database")
def save_tweets_to_db_flow(tweets: List[Any]):
    engine = connect_to_db()
    save_tweets_to_db.submit(tweets, engine)
