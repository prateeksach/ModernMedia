""" 
You guys will be using a REST API from python/scraping script to fetch the list of URLs to scrape
(urls are stored in parse DB). And then update Parse as you scrape each link so we can remember it
(also through a REST API). So while you're working on it, make a fake request that sends you a list
of URLs and continue from there while I make the API for you tonight.
"""


# Using newspaper library. Download and install from http://newspaper.readthedocs.org/en/latest/
import newspaper 

# Function getURL which pulls some URL out of a database. Returns a url.

if __name__ == '__main__':

    # Output of getURL() goes here. Using a temporary URL to scrape.
    url = "http://www.cnn.com/2015/03/23/world/isis-luring-westerners/index.html"

    art = newspaper.Article(url)
    art.download()
    art.parse()

    art_txt = art.text

    # art_txt -> ML algorithms for text processing. 
    # Update Parse DB that URL has been processed.
    
