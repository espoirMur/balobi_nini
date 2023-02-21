from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from dags import default_args
from tweets_queries.tweets_actions import tweet_words_count
from tweets_queries.twitter_client import get_twitter_client
from utils.wordcloud import generate_today_word_cloud


def generate_image(**context):
    # Pull
    image_path = generate_today_word_cloud()
    context["task_instance"].xcom_push(key="word_cloud_path", value=image_path)


def tweet_image(**context):
    client = get_twitter_client()
    image_path = context["task_instance"].xcom_pull(task_ids="generate_image", key="word_cloud_path")
    if image_path:
        tweet_words_count(client, image_path)
    else:
        print("No image generated")


tweet_word_cloud_dag = DAG(
    dag_id="tweet_word_cloud",
    default_args=default_args,
    schedule_interval="00 18 * * *",  # every  day at 22:00Pm need to bring back to 18pmUTC
    catchup=False,
)


generate_image_operator = PythonOperator(
    task_id="generate_image",
    python_callable=generate_image,
    provide_context=True,
    dag=tweet_word_cloud_dag,
)

tweet_image_operator = PythonOperator(
    task_id="tweet_image_operator",
    python_callable=tweet_image,
    provide_context=True,
    dag=tweet_word_cloud_dag,
)

generate_image_operator >> tweet_image_operator
