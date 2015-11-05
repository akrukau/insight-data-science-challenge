#!/usr/bin/python
#
# Program that created the graph of Twitter hashtags 
# and calculates the average degree of vertices at each iteration.
#
# Requires Python 2.7 because of "with" statement for two files
#
# Created by Aliaksandr Krukau
# Started on 11/3/2015 
#
import json
import sys
from email.utils import parsedate_tz
from datetime import datetime, timedelta
from heapq import heappush, heappop
from text_utilities import clean_string
from graph import Graph

def extract_time(timestamp_string):
    """Return the datetime object based on timestamp_string"""
    tuple_time = parsedate_tz(timestamp_string.strip())
    raw_time = datetime(*tuple_time[:6])
    timezone_correction = timedelta(seconds = tuple_time[-1]) 
    return raw_time - timezone_correction


def add_tweet(heap, graph, tweet, timestamp, debug):
    """
    Adds tweet to heap and to graph
    
    Heap stores all tweets with timestamp as a key.
    The top of the heap is the oldest tweet.
    Graph stores information about all edges between tweets.
    """
    tags = []
    if "entities" in tweet and "hashtags" in tweet["entities"]:
        for entry in tweet['entities']['hashtags']:
            # Input tags are in mixed case Unicode (created by json module).
            # Clean text from non-ascii characters and escaped whitespace.
            # Then make all tags lowercase and remove empty or space only tags.
            if "text" in entry:
                cleaned_text =  clean_string(entry["text"])[0].lower()
                if cleaned_text or cleaned_text.isspace():
                    tags.append(cleaned_text)
    tags = set(tags)                
    tweet_entry = (timestamp, tags)
    heappush(heap, tweet_entry)
    graph.add_edges(tags)
    
    if debug and len(tags) > 1:
        print "Adding tweet",tweet_entry


def remove_old_tweets(heap, graph, current_time, debug):
    """Removes the tweets that are 61 seconds or more before current_time"""
    index_top = 0
    index_time = 0
    while heap:        
        oldest_time = heap[index_top][index_time]
        time_dif = current_time - oldest_time
        if time_dif.days == 0 and time_dif.seconds <= 60:
            break
        tweet = heappop(heap)
        tags = tweet[1]
        graph.remove_edges(tags)

        if debug:
            print "Removing old tweet", tweet
            graph.show_edges()


#with open('../data-gen/example-github.txt', 'rb') as input_file:
#with open('../tweet_input/oct-15-2011.txt', 'rb') as input_file:
#with open('../data-gen/tweets.txt', 'rb') as input_file:
with open('./changed-example-github.txt', 'rb') as input_file:
    debug = True
    heap = []
    graph = Graph()
    for line in input_file:
        try:
            tweet = json.loads(line)
            if "created_at" in tweet:
                timestamp_string = tweet["created_at"]
                timestamp = extract_time(timestamp_string)
                add_tweet(heap, graph, tweet, timestamp, debug)
                remove_old_tweets(heap, graph, timestamp, debug)
                if debug:
                    graph.show_degrees()
                average_degree = graph.average_degree()
                print "{0:.2f}".format(average_degree) 

        except ValueError:
            sys.stderr.write("The following line is not valid JSON\n")
            sys.stderr.write(line)

        #except Exception as error:
        #    sys.stderr.write(error.message)
        #    sys.stderr.write("Error trying to process the line\n")
        #    sys.stderr.write(line)

            

