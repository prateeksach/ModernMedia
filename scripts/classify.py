import os
import sys
import json
import sklearn

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn import cross_validation

training_folder = "data/"
test_folder = "test/"

categories = {'yellowLabel': ('Yellow', 'Not Yellow') }
#               'politicalLabel': ('Conservative', 'Liberal', 'Neutral'),
#               'opinionLabel': ('Biased', 'Not Biased')}
categoryTargets = {'yellowLabel': {'Yellow': 1, 'Not Yellow': 2} }
#                   'politicalLabel': {'Conservative': 1, 'Liberal': 2, 'Neutral': 3},
#                   'biasLabel': {'Biased': 1, 'Not Biased': 2}}

def organizeData():
    # { 'data': ['article1', 'article2'], 'yellow': [targets], ... }
    trainingData = {'data': []}

    # data -> ['article1', 'article2', ...]
    # target -> [1, 2, 3, 2, 1, 3, ...] 1 = conservative, 2 = liberal, ... etc.

    for category in categories:
        trainingData[category] = []

    files = os.listdir(training_folder)
    for training_file in files:
        # read in file, assign target for each category
        with open(training_folder + training_file, 'r') as f:
            json_file = json.load(f)
            trainingData['data'].append(json_file['content'])
            for category in categories:
                label = json_file[category][0]
                trainingData[category].append(categoryTargets[category][label])

    return trainingData

def trainSVMClassifier(data):
    classifiers = {}
    for category in categories:
        text_clf = Pipeline([('vect', CountVectorizer()),\
                             ('tfidf', TfidfTransformer()),\
                             ('clf', SGDClassifier(loss='hinge',\
                                                   penalty='l2',\
                                                   alpha=1e-3,
                                                   n_iter=5))])
        loo = cross_validation.LeaveOneOut(len(data['data']))
        correct = 0
        for train_index, test_index in loo:
            _ = text_clf.fit([data['data'].index(i) for i in train_index], [data[category].index(i) for i in train_index])
            predicted = text_clf.predict(data['data'][test_index])
            if predicted == data[category][test_index]:
                print "Article ", str(text_index), "is", categories[category][predicted]
                correct += 1
        print "Accuracy ", str(float(correct)/len(data['data']))
        classifiers[category] = text_clf

    return classifiers

def trainNaiveBayesClassifier(data):
    classifiers = {}
    for category in categories:
        text_clf = Pipeline([('vect', CountVectorizer()),\
                             ('tfidf', TfidfTransformer()),\
                             ('clf', MultinomialNB())])
        text_clf = text_clf.fit(data['data'], data[category])
        classifiers[category] = text_clf

    return classifiers

def testClassifier(classifiers):
    test_docs = []
    files = os.listdir(test_folder)
    for test_file in files:
        with open(test_folder + test_file, 'r') as f:
            json_file = json.load(f)
            test_docs.append(json_file['content'])

    for category in categories:
        predicted = classifiers[category].predict(test_docs)

        print "\nClassification of " + category + "\n"
        #import ipdb; ipdb.set_trace()
        for i, prediction in enumerate(predicted):
            print files[i] + ',' + categories[category][prediction-1]

def main():
    algorithm = sys.argv[1]

    trainingData = organizeData()

    if algorithm == 'naivebayes':
        classifiers = trainNaiveBayesClassifier(trainingData)
    elif algorithm == 'svm':
        classifiers = trainSVMClassifier(trainingData)
    else:
        classifiers = trainSVMClassifier(trainingData)

    # testClassifier(classifiers)

if __name__ == "__main__":
    main()
