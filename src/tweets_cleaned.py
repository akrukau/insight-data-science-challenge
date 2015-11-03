#!/usr/bin/python
#
# example of program that calculates the number of tweets cleaned
#
import json
from pprint import pprint

def _decode_list(data):
    rv = []
    for item in data:
        #if isinstance(item, unicode):
        #    item = item.encode('utf-8')
        if isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv

def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        #if isinstance(key, unicode):
        #    key = key.encode('utf-8')
        #if isinstance(value, unicode):
        #    value = value.encode('utf-8')
        if isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv

with open('../data-gen/tweets.txt', 'rb') as input_file:
    for line in input_file:
        tweet = json.loads(line, object_hook = _decode_dict)
        cleaned_tweet = ""

        if "text" in tweet:
            #cleaned_tweet += ''.join([ char for char in tweet["text"] if ord(char) <= 255 ])  
            cleaned_text = tweet["text"]
            #cleaned_text = cleaned_text.encode('unicode-escape') 
            cleaned_tweet += cleaned_text

        print cleaned_tweet       


