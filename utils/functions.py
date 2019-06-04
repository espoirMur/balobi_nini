import sys
import string
import pickle
import json
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import many_stop_words
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from collections import Counter, defaultdict
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords

from datetime import datetime


from datetime import datetime


TWEETS_PATH = '../data/query_drc_by_hashtags__03-06-2019-12-53.jsonl'


def get_text(tag):
    """return text from hashtags

    Args:
        tag (object): object with hashtags

    Returns:
        string: the text from a hashtag
    """
    return tag.get('text').lower()


def get_hashtags(tweet):
    """return hashtags from a given tweet

    Args:
        tweet (object): an object representing a tweet

    Returns:
        list: list of hastags in a tweet
    """
    entities = tweet.get('entities', {})
    hashtags = entities.get('hashtags', [])
    return [get_text(tag) for tag in hashtags if get_text(
        tag) not in ['rdc', 'drc', 'rdcongo', 'drcongo']]


def read_tweets_file(path):
    """ function which read a file with tweets

    Args:
        path (string): path for the file of tweets

    Returns:
        iterator: an iterator of tweets obejcts
    """
    with open(path, 'r') as f:
        for line in f:
            tweet = json.loads(line)
            yield tweet


def get_most_common_hashtags(path, number):
    """
    find the most common hash tags in a corpus of tweets

    Args:
        path (string): path of the tweet files
        number (int): number of most frequent hashtags to return
    Returns :
        an iterator of most tags and their count
    """
    hastags = Counter()
    for tweet in read_tweets_file(TWEETS_PATH):
        hashtags_in_tweet = get_hashtags(tweet)
        hastags.update(hashtags_in_tweet)
    for tag, count in hastags.most_common(number):
        yield tag, count


def process_text(text, tokenizer=TweetTokenizer(), words_to_remove=[]):
    """
    clean a tweet text

    Args:
        text (string): text of a tweet
        tokenizer (TweetTokenizer, optional): tokenizer to use from NLTK. Defaults to TweetTokenizer().
        words_to_remove (list, optional): list of words to remove. Defaults to [].

    Returns:
        list: tokens from a tweet
    """
    text = text.lower()
    tokens = tokenizer.tokenize(text)
    return [
        token for token in tokens if token not in words_to_remove and not token.isdigit()]


def get_words_to_remove():
    """
    generate a list of words to remove for a better cleaning of tweets
    Returns:
        set : an array of words to remove
    """
    punctuation = list(string.punctuation)
    stop_word_list_english = stopwords.words('english')
    stop_word_list_french = stopwords.words('french')
    others_words = ['rt', 'via', '...', '…', '»:', '«:', '’:', 'les', '-', ]
    words_to_remove = punctuation + stop_word_list_english + \
        stop_word_list_french + others_words
    congo_words = {
        'congo',
        'congolais',
        'rdc',
        'drc',
        '-',
        'https',
        'rdc',
        'rdcongo',
        'drc',
        'drcongo',
        'tshisekedi'}
    words_to_remove = set(words_to_remove).union(congo_words)
    words_to_remove = words_to_remove.union(
        set(many_stop_words.get_stop_words('FR')))
    return words_to_remove


def get_most_common_words(number, words_to_remove, path=TWEETS_PATH):
    """
    find the most common words in a corpus of tweets
    Args:
        path (string): path of the tweet files
        number (int): number of most frequent hashtags to return
        word_to_remove: list of words to remove
    Returns :
        an iterator most frequent words  and their count
    """
    term_counts = Counter()
    for tweet in read_tweets_file(TWEETS_PATH):
        tokens = process_text(
            text=tweet.get('text'),
            words_to_remove=words_to_remove)
        term_counts.update(tokens)
    for tag, count in term_counts.most_common(number):
        yield tag, count
