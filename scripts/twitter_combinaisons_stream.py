from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
from rx import Observable
from twitter_client import get_twitter_auth, get_twitter_client
from twitter_query_data import get_location


def tweet_for(topics: list, locations=None):
    def observe_tweets(observable):
        class TweetListener(StreamListener):
            def on_data(self, data):
                print('data comming ===>')
                observable.on_next(data)
                return True

            def on_error(self, http_status):
                observable.on_error(http_status)

        tweet_listener = TweetListener()
        auth = get_twitter_auth()

        stream = Stream(auth, tweet_listener)
        stream.filter(track=topics, locations=locations)

    return Observable.create(observe_tweets).share()


topics = [
    'RDC',
    'RDCongo',
    'DRC',
    'DRCongo',
]
place_id = get_location(get_twitter_client(), 'Congo')
location_tweets = tweet_for(topics=[], locations=[11.94, -13.64, 30.54, 5.19])
hash_tag_tweets = tweet_for(topics=topics)
place_id_tweet = tweet_for(topics=place_id)
combine_loc_hash_tag = Observable.merge( hash_tag_tweets, place_id_tweet)

(
    combine_loc_hash_tag.map(json.loads).subscribe(
        lambda tweet_data: print(f"🐦 -> : {tweet_data.get('text')} \n\n")
    )
)
