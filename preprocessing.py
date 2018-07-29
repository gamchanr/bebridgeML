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

    """
    just for the demo
    categoryList = ["Tours-travel", "food", "culture", "Society"]
    """

    return categoryList


def data2list(dirPath):
    """
    Input: path to DATASET directory
    Output: single list with all data as elements with filetype '.txt'
    """
    dataList = []
    fileExt = '*.txt'

    for root, dirs, files in os.walk(dirPath):
        for a in glob.glob(os.path.join(root, fileExt)):
            with open(a, "r") as f:
                line = f.readline().rstrip()
                dataList.append(line)

    return dataList

if __name__ == '__main__':
    data2list('./DATASET/')
