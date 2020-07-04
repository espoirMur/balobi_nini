from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from tweets_queries.twitter_query_data import query_tweets
from tweets_queries.twitter_client import get_twitter_client
from tweets_cleaner.TweetsCleaner import TweetsCleaner
from datetime import timedelta, datetime



def get_tweets(**context):
    # Pull
    client = get_twitter_client()
    tweets = query_tweets(
        client, max_tweets=2000, query=[
            'RDC', 'RDCongo', 'DRC', 'DRCongo'])
    context['task_instance'].xcom_push(key='tweets',
                                       value=list(tweets))


def clean_save_to_db(**context):
    tweets = context['task_instance'].xcom_pull(
        task_ids='get_tweets', key='tweets')
    cleaner = TweetsCleaner('.')
    cleaner.save_clean_tweets(tweets)


default_args = {
    "owner": "airflow",
    "depend_on_past": False,
    "email": "espoir.mur@gmail.com",
    "start_date": datetime(2020, 5, 14),
    "email_on_failure": False,
    "wait_for_downstream": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

dag = DAG(
    dag_id='collect_tweets',
    default_args=default_args,
    schedule_interval='@hourly',  # every  60 minutes
    catchup=False)


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
