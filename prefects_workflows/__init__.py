from datetime import datetime, timedelta

from dotenv import load_dotenv

load_dotenv()

default_args = {
    "owner": "airflow",
    "depend_on_past": False,
    "email": "espoir.mur@gmail.com",
    "start_date": datetime(2020, 5, 14),
    "email_on_failure": False,
    "wait_for_downstream": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}
