import json
from pprint import pprint


with open('tweets.txt') as input_file:
    tags = []
    #print tweet
    #print tweet["entities"]["hashtags"]
    count = 0
    for line in input_file:
        tweet = json.loads(line)
        if "entities" in tweet and "hashtags" in tweet["entities"]:
        #if "entities" in tweet:
            #data.append(tweet["entities"]["hashtags"])
            tags.append(tweet['entities']['hashtags'])
            count +=1 

    #print "Count",count

    #for tag in tags: 
    #    if len(tag) > 1:
    #        pass
            #print tag
        
