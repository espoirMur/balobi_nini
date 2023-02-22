from collections import Counter
from typing import Dict, List


def get_term_count(cleaned_tweets: List[Dict]):
    """
    pre process and return terms count from a file of tweets.
    Parm :
    path:  string : the path of the tweet files
    return a dictionary of term and the count of they occurrences
    """
    term_counts = Counter()
    for tweet in cleaned_tweets:
        text = tweet.text
        tokens = text.split(" ")
        term_counts.update(tokens)
    return term_counts
