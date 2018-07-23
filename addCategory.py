#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os.path
import glob


"""
Add category label to data
"""
def addCategory(category_name):
    category = category_name
    dirpath = './DATASET/' + category
    fileExt = '*.txt'
    for a in glob.glob(os.path.join(dirpath, fileExt)):
        with open(a, "a") as f:
            f.write("\n" + category)

    print("category labeled to data")
    return
