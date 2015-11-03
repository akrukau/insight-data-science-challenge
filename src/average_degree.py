#!/usr/bin/python
#
# example of program that calculates the average degree of hashtags
#
# Created by Aliaksandr Krukau, 11/2/2015 
#
# Requires Python 2.7 because of "with" statement for two files
#
import Queue
import json
import sys
import re

def clean(text):
    #Remove all non-ascii characters that correspond to \uxxxx sequences
    (cleaned_text, unicode_deletions) = re.subn(r'[^\x00-\x7F]','', text)
    tweet_has_unicode = False
    if unicode_deletions > 0:
        tweet_has_unicode = True
    #Change all whitespace to a single space, as mentioned in FAQ
    (cleaned_text, whitespace_changes) = re.subn(r'[\"\\\b\f\n\r\t]',' ', cleaned_text)
    return (cleaned_text, tweet_has_unicode)


with open('../data-gen/short-tweets.txt', 'rb') as input_file:
    heap = Queue.PriorityQueue()
    for line in input_file:
        try:
            tweet = json.loads(line)
            tags = []
            if "entities" in tweet and "hashtags" in tweet["entities"]:
                tags.append(tweet['entities']['hashtags'])
            if "created_at" in tweet:
                timestamp = tweet["created_at"]
            tweet_entry = (timestamp, tags[0])   
            heap.put(tweet_entry)               

        except:
            sys.stderr.write("We suspect that the following line is not valid JSON\n")
            sys.stderr.write(line)

    while not heap.empty():        
        tweet = heap.get()
        print tweet
            

