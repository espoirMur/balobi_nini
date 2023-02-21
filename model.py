import os

from sqlalchemy import BigInteger, Column, DateTime, Text, create_engine
from sqlalchemy.dialects.postgresql import JSON, insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base

from config import app_config as app_configs
from logger_config import logger

app_config = app_configs.get(os.getenv("APP_SETTINGS"))
Base = declarative_base()
DATABASE_URI = app_config.SQLALCHEMY_DATABASE_URI
engine = create_engine(DATABASE_URI, echo=True)


class CleanedTweet(Base):
    __tablename__ = "tweet"

    id = Column(BigInteger, primary_key=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)
    raw_json = Column(JSON)

    def __repr__(self):
        return "<id {} {}>".format(self.id, self.text)

    def _to_dictionary(self):
        """
        convert the instance to a dictionary
        """
        return {"id": self.id, "text": self.text, "created_at": self.created_at, "raw_json": self.raw_json}

    def save_to_database(self):
        """
        save the instance to the database
        """
        try:
            engine.execute(insert(CleanedTweet).values([self._to_dictionary()]).on_conflict_do_nothing())
            engine.commit()
            logger.info("I am done saving the tweet in the database ")
        except SQLAlchemyError as e:
            logger.error("Error while saving the tweet to the database: {}".format(e))
