import os
from pathlib import Path
from urllib.parse import quote

from dotenv import load_dotenv


class Config(object):
    def __init__(self, env_name=".env"):
        env_path = Path.cwd().joinpath(env_name)
        load_dotenv(dotenv_path=env_path)
        self.DEBUG = False
        self.TESTING = False
        self.CSRF_ENABLED = True
        self.SECRET_KEY = os.environ.get("SECRET_KEY")
        self.SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{user}:{password}@{host}/{database}".format(
            user=os.environ.get("POSTGRES_USER"),
            password=quote(os.environ.get("POSTGRES_PASSWORD")),
            host=os.environ.get("POSTGRES_HOST"),
            database=os.environ.get("POSTGRES_DB"),
        )


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


app_config = {
    "development": DevelopmentConfig(),
    "production": ProductionConfig(".env.production"),
    "testing": ProductionConfig(".env.testing"),
}
