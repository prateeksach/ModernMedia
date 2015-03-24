# Usual libraries
import os, sys
import datetime
import json

# Using newspaper library. Download and install from http://newspaper.readthedocs.org/en/latest/
try:
        import newspaper
except:
        print "Install newspaper package, from http://newspaper.readthedocs.org/en/latest/"
        print "Installation:"
        print "brew install libxml2 libxslt"
        print "brew install libtiff libjpeg webp little-cms2"
        print "pip install newspaper"
        print "curl https://raw.githubusercontent.com/codelucas/newspaper/master/download_corpora.py | python2.7"
        sys.exit()

try:
        from parse_rest.connection import register, ParseBatcher
        from parse_rest.datatypes import Object as ParseObject
except:
        print "Install ParsePy library: https://github.com/dgrtwo/ParsePy.git",
        print "pip install git+https://github.com/dgrtwo/ParsePy.git"
        sys.exit()


# These make batch updates easier, but I haven't had to use them. Keeping them in for later use if needed.
# def saveToParse(keylist):
#         batcher = ParseBatcher()
#         batcher.batch_save(keylist)
#
# def deleteFromParse(keylist):
#         batcher = ParseBatcher()
#         batcher.batch_delete(keylist)


if __name__ == '__main__':


        # Keys to the application
        APPLICATION_ID = "mequ79kBCNp74UrSEcoyty4Jwb3q9frUkuFrSsLE"
        REST_API_KEY = "i8uGEe3rJhBPjPYccnxBsJajlendJc8b7CF5lAhC"
        register(APPLICATION_ID, REST_API_KEY)

        # Inherit a ParseObject called Link which is the table object
        class Link(ParseObject):
                pass


        # Set all dataScrapped to False before processing
        # allRows = list(Link.Query.all())
        # for rowObj in allRows:
        #     rowObj.dataScrapped = False
        #     rowObj.save()



        ##------------------
        # Example website, delete for final version!

        url_ex = "http://www.cnn.com/2015/03/23/world/isis-luring-westerners/index.html"
        url_check_exists = list(Link.Query.filter(url = url_ex))
        # Avoid duplicating this link multiple times
        if len(url_check_exists) == 0:
                urlObj = Link()
                urlObj.url = url_ex
                urlObj.dataScrapped = False
                urlObj.save()

        elif len(url_check_exists) == 1:
                urlObj = url_check_exists[0]
                urlObj.dataScrapped = False
                urlObj.save()


        ##------------------

        # Yank all unread urls (dataScrapped == False) from the table
        unreadRows = list(Link.Query.filter(dataScrapped=False))
        unreadURLs = [rowObj.url for rowObj in unreadRows]
        for idx, url in enumerate(unreadURLs):
                article = newspaper.Article(url)
                # Download and parse the text in the article
                article.download()
                article.parse()

                # DO: Store the text as .txt in a separate folder locally
                # FOR NOW: just printing the text onto terminal
                art_title = article.title
                art_content = article.text
                art_tags = article.tags

                f = open("article" + str(idx) + ".json", 'w')
                json.dump({'title': str(art_title), 'content': str(art_content), 'tags': str(art_tags)}, f)
                f.close()

                # print "Article title is: ", art_title
                # raw_input("Press key to continue.")
                # print "Article content is: ", art_content
                # raw_input("Press key to continue.")
                # print "Article tags are: ", art_tags
                # raw_input("Press key to continue.")

                # Once saved, update dataScrapped to True
                rowObj = unreadRows[idx]
                rowObj.dataScrapped = True
                rowObj.save()



