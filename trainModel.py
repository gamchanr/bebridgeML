#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas
import glob
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from preprocessing import categoryList


debug = 0
dirPath = './DATASET/'

def basicModel(dirPath):
    """
    1. Take all data in DATASET and combine in to a single CSV file with category label
    2. generate basic model
    """
    
    # search category list in DATASET dir
    category_list = categoryList(dirPath)
    if debug:
        print("category list: ", category_list, "(total: ", len(category_list), ")")

    # read all data in DATASET dir and combine in to a CSV file
    directory_list = []
    for i in range(len(category_list)):
        directory_list.append(dirPath+category_list[i]+"/*.txt")
    if debug: 
        print("directory_list: ", directory_list)

    text_files = list(map(lambda x: glob.glob(x), directory_list))
    text_files = [item for sublist in text_files for item in sublist]
    if debug:
        #print("text_files: ", text_files)
        pass

    training_data = []

    for t in text_files:
        with open(t, 'r') as f:
            f = f.read()
            t = f.split('\n')
            #t = ''.join(t)
            training_data.append({'data' : t[0], 'flag' : category_list.index(t[-1])})

    if debug:
        print(training_data[0])

    training_data = pandas.DataFrame(training_data, columns=['data', 'flag'])
    training_data.to_csv("./train_data.csv", sep=',', encoding='utf-8')
    if debug:
        print("new training_data.csv file is generated")

    print("-----------------------------------------")
    print("total # of data:",training_data.data.shape)
    print("-----------------------------------------")
    """
    sklearn.feature_extraction.text
    """

    #GET VECTOR COUNT
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(training_data.data)

    #SAVE WORD VECTOR
    pickle.dump(count_vect.vocabulary_, open("./TRAINED_MODEL/count_vector.pkl","wb"))

    """
    sklearn.feature_extraction.text
    """
    #TRANSFORM WORD VECTOR TO TF IDF
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

    #SAVE TF-IDF
    pickle.dump(tfidf_transformer, open("./TRAINED_MODEL/tfidf.pkl","wb"))


    """
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.model_selection import train_test_split
    """
    # Multinomial Naive Bayes

    #clf = MultinomialNB().fit(X_train_tfidf, training_data.flag)
    X_train, X_test, y_train, y_test = train_test_split(X_train_tfidf, training_data.flag, test_size=0.25, random_state=42)
    clf = MultinomialNB().fit(X_train, y_train)

    #SAVE MODEL
    pickle.dump(clf, open("./TRAINED_MODEL/nb_model.pkl", "wb"))

