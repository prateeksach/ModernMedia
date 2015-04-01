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
    for key in categories:
        trainingData[key] = {'data': [], \
                             'target': [], \
                             'filenames': [], \
                             'target_names': categories}

    files = os.listdir(training_folder)

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
