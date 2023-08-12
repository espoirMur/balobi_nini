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
from utils.words_to_remove import OTHERS_WORDS, CONGO_WORDS
from datetime import datetime



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
    words_to_remove = punctuation + stop_word_list_english + \
        stop_word_list_french + OTHERS_WORDS
    words_to_remove = set(words_to_remove).union(CONGO_WORDS)
    words_to_remove = words_to_remove.union(
        set(many_stop_words.get_stop_words('fr')))
    return words_to_remove
