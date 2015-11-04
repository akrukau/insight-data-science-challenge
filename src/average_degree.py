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

class Graph:
    def __init__(self):
        self.adj = {}

    def add(self, vertex1, vertex2):
        vertex1 = vertex1.lower()
        vertex2 = vertex2.lower()

        if vertex1 not in self.adj:
            self.adj[vertex1] = [vertex2]
        elif vertex2 not in self.adj[vertex1]: 
                self.adj[vertex1].append(vertex2)

        if vertex2 not in self.adj:
            self.adj[vertex2] = [vertex1]
        elif vertex2 not in self.adj[vertex1]: 
            self.adj[vertex2].append(vertex1) 

    def remove(self, vertex1):
        vertex1 = vertex1.lower()
        if vertex1 in self.adj:
            adjacent_vertices = self.adj[vertex1]
            for vertex2 in adjacent_vertices:
                try:
                    self.adj[vertex2].remove(vertex1)
                except ValueError:
                    pass
                except KeyError:
                    print "Key",vertex2,"is not found in:"
                    self.show()
            self.adj.pop(vertex1, None)
            
    def show(self):
        for vertex in self.adj:
            print "Vertex:",vertex,"-",self.adj[vertex]
                

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
    print "Adding tweet",tweet_entry
    if (len(tags) >= 2):
        graph.add(tags[0], tags[1])
    heappush(heap, tweet_entry)
    graph.show()    
    print 
    return timestamp

def remove_old_tweets(heap, graph, current_time):
    while heap:        
        oldest_time = heap[0][0]
        time_dif = current_time - oldest_time
        if time_dif.days == 0 and time_dif.seconds <= 60:
            break
        tweet = heappop(heap)
        tags = tweet[1]
        for tag in tags:
            graph.remove(tag)
        print "Removing old tweet", tweet
        graph.show()
        print 

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

            

