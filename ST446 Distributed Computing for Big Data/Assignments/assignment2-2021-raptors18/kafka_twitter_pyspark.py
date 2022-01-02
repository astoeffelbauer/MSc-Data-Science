#!/usr/bin/env python

# based on examples/src/main/python/streaming/kafka_wordcount.py

from __future__ import print_function

import sys
import nltk
import json

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string

stop_words = set(stopwords.words('english'))

def returnText(x):
    try:
        return x['text']
    except:
        return ""


def get_tokens(line):
    tokens = word_tokenize(line)
    # convert to lower case
    tokens = [w.lower() for w in tokens]
    # remove punctuation from each word
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    # stripped = tokens
    # remove remaining tokens that are not alphabetic
    words = [word for word in stripped if word.isalpha()]
    # filter out stop words
    words = [w for w in words if not w in stop_words]
    return words


# for debugging:
def testmap(line):
    return word_tokenize(line)

# helper functions
mean = lambda m, x, w: (1-w)*m + w*x
var = lambda sig2, m, x, a, b: a*sig2 + b*(x-m)**2


if __name__ == "__main__":

    topic = 'twitter-stream'

    sc = SparkContext()
    ssc = StreamingContext(sc, 1) # 1 second intervals!
    ssc.checkpoint("checkpoint")

    zkQuorum = "localhost:2181"
    kafka_stream = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: 1})
    lines = kafka_stream.map(lambda x: json.loads(x[1])).map(returnText)

    # RDD with initial state (key, value) pairs
    initialStateRDD = sc.parallelize([(u'state', (20, 40, 20, 40, 1))])

    def updateFunc(new_values, last_state):

        word_counts = new_values
        mean_decay, var_decay, mean_smooth, var_smooth, count = last_state

        ####### PART 1: DECAY
        for word_count in word_counts:
            a = count / (count+1) # (count-1) / count
            b = count / (count+1)**2 # 1 / (count + 1)
            w = 1 / (count + 1)

            var_decay = var(var_decay, mean_decay, word_count, a, b)
            mean_decay = mean(mean_decay, word_count, w)
            count += 1

        ####### PART 2: SMOOTHING
        a = 0.8
        b = 0.2
        w = 0.2

        for word_count in word_counts:
            var_smooth = var(var_smooth, mean_smooth, word_count, a, b)
            mean_smooth = mean(mean_smooth, word_count, w)

        return (mean_decay, var_decay, mean_smooth, var_smooth, count)


    online_values = lines.map(get_tokens)\
        .map(len)\
        .map(lambda tweet_len: (u'state', tweet_len))\
        .updateStateByKey(updateFunc, initialRDD=initialStateRDD)

    online_values.pprint()

    ssc.start()
    ssc.awaitTermination()
