from prefect.deployments import Deployment

from prefects_workflows.get_and_clean_tweets import get_and_clean_tweets

deployment = Deployment.build_from_flow(
    flow=get_and_clean_tweets,
    name="get-and-clean-tweets",
    parameters=None,
    infra_overrides={"env": {"PREFECT_LOGGING_LEVEL": "DEBUG"}},
    work_queue_name="test",
)

if __name__ == "__main__":
    deployment.apply()
