#!/usr/bin/env python


# import required libraries
from kafka import KafkaProducer, KafkaClient
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import time
import traceback

# update the following to your own key and token
consumer_key = "key"
consumer_secret = "key"
access_token = "key"
access_token_secret = "key"

# Kafka settings
topic = 'twitter-stream'
# setting up Kafka producer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
# setting up the keywords
search_kw = ["London"]

#This is a basic listener that just sends received tweets to kafka
class StdOutListener(StreamListener):
    def on_data(self, data):
        producer.send(topic, data.encode('utf-8'))
        print(len(data))
        return True

    def on_error(self, status):
        print(status)
        return False

if __name__ == '__main__':
    print('running the twitter-stream python code')
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    public_tweets = api.home_timeline()
    stream = Stream(auth, l)
    # Goal is to keep this process always going
    while True:
        try:
           # stream.sample()
           stream.filter(track=search_kw)
        except:
           print(traceback.format_exc())
        time.sleep(10)
