#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import glob


debug = 0
dirPath = './DATASET/'

def addCategory(category):
    """
    Add category label to data
    """
    dirpath = './DATASET/' + category
    fileExt = '*.txt'
    for a in glob.glob(os.path.join(dirpath, fileExt)):
        with open(a, "a") as f:
            f.write("\n" + category)

    print("category labeled to data")
    return


def categoryList(dirPath):
    """
    Input: path to DATASET directory
    Output: list of categories in DATASET directory
    """

    categoryList = []
    
    for root, dirs, files in os.walk(dirPath):
        for dirName in dirs:
            categoryList.append(dirName)

    return categoryList

