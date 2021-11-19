from app import db
from sqlalchemy.dialects.postgresql import JSON, insert


class CleannedTweet(db.Model):
    __tablename__ = 'tweet'

    id = db.Column(db.BigInteger, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    raw_json = db.Column(JSON)

    def __repr__(self):
        return '<id {} {}>'.format(self.id, self.text)
    
    def _to_dictionary(self):
        """
        convert the instance to a dictionary
        """
        return {
            'id': self.id,
            'text': self.text,
            'created_at': self.created_at,
            'raw_json': self.raw_json
        }

    def save_to_database(self):
        """
        save the instance to the database
        """
        db.session.execute(insert(CleannedTweet).values([self._to_dictionary()]).on_conflict_do_nothing())
        db.session.commit()
        print("I am done saving the tweet in the database ")
