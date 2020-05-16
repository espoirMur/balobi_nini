from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
from rx import Observable
from twitter_client import get_twitter_auth, get_twitter_client
from twitter_query_data import get_location
from mongo_db_client import insert_tweet


def tweet_for(topics: list, locations=None):
    def observe_tweets(observable):
        class TweetListener(StreamListener):
            def on_data(self, data):
                insert_tweet(json.loads(data))
                observable.on_next(data)
                return True

            def on_error(self, status):
                if status == 420:
                    observable.on_error(status)
                    sys.stderr.write("Rate limit exceeded\n".format(status))
                    return False
                else:
                    sys.stderr.write("Error {}\n".format(status))
                    return True

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
coordinates = get_location(get_twitter_client(), 'Congo').get('coordinates')
location_tweets = tweet_for(topics=[], locations=[11.94, -13.64, 30.54, 5.19])
hash_tag_tweets = tweet_for(topics=topics)
place_id_tweet = tweet_for(topics=topics, locations=coordinates)
combine_loc_hash_tag = Observable.merge(hash_tag_tweets)

(
    combine_loc_hash_tag.subscribe()

)
