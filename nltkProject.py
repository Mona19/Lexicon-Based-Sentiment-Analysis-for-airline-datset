# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 01:18:33 2017

@author: Mona
"""

import pandas as pd

# Import csv package to convert pandas dataframe to csv file
import csv

# Import Counter package to do counting
from collections import Counter

# Import operator package to sort a dictoinary by its values
import operator

# Import NTLK package after the installation

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.util import ngrams

import nltk
# nltk.download()

from pymongo import MongoClient

client = MongoClient()

db = client.Airline

AirlineReviews = db.AirlineReview

result = AirlineReviews.find({})

Airlinedf = pd.DataFrame(list(result))

del Airlinedf['_id']

# Airlinedf.head(5)



def word_feats(words):
    return dict([(word, True) for word in words])



review_test = Airlinedf[['reviewcontent', 'airlinename', 'authorname', 'rating_overall', 'recommended']]


#creating recommended and not recommended feature list
recc_feat = []
not_recc_feat = []

review = review_test.iloc[:1000, :]

#importing regex

import re
#iterating the dataset and removing the stopwods and punctionaion on recommendation
for row in range(0, len(review)):
    
    review1 = ""

    if review.iloc[row]['recommended'] == 1:

        # Reset the review variable
        review1 = review.iloc[row]['reviewcontent']

        # Remove punctuation
        # review1 = re.sub(r'[^\w\s]0123456789.-,()','',review1)
        review1 = re.sub(r'[^\w\s]', '', review1)
        # Review words with only 1 letter
        review1 = " ".join(
            word for word in review1.split()
            if len(word) > 1
        )

        # Remove Stopwords
        review1 = " ".join(
            word for word in review1.split()
            if not word in stopwords.words('english')
        )

        # Stemming
        stemmer = SnowballStemmer('english')
        review1 = " ".join(
            [stemmer.stem(word)
             for word in review1.split()]
        )

        ngramsize = 2

        if ngramsize > 1:
            review1 = [word for word in ngrams(
                review1.split(), ngramsize)]
            review1 = (word_feats(review1), 'rec')
        else:
            review1 = (word_feats(review1.split()), 'rec')
        recc_feat.append(list(review1))

#recommendation[0]
for row in range(0, len(review)):
    
    review2 = ""

    if review.iloc[row]['recommended'] == 0:

        # Reset the review variable
        review2 = review.iloc[row]['reviewcontent']

        # Remove punctuation
        # review2 = re.sub(r'[^\w\s]0123456789.-,()','',review2)
        review2 = re.sub(r'[^\w\s]', '', review2)
        # Review words with only 1 letter
        review2 = " ".join(
            word for word in review2.split()
            if len(word) > 1
        )

        # Remove Stopwords
        review2 = " ".join(
            word for word in review2.split()
            if not word in stopwords.words('english')
        )

        # Stemming
        stemmer = SnowballStemmer('english')
        review2 = " ".join(
            [stemmer.stem(word)
             for word in review2.split()]
        )

        ngramsize = 2
        if ngramsize > 1:
            review2 = [word for word in ngrams(
                review2.split(), ngramsize)]
            review2 = (word_feats(review2), 'not_rec')
        else:
            review2 = (word_feats(review2.split()), 'not_rec')

        not_recc_feat.append(list(review2))


train = recc_feat[:1000] + not_recc_feat[:1000]
test = recc_feat[1000:1500] + not_recc_feat[1000:1500]

print(train)
print(test)

# Train a Naive Bayesian Classifier
from nltk.classify import NaiveBayesClassifier

classifier = NaiveBayesClassifier.train(train)

# ==============================================================================
# print(classifier)
# ==============================================================================
# refsets will include the original pos/neg classification from the original data
# testsets will include the predicted classification results using the trained
# Naive Bayesian Classifier

import collections

refsets = collections.defaultdict(set)
testsets = collections.defaultdict(set)
(refsets['recommended'])
(testsets['not_recommended'])
(refsets['recommended'])
(testsets['not_recommended'])

# Iterate the reviews in the test dataset
# For each review, record the original class in the refset
# Put the predicted class in the testset
result = []
for i, (feats, label) in enumerate(test):
    print(i)
    refsets[label].add(i)
    observed = classifier.classify(feats)
    testsets[observed].add(i)
    result.append(observed)
    print(observed, label)
    


    
    
    
    


