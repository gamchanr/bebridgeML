#!/usr/bin/python3
# -*- coding: utf-8 -*-
from gensim.models import KeyedVectors
import string

def notInDic(q):
    qList = q.split()
    table = str.maketrans('', '', string.punctuation)
    strippedQ = [w.translate(table) for w in qList]

    model = KeyedVectors.load_word2vec_format("./sentenceSim/data/GoogleNews-vectors-negative300.bin.gz", binary=True, limit=500000)
    for i in strippedQ:
        if i in model.vocab:
            pass
            #print("'%s' in word2vec" %i)
        else:
            #print("'%s' not in word2vec" %i)
            return True


#notInDic("what's your fav fhawoihfoi?")
