#!/usr/bin/python3
# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import time
import os
from preprocessing import addCategory


"""
crawling dataset of listed category
"""
category = []
MAX_ITER = 10
existCategory = ["food","culture", "weather", "Tours-travel", "Human-Behavior","Society","Jobs-and-Careers","Life-and-Living-2", "sports"]

for i in range(len(category)):
    filepath = "./DATASET_ETC/"+category[i]+"/"
    if not os.path.isdir(filepath):
        os.mkdir(filepath)
        print("Generated category directory in DATASET")

    driver = webdriver.Chrome()
    driver.get('https://www.quora.com/topic/'+category[i])
    driver.implicitly_wait(5)

    questionList = []

    for it in range(0, MAX_ITER):
        print("iter: ", it)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    posts = driver.find_elements_by_class_name("story_title_container")
    print("#of posts: ", len(posts))
    for post in posts:
        if post not in questionList:
            questionList.append(post.text)
    print("#of questions: ", len(questionList))

    for q in range(len(questionList)):
        filename = str(q)+".txt"
        if os.path.exists(os.path.join(filepath, filename)):
            print("file exists")
        with open(os.path.join(filepath,filename), 'w') as f:
            f.write(questionList[q])

    addCategory(category[i])

