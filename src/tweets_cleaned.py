#!/usr/bin/python
#
# example of program that calculates the number of tweets cleaned
#
import json
import re
from pprint import pprint

with open('../data-gen/tweets.txt', 'rb') as input_file:
    #p = re.compile(r'(\"text:\"'))
    #re.findall(p, line)
    count_tweets_unicode = 0
    for line in input_file:
        # Remove all \uxxxx sequences
        (line, deletions) = re.subn(r"\\u[0-9a-f]{4}", "", line) 
        if deletions > 0:
            count_tweets_unicode += 1

        tweet = json.loads(line)
        cleaned_text = ""
        if "text" in tweet:
            #cleaned_tweet += ''.join([ char for char in tweet["text"] if ord(char) <= 255 ])  
            cleaned_text = tweet["text"]
            #cleaned_text = cleaned_text.encode('unicode-escape') 

        timestamp = ""
        if "created_at" in tweet:
            timestamp = tweet["created_at"] 

        cleaned_tweet = cleaned_text + " (timestamp: " + timestamp + ")" 
        print cleaned_tweet

    print
    print count_tweets_unicode, "tweets contained unicode."

