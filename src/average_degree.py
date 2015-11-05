#!/usr/bin/python
#
# example of program that calculates the average degree of hashtags
#
# Created by Aliaksandr Krukau
# Started on 11/3/2015 
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
        self.sum_degrees = 0
        self.number_vertices = 0

    def add_edges(self, tags):
        if (len(tags) >= 2):
            pairs_tags = [(i, j) for i in tags for j in tags if i != j]
            for (i, j) in pairs_tags:
                self.edges[(i, j)] += 1
                if self.edges[(i, j)] == 1:
                    self.sum_degrees += 1
                    self.degrees[i] += 1
                    if self.degrees[i] == 1:
                        self.number_vertices += 1
        #if self.sum_degrees > 0:
        #    print
        #    print "Tweet is",tags



    def remove_edges(self, tags):
        # Input tags are all in lowercase ascii characters.
        if (len(tags) >= 2):
            pairs_tags = [(i, j) for i in tags for j in tags if i != j]
            for (i, j) in pairs_tags:
                self.edges[(i, j)] -= 1
                if self.edges[(i, j)] == 0:
                    self.sum_degrees -= 1
                    self.degrees[i] -= 1
                    if self.degrees[i] == 0:
                        self.number_vertices -= 1

    def show_edges(self):
        print "Graph", self.edges    
    
    def show_degrees(self):
        for vertex in self.degrees:
            print "Vertex", vertex, "degree", self.degrees[vertex]

    def average_degree(self):
        #print "Graph", self.edges  
        #number_vertices = sum(1 for v in self.degrees if self.degrees[v] > 0)
        #sum_degrees  = sum(self.degrees[v] for v in self.degrees)
        #if vertex_count > 0:
        if self.number_vertices > 0:
            average_degree = 1.0 * self.sum_degrees / self.number_vertices
            #average_degree = 1.0 * sum_degrees / number_vertices
        else:    
            average_degree = 0.0
        #info_average_degree = "Average degree " + "{0:.2f}".format(average_degree)    
        info_average_degree = "{0:.2f}".format(average_degree)    
        #if self.sum_degrees > 0:
        #    self.show_degrees()
        print info_average_degree
        return average_degree

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
            # Input tags are in mixed case Unicode (created by json module).
            # Clean text from non-ascii characters and escaped whitespace.
            # Then make all tags lowercase and remove empty tags.
            if "text" in entry:
                cleaned_text =  clean_string(entry["text"])[0].lower()
                if cleaned_text:
                    tags.append(cleaned_text)
    tags = set(tags)                
    tweet_entry = (timestamp, tags)
    heappush(heap, tweet_entry)
    #print "Adding tweet",tweet_entry
    graph.add_edges(tags)

    #graph.dump()
       
    return timestamp

def remove_old_tweets(heap, graph, current_time):
    while heap:        
        oldest_time = heap[0][0]
        time_dif = current_time - oldest_time
        if time_dif.days == 0 and time_dif.seconds <= 60:
            break
        tweet = heappop(heap)
        tags = tweet[1]
        #print "Removing old tweet", tweet
        graph.remove_edges(tags)


#with open('../data-gen/example-github.txt', 'rb') as input_file:
with open('../data-gen/tweets.txt', 'rb') as input_file:
    heap = []
    graph = Graph()
    for line in input_file:
        try:
            tweet = json.loads(line)
            if "created_at" in tweet:
                current_time = add_tweet(heap, graph, tweet)
                remove_old_tweets(heap, graph, current_time)
                #graph.show_degrees()
                ans = graph.average_degree()


        except ValueError:
            sys.stderr.write("The following line is not valid JSON\n")
            sys.stderr.write(line)
        #except:
        #    sys.stderr.write("The following line could not be parsed\n")
        #    sys.stderr.write(line)

            

