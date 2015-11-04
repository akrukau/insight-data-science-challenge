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
import re
from datetime import datetime, timedelta
from email.utils import parsedate_tz
from heapq import heappush, heappop

def clean(text):
    #Remove all non-ascii characters that correspond to \uxxxx sequences
    (cleaned_text, unicode_deletions) = re.subn(r'[^\x00-\x7F]','', text)
    tweet_has_unicode = False
    if unicode_deletions > 0:
        tweet_has_unicode = True
    #Change all whitespace to a single space, as mentioned in FAQ
    (cleaned_text, whitespace_changes) = re.subn(r'[\"\\\b\f\n\r\t]',' ', cleaned_text)
    return (cleaned_text, tweet_has_unicode)

def extract_time(timestamp_string):
    time_tuple = parsedate_tz(timestamp_string.strip())
    raw_time = datetime(*time_tuple[:6])
    timezone_correction = timedelta(seconds = time_tuple[-1]) 
    return raw_time - timezone_correction

#with open('../data-gen/short-tweets.txt', 'rb') as input_file:
with open('../data-gen/tweets.txt', 'rb') as input_file:
    heap = []
    for line in input_file:
        try:
            tweet = json.loads(line)
            tags = []
            if "entities" in tweet and "hashtags" in tweet["entities"]:
                tags.append(tweet['entities']['hashtags'])
            if "created_at" in tweet:
                timestamp_string = tweet["created_at"]
                timestamp = extract_time(timestamp_string)
                #print timestamp
                tweet_entry = (timestamp, tags)   
                heappush(heap, tweet_entry)


        except IndexError:
            sys.stderr.write("We suspect that the following line is not valid JSON\n")
            sys.stderr.write(line)

    while heap:        
        tweet = heappop(heap)
        #print tweet
            

