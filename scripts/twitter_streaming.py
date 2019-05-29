# Chap02-03/twitter_streaming.py
import sys
import string
import time
from tweepy import Stream
from tweepy.streaming import StreamListener
from twitter_client import get_twitter_auth
from datetime import datetime, timedelta


class CustomListener(StreamListener):
    """Custom StreamListener for streaming Twitter data."""

    def __init__(self, fname):
        safe_fname = format_filename(fname)
        now = datetime.now()
        today = now.strftime("%d-%m-%Y-%H-%M-%S")
        self.outfile = "stream_{}_{}.jsonl".format(safe_fname, today)

    def on_data(self, data):
        try:
            print('fetching data ==')
            with open('data/{}'.format(self.outfile), 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            sys.stderr.write("Error on_data: {}\n".format(e))
            time.sleep(5)
        return True

    def on_error(self, status):
        if status == 420:
            sys.stderr.write("Rate limit exceeded\n".format(status))
            return False
        else:
            sys.stderr.write("Error {}\n".format(status))
            return True


def format_filename(fname):
    """Convert fname into a safe string for a file name.

    Return: string
    """
    return ''.join(convert_valid(one_char) for one_char in fname)


def convert_valid(one_char):
    """Convert a character into '_' if "invalid".

    Return: string
    """
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    if one_char in valid_chars:
        return one_char
    else:
        return '_'


def get_tweets(query_fname, max_time):
    stop = datetime.now() + max_time
    while datetime.now() < stop:
        twitter_stream = Stream(auth, CustomListener(query_fname))
        twitter_stream.filter(track=query, is_async=True)


if __name__ == '__main__':
    query = sys.argv[1:]  # list of CLI arguments
    query_fname = ' '.join(query)  # string
    auth = get_twitter_auth()
    get_tweets(query_fname, timedelta(minutes=30))
