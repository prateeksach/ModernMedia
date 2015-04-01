import os
import sys
import json
import sklearn

training_folder = "data/"

categories = {'yellowness': ('yellow', 'non-yellow'),
              'affilation': ('conservative', 'liberal', 'neutral'),
              'harshness': ('critical', 'defensive', 'factual')}

def organizeData():
    trainingData = {}

    # data -> ['article1', 'article2', ...]
    # target -> [1, 2, 3, 2, 1, 3, ...] 1 = conservative, 2 = liberal, ... etc.

    for key in categories:
        trainingData[key] = {'data': [], \
                             'target': []}

    files = os.listdir(training_folder)
    for training_file in files:
        with open(training_folder + training_file, 'r') as f:
            s = ''
            # read in file, assign target for each category

def classifyYellowness():
    pass

def classifyAffilation():
    pass

def classifyHarshness():
    pass

def main():
    pass

if __name__ == "__main__":
    main()
