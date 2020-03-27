import copy
import operator

import xlsxwriter
from sklearn import metrics

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy
import xlrd
import joblib
from sklearn.metrics import recall_score, precision_score
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

import Word2VecTrain.Word2Vec_train as word2vec_train
import Word2VecTrain.EditDistance as check_keys
# Load libraries
from gensim.models import Word2Vec
from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import random


def warn(*args, **kwargs):
    pass


import warnings

warnings.warn = warn


def read_dataset():

    #loc = ("C:/Users/Lenovo/Desktop/son_aramaKelimesi_ürün.xlsx")
    loc = ("C:/Users/Lenovo/Desktop/arama_sonuclar_komple.xlsx")
    f = open("C:/Users/Lenovo/Desktop/Bitirme/SearchEngine/files/pca.csv", "w", encoding="utf-8")
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)
    f.write('Product,Keywords\n')
    for i in range(1, int(sheet.nrows)):
        text = sheet.cell_value(i, 0)
        keys = sheet.cell_value(i, 1).replace(',', '')
        print(i, keys, end=" ")
        keys = check_keys.controlKeywords(keys)
        print(keys)
        if len(keys) > 0:
            text += ',' + ' '.join(keys) + '\n'
            f.write(text)
        # print(text)

#read_dataset()

#datasetFirst = read_csv('C:/Users/Lenovo/Desktop/Bitirme/Word2Vec.v3/files/class_data.csv')
datasetFirst = read_csv('C:/Users/Lenovo/Desktop/Bitirme/SearchEngine/files/pca.csv')
datasetFirst = datasetFirst.groupby('Product').filter(lambda x: x['Product'].count() >=10)
Word2VecModel = Word2Vec.load('C:/Users/Lenovo/Desktop/Bitirme/SearchEngine/models/trained_data.model.bin')

products = dict()
data = []
data2= []
print(len(datasetFirst))

print('filtred', len(datasetFirst))

for i, j in zip(datasetFirst['Product'], datasetFirst['Keywords']):
    keys = j.split()
    for k in keys:
        sub = []
        sub2 = []
        sub2.append(k)
        if k in Word2VecModel.wv.vocab:
            for ind in Word2VecModel.wv[k]:
                sub.append(ind)
            sub2.append(i)
            sub.append(i)
            data2.append(sub2)
            data.append(sub)
""""
classDict = dict()
for i in data:
    if i[300] in classDict:
        classDict[i[300]] += 1
    else:
        classDict[i[300]] = 1
print(len(data), len(classDict))

classDict2 = dict()
for i,j in zip(data,data2):
    if classDict[i[300]] <10 or (i[300] in classDict2 and classDict2[i[300]]==10):
        data.remove(i)
        data2.remove(j)
    elif i[300] in classDict2:
        classDict2[i[300]]+=1
    elif i[300] not in classDict2:
        classDict2[i[300]]=1


print(classDict2)
print(len(classDict),len(classDict2))
print(len(data), len(data2))"""

columnNames = []
for i in range(300):
    columnNames.append('Index' + str(i))
columnNames.append('Class')
dataset = pd.DataFrame(data=(data), columns=columnNames)

array = dataset.values
X = array[:, 0:300]
y = array[:, 300]

X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.05, random_state=None)

""""
f = open("C:/Users/Lenovo/Desktop/Bitirme/Word2Vec.v3/files/test_data1.csv", "w", encoding="utf-8")
f.write('Keyword,Product\n')
count = 0
print('len X_test',len(X_test))
for i in range(len(data2)):
    if X[i] in X_test and y[i] in Y_test:
        print(data2[i][0] + ',' + data2[i][1])
        f.write(data2[i][0] + ',' + data2[i][1] + '\n')
        count+=1
    if count==len(X_test):
        break"""


sc = StandardScaler()
X_train = sc.fit_transform(X_train)  # eğitmek için kullanılıyor
X_test = sc.transform(X_test)  # eğitimi test için kullanmak
print('train,test')
import datetime

print(datetime.datetime.now())

from sklearn.decomposition import PCA

pca = PCA(n_components=100)
X_train2 = pca.fit_transform(X_train)
X_test2 = pca.transform(X_test)  # yeni verilere göre testi tekrar boyutlandır
""""
filename = 'logistic5_pca.sav'
joblib.dump(pca, filename)"""

classifier2 = LogisticRegression(solver='liblinear', multi_class='ovr')
classifier2.fit(X_train2, Y_train)
print('classifier fit')
print(datetime.datetime.now())
"""
filename = 'logistic5_model.sav'
joblib.dump(classifier2, filename)"""


y_pred2 = classifier2.predict(X_test2)
result2 = classifier2.score(X_test2, Y_test)
print('AFTER PCA')
precision = precision_score(Y_test, y_pred2, pos_label='positive', average='micro')
recall = recall_score(Y_test, y_pred2, pos_label='positive', average='micro')
f1_score = 2 * ((precision * recall) / (precision + recall))
print("Precision Score : ", precision)
print('recall_score', recall)
print('f1 score', f1_score)
print(metrics.accuracy_score(Y_test, y_pred2))



def getPredictions(word):
    print(word)
    t = numpy.array(Word2VecModel.wv[word]).reshape(1, -1)
    t = pca.transform(t)

    #filename = 'lr_all_model.sav'
    #model = joblib.load(filename)

    model = classifier2
    rslt = model.predict_proba(t)[0]
    prob_per_class_dictionary = dict(zip(model.classes_, rslt))
    prob_per_class_dictionary = dict(sorted(prob_per_class_dictionary.items(), key=operator.itemgetter(1), reverse=True))
    print(prob_per_class_dictionary)
    print(list(prob_per_class_dictionary)[0])


getPredictions('selpak')
getPredictions('kahve')
getPredictions('süt')
getPredictions('soda')
getPredictions('süzme')
print(datetime.datetime.now())

