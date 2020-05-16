from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from tweets_queries.twitter_query_data import query_tweet
from tweets_queries.twitter_client import get_twitter_client
from tweepy import TweepError
from tweets_cleaner.TweetsCleaner import TweetsCleaner
from app.model import CleannedTweet


def get_tweets(**context):
    # Pull
    client = get_twitter_client()
    tweets = query_tweet(client, max_tweets=2000, query=['RDC', 'RDCongo', 'DRC', 'DRCongo'])
    context['task_instance'].xcom_push(key='tweets',
                                       value=list(tweets))


def clean_save_to_db(**context):
    tweets = context['task_instance'].xcom_pull(task_ids='get_tweets', key='tweets')
    cleaner = TweetsCleaner('.')
    cleaner.save_clean_tweets(tweets)


default_args = {
    "owner": "airflow",
    "depend_on_past": True,
    "email": "espoir.mur@gmail.com",
    "start_date": datetime(2020, 5, 15),
    "email_on_failure": True
}

dag = DAG(
    'collect_tweets',
    default_args=default_args,
    schedule_interval='@hourly')


get_tweets = PythonOperator(
    task_id='get_tweets',
    python_callable=get_tweets,
    provide_context=True,
    dag=dag
 )

clean_and_save_to_db = PythonOperator(
    task_id='clean_and_save_to_database',
    python_callable=clean_save_to_db,
    provide_context=True,
    dag=dag
 )

get_tweets >> clean_and_save_to_db
