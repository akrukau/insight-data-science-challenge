#!/usr/bin/python
#
# example of program that calculates the number of tweets cleaned
# Created by Aliaksandr Krukau, 11/2/2015
#
import json
import re

with open('../data-gen/tweets.txt', 'rb') as input_file:
    count_tweets_unicode = 0

    for line in input_file:
        tweet = json.loads(line)
        if "text" in tweet:
            text = tweet["text"]
            
            #Remove all non-ascii characters that correspond to \uxxxx sequences
            (cleaned_text, unicode_deletions) = re.subn(r'[^\x00-\x7F]','', text)
            #Remove all characters represented by two-character escape sequence
            (cleaned_text, escape_deletions) = re.subn(r'[\"\\\b\f\n\r\t]','', cleaned_text)
            if unicode_deletions > 0:
                count_tweets_unicode += 1

            timestamp = ""
            if "created_at" in tweet:
                timestamp = tweet["created_at"] 

            cleaned_tweet = cleaned_text + " (timestamp: " + timestamp + ")" 
            print cleaned_tweet

    print
    print count_tweets_unicode, "tweets contained unicode."

