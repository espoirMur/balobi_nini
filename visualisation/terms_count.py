from app.model import CleannedTweet
from collections import Counter
from datetime import date
from sqlalchemy import Date


def get_term_count():
    """
    preporcess and return terms count from a file of tweets.
    Parm :
    path:  string : the path of the tweet files
    return a dictionary of term and the count of they occurrences
    """
    term_counts = Counter()
    cleanned_tweets = CleannedTweet.query.filter(CleannedTweet.created_at.cast(Date)==date.today())
    for tweet in cleanned_tweets:
        text = tweet.text
        tokens = text.split(' ')
        term_counts.update(tokens)
    return term_counts
