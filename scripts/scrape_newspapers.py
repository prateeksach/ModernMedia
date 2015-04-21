# Usual libraries
import os, sys
import datetime
import json

# Using newspaper library. Download and install from http://newspaper.readthedocs.org/en/latest/
try:
        import newspaper
except:
        print "Install newspaper package, from http://newspaper.readthedocs.org/en/latest/"
        print "Installation: pip install newspaper"
        sys.exit()

try:
        from parse_rest.connection import register, ParseBatcher
        from parse_rest.datatypes import Object as ParseObject
except:
        print "Install ParsePy library: https://github.com/dgrtwo/ParsePy.git"
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

        # Inherit a ParseObject called Link2 which is the table object
        class Link2(ParseObject):
                pass


        #Set all dataScrapped to False before processing
        # allquery = Link2.Query.all()
        # allRows = allquery.limit(1000)
        # print len(allRows)
        # for rowObj in allRows:
        #     rowObj.dataScrapped = False
        #     rowObj.save()

        


        # Yank all unread urls (dataScrapped == False) from the table
        unreadRows = list(Link2.Query.filter(dataScrapped=False).limit(1000))
        
        for idx, row in enumerate(unreadRows):
                url = row.url

                article = newspaper.Article(url)
                # Download and parse the text in the article
                article.download()
                article.parse()

                # Extract title, text content and tags. Python doesn't interact well with ASCII
                # encoding, so encode all text to utf-8 before storing. 
                art_title = article.title.encode('utf-8')
                art_content = article.text.encode('utf-8')
                art_tags = set([tag.encode('utf-8') for tag in article.tags])

                
                politicalLabel = row.politicalLabel
                yellowLabel = row.yellowLabel
                opinionLabel = row.opinionLabel
                biasLabel = row.biasLabel
                organization = row.organization
                topic = row.topic


                f = open("article" + str(idx) + ".json", 'w')
                json.dump({'title': str(art_title), 'content': str(art_content), 'tags': str(art_tags), 
                    'politicalLabel': politicalLabel, 'yellowLabel': yellowLabel, 
                    'opinionLabel':opinionLabel, 'biasLabel':biasLabel, 'organization':organization, 'topic':topic}, f)
                # json.dump({'title': str(art_title), 'content': str(art_content)}, f)
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



