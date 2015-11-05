import re

def clean_string(text):
    '''Removes non-ascii characters and changes whitespace to space character'''
    #Remove all non-ascii characters that correspond to \uxxxx sequences
    (cleaned_text, unicode_deletions) = re.subn(r'[^\x00-\x7F]','', text)
    tweet_has_unicode = False
    if unicode_deletions > 0:
        tweet_has_unicode = True

    #Change all whitespace to a single space, as mentioned in FAQ
    (cleaned_text, whitespace_changes) = re.subn(r'[\b\f\n\r\t]',' ', cleaned_text)
    return (cleaned_text, tweet_has_unicode)

