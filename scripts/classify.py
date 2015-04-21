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

training_folder = "new_data/"
test_folder = "test/"

# describes the categories, you can uncomment lines to train and classify on other categories
categories = {'yellowLabel': ('Yellow', 'Not Yellow') }
#               'politicalLabel': ('Conservative', 'Liberal', 'Neutral'),
#               'opinionLabel': ('Biased', 'Not Biased')}
categoryTargets = {'yellowLabel': {'Yellow': 1, 'Not Yellow': 2} }
#                   'politicalLabel': {'Conservative': 1, 'Liberal': 2, 'Neutral': 3},
#                   'biasLabel': {'Biased': 1, 'Not Biased': 2}}

# Gathers data and organizes into the described format for sklearn
def organizeData(content):
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
            trainingData['data'].append(json_file[content])
            for category in categories:
                label = json_file[category]
                trainingData[category].append(categoryTargets[category][label])

    return trainingData

# trains and returns svm classifier for each category
# also performs leave one out cross validation
def trainSVMClassifier(data):
    classifiers = {}
    for category in categories:
        # build a pipeline using CountVectorizer, TfidfTransformer and SGDClassifier
        text_clf = Pipeline([('vect', CountVectorizer()),\
                             ('tfidf', TfidfTransformer()),\
                             ('clf', SGDClassifier(loss='hinge',\
                                                   penalty='l2',\
                                                   alpha=1e-3,
                                                   n_iter=5))])
        loo = cross_validation.LeaveOneOut(len(data['data']))
        correct = 0
        total = len(data['data'])

        for train_index, test_index in loo: # for each combination of leave one out

            # allows us to ignore certain articles for classificiation
            # for example, we can only classify yellow articles to check accuracy for yellowness
            # uncomment next three lines for functionality
            # if data[category][test_index[0]] == 1: # use == 1 for non-yellow accuracy and == 0 for yellow accuracy
            #     total -= 1
            #     continue

            # fit the data by choosing files based on leave one out
            _ = text_clf.fit([data['data'][i] for i in train_index], [data[category][i] for i in train_index])
            predicted = text_clf.predict([data['data'][test_index[0]]])

            try:
                print "Article ", str(os.listdir(training_folder)[test_index[0]]), "is", categories[category][predicted[0]-1], "; Correct is", categories[category][data[category][test_index[0]]-1]
                if predicted[0] == data[category][test_index[0]]:
                    correct += 1
            except: # if article did not contain any data due to scraping failure, ignore it
                total -= 1
                continue
        print "Accuracy ", str(float(correct)/total)
        classifiers[category] = text_clf

    return classifiers

# trains and returns naive bayes classifier for each category
# also performs leave one out cross validation
# this function performs the same function as the previous one but with different classifiers
def trainNaiveBayesClassifier(data):
    classifiers = {}
    for category in categories:
        # build a pipeline using CountVectorizer, TfidfTransformer and MultinomialNB
        text_clf = Pipeline([('vect', CountVectorizer()),\
                             ('tfidf', TfidfTransformer()),\
                             ('clf', MultinomialNB())])
        text_clf = text_clf.fit(data['data'], data[category])
        loo = cross_validation.LeaveOneOut(len(data['data']))
        correct = 0
        total = len(data['data'])

        for train_index, test_index in loo:
            # allows us to ignore certain articles for classificiation
            # for example, we can only classify yellow articles to check accuracy for yellowness
            # uncomment next three lines for functionality
            # if data[category][test_index[0]] == 1: # use == 1 for non-yellow accuracy and == 0 for yellow accuracy
            #     total -= 1
            #     continue
            _ = text_clf.fit([data['data'][i] for i in train_index], [data[category][i] for i in train_index])
            predicted = text_clf.predict([data['data'][test_index[0]]])

            try:
                print "Article ", str(os.listdir(training_folder)[test_index[0]]), "is", categories[category][predicted[0]-1], "; Correct is", categories[category][data[category][test_index[0]]-1]
                if predicted[0] == data[category][test_index[0]]:
                    correct += 1
            except:
                total -= 1
                continue
        print "Accuracy ", str(float(correct)/total)
        classifiers[category] = text_clf

    return classifiers

# classifies documents in the test set
# we do not use this function as we chose to do leave one out
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
        #
        for i, prediction in enumerate(predicted):
            print files[i] + ',' + categories[category][prediction-1]

# takes in an argument to choose classifier
def main():
    algorithm = sys.argv[1]
    content = sys.argv[2]

    trainingData = organizeData(content)

    if algorithm == 'naivebayes':
        classifiers = trainNaiveBayesClassifier(trainingData)
    elif algorithm == 'svm':
        classifiers = trainSVMClassifier(trainingData)
    else:
        classifiers = trainSVMClassifier(trainingData)

    # testClassifier(classifiers)

if __name__ == "__main__":
    main()
