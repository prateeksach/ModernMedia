# The usual imports
import os
import sys

# Scraped data is stored as .json files
import json

# Parse database library
try:
        from parse_rest.connection import register, ParseBatcher
        from parse_rest.datatypes import Object as ParseObject
except:
        print "Install ParsePy library: https://github.com/dgrtwo/ParsePy.git"
        print "pip install git+https://github.com/dgrtwo/ParsePy.git"



if __name__ == '__main__':

    APPLICATION_ID = "mequ79kBCNp74UrSEcoyty4Jwb3q9frUkuFrSsLE"
    REST_API_KEY = "i8uGEe3rJhBPjPYccnxBsJajlendJc8b7CF5lAhC"
    register(APPLICATION_ID, REST_API_KEY)

    class Link(ParseObject):
        pass
    
    allRows = list(Link.Query.filter(dataScrapped=True).limit(1000))
    
    # for idx, row in enumerate(allRows):
    #     
    #     f = open("article" + str(idx) + ".json", 'a')

    #     polLabel = row.politicalLabels
    #     posLabel = row.positionLabels
    #     yelLabel = row.yellowLabels

    #     json.dump({'positionLabels': posLabel, 'politicalLabels': polLabel, 'yellowLabel': yelLabel}, f)
    #     f.close()


    with open("article" + str(12) + ".json") as data_file:
        filedata = json.load(data_file)
        print filedata
        data_file.close()




        
    
