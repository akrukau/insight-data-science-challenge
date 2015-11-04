#!/usr/bin/python
#
# example of program that calculates the average degree of hashtags
#
# Created by Aliaksandr Krukau, 11/3/2015 
#
# Requires Python 2.7 because of "with" statement for two files
#
import json
import sys
from email.utils import parsedate_tz
from datetime import datetime, timedelta
from heapq import heappush, heappop
from text_utilities import clean_string

def extract_time(timestamp_string):
    time_tuple = parsedate_tz(timestamp_string.strip())
    raw_time = datetime(*time_tuple[:6])
    timezone_correction = timedelta(seconds = time_tuple[-1]) 
    return raw_time - timezone_correction

def add_tweet(heap, tweet):
    timestamp_string = tweet["created_at"]
    timestamp = extract_time(timestamp_string)
    #print timestamp
    tweet_entry = (timestamp, tags)   
    print "Adding tweet",tweet_entry
    heappush(heap, tweet_entry)
    return timestamp

def remove_old_tweets(heap, current_time):
    while heap:        
        oldest_time = heap[0][0]
        time_dif = current_time - oldest_time
        if time_dif.days == 0 and time_dif.seconds <= 60:
            break
        tweet = heappop(heap)
        print "Removing old tweet", tweet

with open('../data-gen/short-tweets.txt', 'rb') as input_file:
#with open('../data-gen/tweets.txt', 'rb') as input_file:
    heap = []
    for line in input_file:
        try:
            tweet = json.loads(line)
            tags = []
            if "entities" in tweet and "hashtags" in tweet["entities"]:
                for entry in tweet['entities']['hashtags']:
                    if "text" in entry:
                        tags.append(entry["text"])
            if "created_at" in tweet:
                current_time = add_tweet(heap, tweet)
                remove_old_tweets(heap, current_time)

        except ValueError:
            sys.stderr.write("The following line is not valid JSON\n")
            sys.stderr.write(line)
        #except:
        #    sys.stderr.write("The following line could not be parsed\n")
        #    sys.stderr.write(line)

            

