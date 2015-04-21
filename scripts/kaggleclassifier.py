from os import walk, path, getcwd, listdir
from sys import exit, argv
from math import log10
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn import svm, naive_bayes
import re
import json

if __name__ == '__main__':


    pwd = getcwd()
    datafolder = path.join(pwd,'new_data')

    filelist = []
    for root,subdirs,files in walk(datafolder):
        for f in files:
            fname = path.join(root,f)
            filelist.append(fname)

    accuracy = 0.0
    yellowPredictionAll = []
    yellowTrueAll = []

    for leave_idx in range(len(filelist)):
        trainlist = filelist[0:leave_idx-1] + filelist[leave_idx+1:]
        testfile = filelist[leave_idx]

        trainingData = []
        trainYellowLabels = []

        for trainfile in trainlist:
            with open(trainfile, 'r') as f:
                json_file = json.load(f)
                trainingData.append(json_file['content'])
                # trainingData.append(json_file['title'])
                trainYellowLabels.append(1 if json_file['yellowLabel'] == 'Yellow' else 0)

        vectorizer = CountVectorizer(input='content',analyzer='word', stop_words = 'english', ngram_range=(1,3),decode_error='ignore')
        transformer = TfidfTransformer(norm='l2', use_idf=True, smooth_idf=True, sublinear_tf=False)
        tdtrain = vectorizer.fit_transform(trainingData)
        tfidftrain = transformer.fit_transform(tdtrain)
        clf = svm.LinearSVC(penalty = 'l1', loss = 'l2', C = 100, dual=False)
        # clf = naive_bayes.MultinomialNB()
        # clf = svm.SVC(C = 10.0, kernel = 'rbf', max_iter = 1000)
        clf.fit(tfidftrain, trainYellowLabels)

        testData = []
        with open(testfile, 'r') as f:
            json_file = json.load(f)
            testData.append(json_file['content'])
            # testData.append(json_file['title'])
            yellowTrue = 1 if json_file['yellowLabel'] == 'Yellow' else 0
            yellowTrueAll.append(yellowTrue)
        
        tdtest = vectorizer.transform(testData)
        tfidftest = transformer.transform(tdtest)
        yellowPrediction = clf.predict(tfidftest)
        yellowPredictionAll.append(yellowPrediction)
            
        
        print "Predicted label = ", yellowPrediction,
        print "True label = ", yellowTrue
        
        accuracy += 1 if yellowPrediction[0] == yellowTrue else 0
        print "Progress: ", leave_idx, '/', len(filelist)

    accuracy = accuracy/len(filelist)
    print "Accuracy = ", accuracy

    yellowAccuracy = 0.0
    for x,y in zip(yellowPredictionAll, yellowTrueAll):
        if (y == 1) and (x[0] == y):
            yellowAccuracy += 1
    yellowAccuracy = yellowAccuracy/len(filter(lambda x: x == 1, yellowTrueAll))

    nonYellowAccuracy = 0.0
    for x,y in zip(yellowPredictionAll, yellowTrueAll):
        if (y == 0) and (x[0] == y):
            nonYellowAccuracy += 1
    nonYellowAccuracy = nonYellowAccuracy/len(filter(lambda x: x == 0, yellowTrueAll))

    print "Yellow Accuracy = ", yellowAccuracy,
    print "Non Yellow Accuracy = ", nonYellowAccuracy



#     
#     trnlbl = []
#     for f in trainfiles:
# 
#         fname = path.basename(f)
#         fnamesp = re.split('([a-zA-Z]+).(\d+)',fname)
#         ftype = fnamesp[1]
#         trnlbl += [1] if ftype == 'joke' else [0]
# 
#     clf = svm.LinearSVC(penalty = 'l1', loss = 'l2', C = 1e1, dual=False) 
#     clf.fit(tfidftrain, trnlbl)
# 
# 
#     testfiles = []
#     for root, subdirs, files in walk(testfolder):
#         for f in files:
#             fname = path.join(root,f);
#             testfiles.append(fname)
# 
#     tdtest = vectorizer.transform(testfiles)
#     tfidftest = transformer.transform(tdtest)
#     tstlbl = clf.predict(tfidftest)
# 
#     csvop = ["File,Class","\n"]
#    
# 
#     for f, lbl in zip(testfiles, tstlbl):
#         
#         fname = path.basename(f)
#         fnamesp = re.split('([a-zA-Z]+).(\d+)',fname)
#         ftype = fnamesp[1]
#         csvop += [fname + "," + "".join("joke" if lbl==1 else "mix"), "\n"]
# 
# 
