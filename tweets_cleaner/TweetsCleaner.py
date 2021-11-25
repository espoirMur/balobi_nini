import re
import unicodedata
import many_stop_words
import spacy
import preprocessor as tweet_preprocessor
from utils.functions import process_text, get_words_to_remove
from utils.emoticons import emoticons
from datetime import datetime
from app.model import CleannedTweet

french_lematizer = spacy.load("fr_core_news_sm")

tweet_preprocessor.set_options(tweet_preprocessor.OPT.URL,
                               tweet_preprocessor.OPT.EMOJI,
                               tweet_preprocessor.OPT.RESERVED,
                               tweet_preprocessor.OPT.EMOJI,
                               tweet_preprocessor.OPT.SMILEY,
                               tweet_preprocessor.OPT.NUMBER,
                               tweet_preprocessor.OPT.MENTION)


class TweetsCleaner:

    def __init__(self):
        self.words_to_remove = get_words_to_remove().union(emoticons)
        self.emoji_patterns = re.compile("["
                                         u"\U0001F600-\U0001F64F"  # emoticons
                                         u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                         u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                         # flags (iOS)
                                         u"\U0001F1E0-\U0001F1FF"
                                         u"\U00002702-\U000027B0"
                                         u"\U000024C2-\U0001F251"
                                         "]+", flags=re.UNICODE)

    def remove_accents(self, input_str):
        """
        remove accent from the text, please refer to this code for more info, thanks for the author
        :https://stackoverflow.com/a/517974/4683950
        """
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        only_ascii = nfkd_form.encode('ASCII', 'ignore')
        return only_ascii.decode('utf-8')

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
        text = self.emoji_patterns.sub(r'', text)
        return text

    def lematize_token(self, tokens):
        """
        replace word in token list  with his lemma:
        example : appelais  will become appele,
         plural will be replaced by their singular version, etc
        """

        doc = french_lematizer(' '.join(tokens))
        return [token.lemma_ for token in doc]

    def prepocess_tweet(self, tweet_text, remove_emojis=True, remove_accents=True):
        """
        Apply all the preprocessing process on a tweet and return the tweet as a text and tweet as list of tokens

        Args:
            tweet (object): tweet object to process

        Returns:
            list : list of tokens from the tweet_text
        """
        if remove_accents:
            text = self.remove_accents(tweet_text)
        text = tweet_preprocessor.clean(text)
        text = text.replace('#', '')
        text = text.replace('-', '')
        text = text.replace("«", "")
        text = text.replace("»", "")
        text = text.replace("_", "")
        text = re.sub(r"\b\w{1}\b", "", text)
        text = re.sub(r"\b\w{2}\b", "", text)
        if remove_emojis:
            text = self.remove_emoji(text)
        tokens = process_text(text=text, words_to_remove=self.words_to_remove)
        tokens = self.lematize_token(tokens)
        return tokens

    def save_clean_tweets(self, tweets):
        """get raw tweets , clean them
           and return cleaned tweets
        Args:
            tweets ([type]): [description]
        """
        for tweet in tweets:
            cleaned_tweet = self.prepocess_tweet(tweet.get('text'))
            tweet_date = datetime.fromtimestamp(tweet.get('created_at')),
            cleaned_tweet_model = CleannedTweet(
                id=tweet.get('id'),
                text=" ".join(cleaned_tweet),
                created_at=tweet_date,
                raw_json=tweet)
            cleaned_tweet_model.save_to_database()
