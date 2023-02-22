from sqlalchemy import BigInteger, Column, DateTime, Text
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from logger_config import logger

Base = declarative_base()


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

    def save_to_database(self, engine: Engine):
        """
        save the instance to the database
        """
        with Session(engine) as session:
            session.begin()
            try:
                session.merge(self)
            except IntegrityError:
                logger.info("Tweet already exists")
            except Exception:
                session.rollback()
                raise
            else:
                session.commit()
