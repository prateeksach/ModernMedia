# Standard imports
from os import walk, path, getcwd, listdir
from sys import exit, argv
from math import log10
import re
import json

# Libraries for ML algorithms
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn import svm, naive_bayes

if __name__ == '__main__':


    pwd = getcwd()
    datafolder = path.join(pwd,'project_data')

    filelist = []
    for root,subdirs,files in walk(datafolder):
        for f in files:
            fname = path.join(root,f)
            filelist.append(fname)

    accuracy = 0.0
    yellowPredictionAll = []
    yellowTrueAll = []

    for leave_idx in range(len(filelist)):
        # Choose file under current leave_idx as a test file. Use the remaining data as training files.
        trainlist = filelist[0:leave_idx-1] + filelist[leave_idx+1:]
        testfile = filelist[leave_idx]

        trainingData = []
        trainYellowLabels = []

        for trainfile in trainlist:
            with open(trainfile, 'r') as f:
                json_file = json.load(f)

                #### TODO: change the uncommenting part as argument to program?
                ## Uncomment line below to train on content
                ## trainingData.append(json_file['content'])
                ## Uncomment line below to train on titles
                trainingData.append(json_file['title'])

                # Store training labels in a separate list
                trainYellowLabels.append(1 if json_file['yellowLabel'] == 'Yellow' else 0)

        # At this point, we have training and test data files in separate lists.
        # Implement classifer below.

        ## CountVectorizer options:
        # input = 'content' since data is stored as strings in lists. it would be 'file' if we stored each document as a
        # .txt file.
        # analyzer = 'word' means we use strings separated by whitespace as atoms in the vocabulary. we could use 'char'
        # instead, but that will not be useful since yellow and non-yellow articles in English are likely to have same
        # character distribution. However, yellow and non-yellow articles likely have different distributions of words
        # which are used.
        # stop_words = 'english' uses a standard english stopword dictionary (inbuilt)
        # ngram_range = (1,3) forms vocabulary from 1 upto 3 word-grams (since analyzer = 'word'). This is useful since
        # yellow articles may use different kinds of short "phrases" compared to non-yellow articles. However, very high
        # max_value (e.g. (1,10)) makes computation time very large (vocabulary will be HUGE) and also features will
        # become very high dimensional, so that distinguishing phrases will be sparser in the data and harder to find.
        vectorizer = CountVectorizer(input='content',analyzer='word', stop_words = 'english', ngram_range=(1,3),decode_error='ignore')

        # Not sure what sublinear_tf does, so I set it to False. Remaining options implement the tfidf we learned in
        # class.
        transformer = TfidfTransformer(norm='l2', use_idf=True, smooth_idf=True, sublinear_tf=False)
        tdtrain = vectorizer.fit_transform(trainingData)
        tfidftrain = transformer.fit_transform(tdtrain)

        ## SVM implmentation - Uncomment below to use
        # loss = l2: squared error loss between the predictive model and true data class, which is minimized to find the
        # right model to classify test data. Standard in the literature, not very important.
        # penalty = l1: This is important. It encourages sparsity in SVM solution. The intuition is that only some of
        # the features are "important" features (tfids) which differentiate yellow vs non-yellow articles, while most of
        # the other features are non important. Connect to how most words were common in the yellow vs non-yellow
        # articles. This is also probably why SVM outperforms Naive Bayes to some extent.
        # C = 100: algorithm parameter, has to be set through trial and error. No systematic way (that I know of) which
        # sets it.
        # clf = svm.LinearSVC(penalty = 'l1', loss = 'l2', C = 100, dual=False)

        ## Naive Bayes implementation: As explained in class. Multinomial allows for more than two classes, and uses a
        # multinomial distribution as prior for different classes. The NB we learned in class was for two classes and a
        # special case of this classifier. Implementation details are not different from class.
        clf = naive_bayes.MultinomialNB()

        ## Non-linear SVM. Allows for non-linear decision boundaries between classes. In the Fig. in the report, we can
        # find a line which best separates the two classes, i.e. a linear decision boundary. Most text classification is
        # shown to be non-linear (i.e. we have to find a *curve* which separates the points). The shape of the curve is
        # detemined by choice of kernel. (see wikipedia for figures of different kernels). I did NOT report these for
        # the final, but you can run it to see how it performs. The disadvantage with non-linear SVMs is large
        # computation time, as you will see if you run it.
        # clf = svm.SVC(C = 10.0, kernel = 'rbf', max_iter = 1000)
        clf.fit(tfidftrain, trainYellowLabels)

        # Predict test data using trained classifier clf. Store true as well as predicted labels.
        testData = []
        with open(testfile, 'r') as f:
            json_file = json.load(f)
            #testData.append(json_file['content'])
            testData.append(json_file['title'])
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

    # Evaluation of accuracy, yellow and non yellow accuracy, should be self documenting.
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


