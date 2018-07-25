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
from trainModel import basicModel


"""
Input passes through ML model and outputs classified category
Input: Single question in string
Output: Classified category
"""
debug = 0
chosenModel = "basic"
updateModel = 0
question = "Does Korean stil eat dog?" #food or culture
#question = "what is one famous place to visit in United States?" #tours-travel
#question = "What is the most impressive social issue in Canada?" #society or life-and-living
#question = "what is the most famous sports in Norway" #sports
#question = "how does Korean think about their happiness" #culture or life-and-living
#question = "How do musicians find places for their tours?" #tours-travel
#question = "Who is the most famous person in Korea" #life-and-living
"""
question = "Why is Korea so hot in summer and so cold in winter? \n \n when I was young, I had a chance to travel Korea but the weather was extremely hot in summer and cold in winter"
question = question.splitlines()
question = ''.join(question)
"""

def MLprocessing(question):
    # search category list in DATASET dir
    dirPath = "./DATASET/"
    category_list = categoryList(dirPath)
    if debug: 
        print("category list: ", category_list, "(total: ", len(category_list), ")")
    
    if chosenModel=="basic":
        # update Models
        if updateModel:
            basicModel(dirPath)

        # apply Models
        print("Asked question:", question)
        docs = [question]

        loaded_vec = CountVectorizer(vocabulary=pickle.load(open("./TRAINED_MODEL/count_vector.pkl", "rb")))
        loaded_tfidf = pickle.load(open("./TRAINED_MODEL/tfidf.pkl","rb"))
        loaded_model = pickle.load(open("./TRAINED_MODEL/nb_model.pkl","rb"))

        X_new_counts = loaded_vec.transform(docs)
        X_new_tfidf = loaded_tfidf.transform(X_new_counts)
        predicted = loaded_model.predict(X_new_tfidf)

        print("Applyed category:", category_list[predicted[0]])

        return (category_list[predicted[0]])


if __name__ == '__main__':
    MLprocessing(question)
