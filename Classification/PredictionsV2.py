import copy
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
    filename = 'C:/Users/Lenovo/Desktop/Bitirme/Word2Vec.v3/Classification/class3_v2_model.sav'
    model = joblib.load(filename)
    filename = 'C:/Users/Lenovo/Desktop/Bitirme/Word2Vec.v3/Classification/class3_v2_pca.sav'
    pca = joblib.load(filename)
    probDicts = []

    for i in words:
        t = numpy.array(Word2VecModel.wv[i]).reshape(1, -1)
        t = pca.transform(t)
        rslt = model.predict_proba(t)[0]
        prob_per_class_dictionary = dict(zip(model.classes_, rslt))
        prob_per_class_dictionary = dict(sorted(prob_per_class_dictionary.items(), key=operator.itemgetter(1), reverse=True))
        #print(prob_per_class_dictionary)
        probDicts.append(prob_per_class_dictionary)

    result = copy.deepcopy(probDicts[0])
    #print(result)
    for i in result.copy():
        pr, mn = controlProduct(i)
        if len(pr)>0:
            sm=0
            for w in words:
                sm += Word2VecModel.wv.n_similarity(pr,[w])
            average = sm/len(words)
            if average <0.75:
                del result[i]
            else:
                result[i]=average
                #print(i,average)
        else:del result[i]

    for i in range(1,len(words)+1):
        for p in probDicts[i-1]:
            if p in result:
                result[p] = ((result[p]*(i))+probDicts[i-1][p]*100)/i
                #result[p] += probDicts[i - 1][p]
    result = dict(sorted(result.items(), key=operator.itemgetter(1),reverse=True))
    #print('\nRESULT')
    return take(10,result.items())

start = time.time()
#res = getPredictions(['süzme','peynir'])
res= getPredictions(['şampuan'])
for i in res:
    print(i,res[i])
print()
print(time.time()-start)
"""
res = getPredictions('süzme yoğurt')
for i in res:
    print(i,res[i])
print()
res = getPredictions('çikolata')
for i in res:
    print(i,res[i])
print()
res = getPredictions('meyveli yoğurt')
for i in res:
    print(i,res[i])
print()
res = getPredictions('çubuk kraker')
for i in res:
    print(i,res[i])
"""