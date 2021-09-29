from app import db
from sqlalchemy.dialects.postgresql import JSON


class CleannedTweet(db.Model):
    __tablename__ = 'tweet'

    id = db.Column(db.BigInteger, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    raw_json = db.Column(JSON)

    def __repr__(self):
        return '<id {} {}>'.format(self.id, self.text)

    def save_to_database(self):
        """
        save the instance to the database
        """
        db.session.add(self)
        db.session.commit()
