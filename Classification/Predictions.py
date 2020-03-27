import operator
from itertools import islice

from Word2VecTrain.SearchEngineV2 import controlProduct
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy
import joblib
from gensim.models import Word2Vec
from pandas import read_csv
import time


Word2VecModel = Word2Vec.load('C:/Users/Lenovo/Desktop/Bitirme/Word2Vec.v3/models/trained_data.model.bin')


def take(n, iterable):
    return dict(islice(iterable, n))
def getPredictions(words):
    filename = 'class3_10_model.sav'
    model = joblib.load(filename)
    filename = 'class3_10_pca.sav'
    pca = joblib.load(filename)
    result = dict()
    for i in words.split():
        t = numpy.array(Word2VecModel.wv[i]).reshape(1, -1)
        t = pca.transform(t)
        rslt = model.predict_proba(t)[0]
        prob_per_class_dictionary = dict(zip(model.classes_, rslt))

        prob_per_class_dictionary = dict(sorted(prob_per_class_dictionary.items(), key=operator.itemgetter(1),reverse=True))

        print(prob_per_class_dictionary)

        maxSimilarity = 0
        for k in prob_per_class_dictionary:
            pr ,mn= controlProduct(k)
            #print(pr,end=" ")
            if len(result)==10:
                break
            if len(pr)>0:
                #print(pr,i, Word2VecModel.wv.n_similarity(pr,[i]))
                sm = 0
                for w in words.split():
                    sm +=Word2VecModel.wv.n_similarity(pr,[w])
                print(pr,sm/len(words.split()))
                if sm/len(words.split()) > 0.75:
                    if k not in result:
                        result[k]= prob_per_class_dictionary[k]
                        #result[k]+=sm
                    else:
                        result[k] += 1
                        #result[k]+=sm
                        #result[k] += prob_per_class_dictionary[k]

    result = dict(sorted(result.items(), key=operator.itemgetter(1), reverse=True))
    if len(words.split()) >1 and result[list(result.keys())[0]]>1:
       result = {k: v for k, v in result.items() if v > len(words.split())-1}

    n = len(result)
    print(result)
    if n>10:
        n = 10

    return take(n,result.items())

start = time.time()
result = getPredictions('süzme yoğurt')
print(time.time()-start)
print('\nResults')
for i in result:
    print(i,result[i])

