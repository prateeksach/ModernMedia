""" 
You guys will be using a REST API from python/scraping script to fetch the list of URLs to scrape
(urls are stored in parse DB). And then update Parse as you scrape each link so we can remember it
(also through a REST API). So while you're working on it, make a fake request that sends you a list
of URLs and continue from there while I make the API for you tonight.
"""


# Using newspaper library. Download and install from http://newspaper.readthedocs.org/en/latest/
import newspaper 
import os, sys
import datetime

# install ParsePy library: https://github.com/dgrtwo/ParsePy.git
from parse_rest.connection import register, ParseBatcher
from parse_rest.datatypes import Object as ParseObject


# Function getURL which pulls some URL out of a database. Returns a url.
# Parse to python tutorial is found here: https://github.com/dgrtwo/ParsePy
"""
def saveToParse(urlDictionary):

        batcher = ParseBatcher()
        batcher.batchsave(urlDictionary)

def queryFromParse(AllURLs,read_query):
        # Assumed that database contains table with fields: url, read_status
        # url contains the urls, read_status indicates "read" or "unread"
        urlquery = list(ParseObject.Query.filter(read_status == read_query))
        return urlquery



"""

if __name__ == '__main__':

        """
        APPLICATION_ID = "ENTER_APP_ID"
        REST_API_KEY = "ENTER REST API KEY"
        register(APPLICATION_ID, REST_API_KEY)
        
        # Instantiate parse.com object imported as ParseObject
        class AllURLs(ParseObject):
                pass

        # Get a list of unread URLs
        unreadURL = queryFromParse(AllURLs, "unread")

        for url in unreadURL.keys():
        ### DO THE SCRAPING BELOW.

        """

	# Output of getURL() goes here. Using a temporary URL to scrape.
	url = "http://www.cnn.com/2015/03/23/world/isis-luring-westerners/index.html"

	art = newspaper.Article(url)
	art.download()
	art.parse()

	art_txt = art.text

        """
        unreadURL[url] = "read"
        ### DONE.
        """
	# art_txt -> ML algorithms for text processing. 

        """
        # Update the parse database indicating that URL has been read
        savetoParse(unreadURL)

        
