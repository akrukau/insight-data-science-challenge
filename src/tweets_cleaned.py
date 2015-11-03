#!/usr/bin/python
#
# example of program that calculates the number of tweets cleaned
#
# Created by Aliaksandr Krukau, 11/2/2015 
#
# Requires Python 2.7 because of "with" statement for two files
#
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


#with open('./example-wrong.txt', 'rb') as input_file:
if len(sys.argv) < 3:
    print "Error: too few arguments"
    print "Usage: ./tweets_cleaned.py input_file output_file"
else:
    with open(sys.argv[1], 'rb') as input_file, open(sys.argv[2], 'wb') as output_file:
        count_tweets_unicode = 0

        for line in input_file:
            try:
                tweet = json.loads(line)
                if "text" in tweet:
                    text = tweet["text"]
                    (cleaned_text, tweet_has_unicode) = clean(text)
                    if tweet_has_unicode:
                        count_tweets_unicode += 1
            
                    timestamp = ""
                    if "created_at" in tweet:
                        timestamp = tweet["created_at"] 
            
                    cleaned_tweet = cleaned_text + " (timestamp: " + timestamp + ")\n" 
                    output_file.write(cleaned_tweet)
            
            except:
                sys.stderr.write("The following line is not valid JSON\n")
                sys.stderr.write(line)
        
        summary =  "\n" + str(count_tweets_unicode) + " tweets contained unicode."
        output_file.write(summary)
            

