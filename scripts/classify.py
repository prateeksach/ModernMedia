import os
import sys
import json
import sklearn

training_folder = "data/"

categories = {'yellow': ('yellow', 'nonyellow'),
              'political': ('conservative', 'liberal', 'neutral'),
              'position': ('critical', 'defensive', 'factual')}

def organizeData():
    trainingData = {}

    # data -> ['article1', 'article2', ...]
    # target -> [1, 2, 3, 2, 1, 3, ...] 1 = conservative, 2 = liberal, ... etc.

    for category in categories:
        trainingData[category] = {'data': [], \
                             'target': []}

    files = os.listdir(training_folder)
    for training_file in files:
        with open(training_folder + training_file, 'r') as f:
            s = ''
            # read in file, assign target for each category

def trainClassifier(data):
    classifiers = {}
    for category in categories:
        text_clf = Pipeline([('vect', CountVectorizer()),\
                             ('tfidf', TfidfTransformer()),\
                             ('clf', SGDClassifier(loss='hinge',\
                                                   penalty='l2',\
                                                   alpha=1e-3,
                                                   n_iter=5))])
        _ = text_clf.fit(data[category]['data'], data[category]['target'])
        classifiers[category] = text_clf

    return classifiers

def main():
    trainingData = gatherData()
    classifiers = trainClassifier(trainingData)

if __name__ == "__main__":
    main()
