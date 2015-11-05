#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import unittest

def clean_string(text):
    '''Removes non-ascii characters and changes whitespace to space character'''
    #Remove all non-ascii characters that correspond to \uxxxx sequences
    (cleaned_text, unicode_deletions) = re.subn(r'[^\x00-\x7F]','', text)
    tweet_has_unicode = False
    if unicode_deletions > 0:
        tweet_has_unicode = True

    #Change all whitespace to a single space, as mentioned in FAQ
    cleaned_text = re.sub(r'[\b\f\n\r\t]',' ', cleaned_text)
    #Delete the rest of non-ascii characters
    cleaned_text = re.sub(r'[^\x20-\x7F]',' ', cleaned_text)
    return (cleaned_text, tweet_has_unicode)

class TestCleanString(unittest.TestCase):
  def test_whitespace(self):
      text_index = 0
      self.assertEqual(clean_string('Hello\b\f\n\r\tWorld!')[text_index], 'Hello     World!')

  def test_unicode(self):
      text_index = 0
      self.assertEqual(clean_string('日本へようこそ!')[text_index], '!')

if __name__ == '__main__':
    unittest.main()

