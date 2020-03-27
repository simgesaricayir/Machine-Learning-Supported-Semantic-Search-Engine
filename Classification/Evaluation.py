import operator
from itertools import islice
from Word2VecTrain.SearchEngineV2 import controlProduct
import numpy
import joblib
from gensim.models import Word2Vec
from pandas import read_csv


Word2VecModel = Word2Vec.load('C:/Users/Lenovo/Desktop/Bitirme/Word2Vec.v3/models/trained_data.model.bin')
def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))


def getPredictions(words):
    filename = 'lda_model.sav'
    model = joblib.load(filename)
    filename = 'lda_pca.sav'
    pca = joblib.load(filename)
    result = dict()
    for i in words.split():
        t = numpy.array(Word2VecModel.wv[i]).reshape(1, -1)
        t = pca.transform(t)
        rslt = model.predict_proba(t)[0]
        prob_per_class_dictionary = dict(zip(model.classes_, rslt))

        prob_per_class_dictionary = dict(sorted(prob_per_class_dictionary.items(), key=operator.itemgetter(1),reverse=True))

        #print(prob_per_class_dictionary)
        #print(list(prob_per_class_dictionary)[0])
        maxSimilarity = 0
        for k in prob_per_class_dictionary:
            pr ,mn= controlProduct(k)
            #print(pr,end=" ")
            if len(pr)>0:
                #print(pr,i, Word2VecModel.wv.n_similarity(pr,[i]))
                sm = Word2VecModel.wv.n_similarity(pr,[i])
                if sm > maxSimilarity:
                    maxSimilarity = sm
                if sm > 0.4:
                    if k not in result:
                        result[k]= prob_per_class_dictionary[k]
                        result[k]+=sm
                    else:
                        result[k] += 1
                        result[k]+=sm
                        #result[k] += prob_per_class_dictionary[k]

                else:
                    break

    result = dict(sorted(result.items(), key=operator.itemgetter(1), reverse=True))
    if len(words.split()) >1 and result[list(result.keys())[0]]>1:
       result = {k: v for k, v in result.items() if v > len(words.split())-1}

    n = len(result)

    if n>10:
        n = 10

    return take(n,result.items())

def createMatrix(path):
    testDataset = read_csv(path)
    model = joblib.load('logistic5_model.sav')
    pca = joblib.load('logistic5_pca.sav')

    classes = dict()
    count = 0
    for i in testDataset['Product']:
        if i not in classes:
            classes[i] = count
            count += 1
    print(classes,len(classes))


    matrix = [[0 for x in range(len(classes))] for y in range(len(classes))]

    for i, j in zip(testDataset['Keyword'], testDataset['Product']):

        t = numpy.array(Word2VecModel.wv[i]).reshape(1, -1)
        t = pca.transform(t)
        rslt = model.predict_proba(t)[0]
        prob_per_class_dictionary = dict(zip(model.classes_, rslt))
        prob_per_class_dictionary = dict(sorted(prob_per_class_dictionary.items(), key=operator.itemgetter(1), reverse=True))

        top10 = take(10,prob_per_class_dictionary)
        #print(top10)

        #top10 = list(getPredictions(i).keys())

        ind = classes[j]
        if len(top10)!=0:
            if j in top10:
                matrix[ind][ind]+=1
            else:
                if top10[0] in classes:
                    index = classes[top10[0]]
                    matrix[ind][index] += 1
        else:
            print(i,j)
    return matrix

def evaluation(path):
    matrix = createMatrix(path)
    print(len(matrix))
    averagePrecision = 0
    averageRecall = 0
    accuracy = 0
    for i in range(len(matrix)):
        tp = matrix[i][i]
        accuracy += tp
        fp,fn = 0,0

        for j in range(len(matrix)):
            fp += matrix[j][i]
            fn += matrix[i][j]
        fp -= matrix[i][i]
        fn -= matrix[i][i]


        if tp != 0:
            p = tp / (tp+fp)
            r = tp / (tp+fn)
        else:
            p = 0
            r = 0
        averagePrecision+=p
        averageRecall +=r
    precision = averagePrecision/len(matrix)
    recall = averageRecall/len(matrix)
    accuracy = accuracy / numpy.sum(matrix)
    f1score = (2*precision*recall)/(precision+recall)
    print('precision',precision)
    print('recall',recall)
    print('accuracy',accuracy)
    print('f1score',f1score)


evaluation('C:/Users/Lenovo/Desktop/Bitirme/Word2Vec.v3/files/test_data1.csv')