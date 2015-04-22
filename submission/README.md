## EECS 498 Final Project

- Nick Morgan
- Raj Tejas
- Prateek Sachdeva
- Yogesh Seetharaman

## What is the State of Modern Media?

An analysis of the accuracy, bias, and 'yellow-ness' of modern internet-based media and corresponding outlets.

## Project Implementation README

To run the code from the terminal, use

    python classify.py [classifier] [content]

Where classifier and content are two arguments.

classifier has two options: svm and naivebayes

content has two options: article and title. 'article' means that the program will train
and classify on the actual wrticle while 'title' means the program will train and
classify on just the title

The program outputs predicted label, true label and progress as files processed/total number of files. Once the
code has iterated over all files, it outputs total accuracy, yellow accuracy and non yellow accuracy.
