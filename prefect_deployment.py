from prefect.deployments import Deployment

from constants import KEYWORD_LIST, MAX_TWEETS
from prefects_workflows.data_collectors.main import collect_tweets_data_flow

deployment = Deployment.build_from_flow(
    flow=collect_tweets_data_flow,
    name="collect tweet data",
    parameters={"keywords": KEYWORD_LIST, "max_tweets": MAX_TWEETS},
    infra_overrides={"env": {"PREFECT_LOGGING_LEVEL": "DEBUG"}},
    work_queue_name="test",
)

if __name__ == "__main__":
    deployment.apply()
