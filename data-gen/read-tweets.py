import json
from pprint import pprint


with open('tweets.txt') as input_file:
    tags = []
    #print tweet
    #print tweet["entities"]["hashtags"]
    count = 0
    for line in input_file:
        tweet = json.loads(line)
        tags = []
        if "entities" in tweet and "hashtags" in tweet["entities"]:
        #if "entities" in tweet:
            #data.append(tweet["entities"]["hashtags"])
            tags.append(tweet['entities']['hashtags'])
            count +=1 
            tag_json_array = tweet['entities']['hashtags']
            for tag_json in tag_json_array:
                if "text" in tag_json:
                    tags.append(tag_json["text"])

    #print "Count",count

    #for tag in tags: 
    #    if len(tag) > 1:
    #        pass
            #print tag
        
