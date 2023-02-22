from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule

from constants import KEYWORD_LIST, MAX_TWEETS
from prefects_workflows.data_collectors.main import collect_tweets_data_flow
from prefects_workflows.tweet_word_cloud import tweet_word_cloud

collect_data_deployment = Deployment.build_from_flow(
    flow=collect_tweets_data_flow,
    name="collect tweet data",
    parameters={"keywords": KEYWORD_LIST, "max_tweets": MAX_TWEETS},
    infra_overrides={"env": {"PREFECT_LOGGING_LEVEL": "INFO"}},
    schedule=CronSchedule(cron="0 */1 * * *", timezone="GMT+0"),
    work_queue_name="test",
)

tweet_world_cloud_deployment = Deployment.build_from_flow(
    flow=tweet_word_cloud,
    name="tweet word cloud",
    schedule=CronSchedule(cron="0 18 * * *", timezone="GMT+0"),
    parameters={},
    infra_overrides={"env": {"PREFECT_LOGGING_LEVEL": "INFO"}},
    work_queue_name="test",
)


if __name__ == "__main__":
    collect_data_deployment.apply()
    tweet_world_cloud_deployment.apply()
