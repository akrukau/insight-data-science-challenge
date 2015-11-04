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
from collections import Counter
from text_utilities import clean_string

class Graph:
    def __init__(self):
        self.edges = Counter()
        self.degrees = Counter()

    def add_edges(self, tags):
        # Input tags are in mixed case
        # Make all tags lowercase and remove repeated tags.
        tags = set( map(lambda s: s.lower(), tags) )
        if (len(tags) >= 2):
            for i in tags:
                for j in tags:
                    if i != j:
                        self.edges[(i, j)] += 1
                        if self.edges[(i, j)] == 1:
                            self.degrees[i] += 1


    def remove_edges(self, tags):
        # Input tags are all lowercase
        if (len(tags) >= 2):
            for i in tags:
                for j in tags:
                    if i != j:
                        self.edges[(i, j)] -= 1
                        if self.edges[(i, j)] == 0:
                            self.degrees[i] -= 1
                            if self.degrees <= 0:
                                self.vertex_count -= 1

    def show_edges(self):
        print "Graph", self.edges    
    
    def show_degrees(self):
        for vertex in self.degrees:
            print "Vertex", vertex, "degree", self.degrees[vertex]
            print 

    def average_degree(self):
        #print "Graph", self.edges  
        vertex_count = sum(1 for v in self.degrees if self.degrees[v] > 0)
        sum_degrees  = sum(self.degrees[v] for v in self.degrees)
        if vertex_count > 0:
            average_degree = 1.0 * sum_degrees / vertex_count
        else:    
            average_degree = 0.0
        info_average_degree = "Average degree " + "{0:.2f}".format(average_degree)    
        #print "Vertex count",vertex_count
        #print "Degree count",sum_degrees
        print info_average_degree
        print 

    def dump(self):
        self.show_edges()
        self.show_degrees()
        self.average_degree()

def extract_time(timestamp_string):
    tuple_time = parsedate_tz(timestamp_string.strip())
    raw_time = datetime(*tuple_time[:6])
    timezone_correction = timedelta(seconds = tuple_time[-1]) 
    return raw_time - timezone_correction

def add_tweet(heap, graph, tweet):
    timestamp_string = tweet["created_at"]
    timestamp = extract_time(timestamp_string)
    tags = []
    if "entities" in tweet and "hashtags" in tweet["entities"]:
        for entry in tweet['entities']['hashtags']:
            if "text" in entry:
                tags.append(entry["text"].lower())
    tweet_entry = (timestamp, tags)
    heappush(heap, tweet_entry)
    print "Adding tweet",tweet_entry
    graph.add_edges(tags)

    graph.dump()
       
    return timestamp

def remove_old_tweets(heap, graph, current_time):
    while heap:        
        oldest_time = heap[0][0]
        time_dif = current_time - oldest_time
        if time_dif.days == 0 and time_dif.seconds <= 60:
            break
        tweet = heappop(heap)
        tags = tweet[1]
        print "Removing old tweet", tweet
        graph.remove_edges(tags)

        graph.dump()

with open('../data-gen/short-tweets.txt', 'rb') as input_file:
#with open('../data-gen/tweets.txt', 'rb') as input_file:
    heap = []
    graph = Graph()
    for line in input_file:
        try:
            tweet = json.loads(line)
            if "created_at" in tweet:
                current_time = add_tweet(heap, graph, tweet)
                remove_old_tweets(heap, graph, current_time)
        except ValueError:
            sys.stderr.write("The following line is not valid JSON\n")
            sys.stderr.write(line)
        #except:
        #    sys.stderr.write("The following line could not be parsed\n")
        #    sys.stderr.write(line)

            

