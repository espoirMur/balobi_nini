from app import db


class CleannedTweet(db.Model):
    __tablename__ = 'cleanned_tweet'

    id = db.Column(db.BigInteger, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)    

    def __repr__(self):
        return '<id {} {}>'.format(self.id, self.text)
