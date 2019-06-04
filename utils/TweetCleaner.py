import re
import unicodedata
import many_stop_words
import spacy
import preprocessor as tweet_preprocessor
import pandas as pd
from io import BytesIO
from csv import writer
from functions import process_text, words_to_remove, read_tweets_file
from utils.emoticons import emoticons
from datetime import datetime


french_stematiser = spacy.load('fr')

tweet_preprocessor.set_options(tweet_preprocessor.OPT.URL,
                               tweet_preprocessor.OPT.EMOJI,
                               tweet_preprocessor.OPT.RESERVED,
                               tweet_preprocessor.OPT.EMOJI,
                               tweet_preprocessor.OPT.SMILEY,
                               tweet_preprocessor.OPT.NUMBER,
                               tweet_preprocessor.OPT.MENTION)


class TweetCleaner:

    def __init__(self, path):
        self.TWEETS_PATH = path
        self.words_to_remove = words_to_remove().union(emoticons)
        self.emoji_patterns = re.compile("["
                                         u"\U0001F600-\U0001F64F"  # emoticons
                                         u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                         u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                         # flags (iOS)
                                         u"\U0001F1E0-\U0001F1FF"
                                         u"\U00002702-\U000027B0"
                                         u"\U000024C2-\U0001F251"
                                         "]+", flags=re.UNICODE)

    def remove_nonlatin(self, s):
        """
        remove non ascii character but keep accent

        Args:
            s (string): text

        Returns:
            string: text without non ascii char
        """
        s = (ch for ch in s
             if unicodedata.name(ch).startswith(('LATIN', 'DIGIT', 'SPACE')))
        return ''.join(s)

    def remove_emoji(self, text):
        """
        remove the emojis and non ascii char with space from the tweet

        Args:
            text (string): text to clean

        Returns:
            string: cleaned text
        """
        # after tweepy preprocessing the colon symbol left remain after
        # removing mentions
        text = re.sub(r':', '', text)
        text = re.sub(r'‚Ä¶', '', text)
        # replace consecutive non-ASCII characters with a space
        text = ' '.join(
            re.findall(
                r'[\u0020-\u007F\u00A0-\u00FF\u0100-\u017F\u0180-\u024F]+',
                text))
        # remove emojis from tweet
        text = self.emoji_pattern.sub(r'', text)
        return text

    def stematise_token(self, tokens):
        """
        replace word in token list  with his lemma:
        example : appelais  will become appele, plural will be replaced by their singular version, etc
        """

        doc = french_stematiser(' '.join(tokens))
        return [token.lemma_ for token in doc]

    def prepocess_tweet(self, tweet):
        """
        Apply all the preprocessing process on a tweet and return the tweet as a text and tweet as list of tokens

        Args:
            tweet (object): tweet object to process

        Returns:
            list : list of tokens from the tweet
        """
        text = tweet_preprocessor.clean(tweet.get('text'))
        text = text.replace('#', '')
        text = text.replace('-', '')
        text = text.replace("«", "")
        text = text.replace("»", "")
        text = text.replace("_", "")
        text = re.sub(r"\b\w{1}\b", "", text)
        text = re.sub(r"\b\w{2}\b", "", text)
        text = remove_emoji(text)
        tokens = process_text(text=text, words_to_remove=self.words_to_remove)
        tokens = self.stematise_token(tokens)
        return tokens

    def create_cleaned_tweet(self):
        """
        apply the whole cleaning pipeline
        Returns :
        dataframe : cleanned tweets
        """
        now = datetime.now()
        today = now.strftime("%d-%m-%Y-%H-%M")
        output_file_name = '../data/cleanned_tweets_{}.csv'.format(today)
        tweets_df = pd.DataFrame(columns=['cleanned_tweet'])
        for tweet in read_tweets_file(self.TWEETS_PATH):
            tweets_df.loc[tweet.get('id')] = [
                ' '.join(self.prepocess_tweet(tweet))]
        tweets_df.to_csv(output_file_name)
        return tweets_df
