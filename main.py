#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas
import glob
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from trainModel import *


"""
Input passes through ML model and outputs classified category
Input: Single question in string
Output: Classified category
"""
debug = 0
genModel = 0
question = "Does Korean eat dog?" #food or culture

#question = "what is one famous place to visit in United States?" #tours-travel
#question = "What is the most impressive social issue in Canada?" #society or life-and-living
#question = "what is the most famous sports in Norway" #sports
#question = "how does Korean think about their happiness" #culture or life-and-living
#question = "How do musicians find places for their tours?" #tours-travel
#question = "Who is the most famous person in Korea" #life-and-living

def MLprocessing(question):
    category_list = ["food", "culture", "weather", "Tours-travel", "Human-Behavior", "Society", "Jobs-and-Careers", "Life-and-Living-2", "sports"]
    dirpath = "./DATASET/"

    directory_list = []
    for i in range(len(category_list)):
        directory_list.append(dirpath+category_list[i]+"/*.txt")
    if(debug): 
        print("directory_list: ", directory_list)
        print("#of category_list: ", len(category_list))

    text_files = list(map(lambda x: glob.glob(x), directory_list))
    text_files = [item for sublist in text_files for item in sublist]
    if(debug):
        #print("text_files: ", text_files)
        print()

    training_data = []

    for t in text_files:
        with open(t, 'r') as f:
            f = f.read()
            t = f.split('\n')
            training_data.append({'data' : t[0], 'flag' : category_list.index(t[-1])})

    if(debug):
        print(training_data[0])

    training_data = pandas.DataFrame(training_data, columns=['data', 'flag'])
    training_data.to_csv("./train_data.csv", sep=',', encoding='utf-8')

    print("-----------------------------------------")
    print("# of total data:",training_data.data.shape)
    print("-----------------------------------------")

    if (genModel):
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


    """
    MODEL APPLY
    """
    docs_new = [question]

    #LOAD MODEL
    loaded_vec = CountVectorizer(vocabulary=pickle.load(open("./TRAINED_MODEL/count_vector.pkl", "rb")))
    loaded_tfidf = pickle.load(open("./TRAINED_MODEL/tfidf.pkl","rb"))
    loaded_model = pickle.load(open("./TRAINED_MODEL/nb_model.pkl","rb"))

    X_new_counts = loaded_vec.transform(docs_new)
    X_new_tfidf = loaded_tfidf.transform(X_new_counts)
    predicted = loaded_model.predict(X_new_tfidf)

    print("Asked question:", question)
    print("Applyed category:", category_list[predicted[0]])

    return (category_list[predicted[0]])


if __name__ == '__main__':
    MLprocessing(question)
