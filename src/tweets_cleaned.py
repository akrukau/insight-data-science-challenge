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
from text_utilities import clean_string

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
                    (cleaned_text, tweet_has_unicode) = clean_string(text)
                    if tweet_has_unicode:
                        count_tweets_unicode += 1
            
                    timestamp = ""
                    if "created_at" in tweet:
                        timestamp = tweet["created_at"] 
            
                    cleaned_tweet = cleaned_text + " (timestamp: " + timestamp + ")\n" 
                    output_file.write(cleaned_tweet)
            
            except ValueError:
                sys.stderr.write("The following line is not valid JSON\n")
                sys.stderr.write(line)
            #except:
            #    sys.stderr.write("The following line could not be parsed\n")
            #    sys.stderr.write(line)
        
        summary =  "\n" + str(count_tweets_unicode) + " tweets contained unicode."
        output_file.write(summary)
            

