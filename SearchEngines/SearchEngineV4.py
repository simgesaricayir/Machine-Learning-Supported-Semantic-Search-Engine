import pandas as pd
from gensim.models import Word2Vec
import operator
from numpy import take
from Word2VecTrain.Word2Vec_train import check_corpus
import time
import copy
import numpy
import joblib
from itertools import islice
from Word2VecTrain.EditDistance import controlKeywords
from string import digits

Word2VecModel = Word2Vec.load('C:/Users/Lenovo/Desktop/Bitirme/SearchEngine/models/trained_data.model.bin')
df = pd.read_csv('C:/Users/Lenovo/Desktop/Bitirme/SearchEngine/files/product_catalog.v2.csv')
abbrev = ['lı', 'li', 'lu', 'lü', 'kg', 'gr', 'lt', 'ml', 'cm']
manufacturers = []

def lowerForTurkish(str):
    rep = [('I', 'ı'), ('İ', 'i')]
    for search, replace in rep:
        str = str.replace(search, replace)
    return str.lower()
def take(n, iterable):
    return dict(islice(iterable, n))
def readStems():
    filename =('C:/Users/Lenovo/Desktop/Bitirme/SearchEngine/files/stems_withoutverb.txt')
    stems = dict()
    with open(filename,encoding='utf8') as fstem:
        for line in fstem:
            val = line.split()
            stems[val[0]] = val[1]
    return stems
def controlProduct(product):

    productl = lowerForTurkish(product)
    productl,manufacturers = check_corpus(productl)
    splitted = productl.split()
    withManufac = productl.split()


    for i in splitted.copy():
        if (len(i) <2) :
            splitted.remove(i)
            withManufac.remove(i)
        elif i not in Word2VecModel.wv.vocab:
            splitted.remove(i)
            if i not in manufacturers:
                withManufac.remove(i)
        elif i in abbrev:
            splitted.remove(i)
    return splitted,withManufac
def getPredictions(words):
    #enSon_model.sav
    filename = 'C:/Users/Lenovo/Desktop/Bitirme/SearchEngine/Classification/enSon_model.sav'
    model = joblib.load(filename)
    filename = 'C:/Users/Lenovo/Desktop/Bitirme/SearchEngine/Classification/enSon_pca.sav'
    pca = joblib.load(filename)
    result = dict()
    for i in words:
        t = numpy.array(Word2VecModel.wv[i]).reshape(1, -1)
        t = pca.transform(t)
        rslt = model.predict_proba(t)[0]
        prob_per_class_dictionary = dict(zip(model.classes_, rslt))
        prob_per_class_dictionary = dict(sorted(prob_per_class_dictionary.items(), key=operator.itemgetter(1), reverse=True))

        temp = take(20,prob_per_class_dictionary.items())
        for k in temp:
            if k in result:
                result[k]+=temp[k]*100
            else:
                result[k]=temp[k]*100

    result = dict(sorted(result.items(), key=operator.itemgetter(1),reverse=True))
    return result

def searchEngine(keys):

    fread = open('C:/Users/Lenovo/Desktop/Bitirme/SearchEngine/files/checked_product.txt', 'r',encoding='utf8')
    numbers = [s for s in keys.split() if s.isdigit()]
    checkedPro = []
    withManufactPro = []
    for sentence in fread:
        sentence = sentence.rstrip('\n')
        sp = sentence.split(',')
        checkedPro.append(sp[1].split())
        withManufactPro.append(sp[2].split())

    keyWords = controlKeywords(keys)
    keyWordsCopy = copy.deepcopy(keyWords)
    for i in keyWords:
        if i not in Word2VecModel.wv.vocab:
            keyWords.remove(i)

    stems = readStems()

    for i in keyWordsCopy:
        if i in stems:
            newWord = stems[i]
            if newWord not in keyWordsCopy and newWord in Word2VecModel.wv.vocab:
                keyWordsCopy.append(newWord)

    puanlanmis = dict()
    if len(keyWords)>0:

        ind = 0
        for product in df['ProductName']:

            checked,withManufact = checkedPro[ind],withManufactPro[ind]
            #checked, withManufact = controlProduct(product)
            #fread.write(product+','+' '.join(checked)+','+' '.join(withManufact)+'\n')
            ind+=1

            if len(checked)>0 and len(keyWords)>0:
                puanlanmis[product]=Word2VecModel.wv.n_similarity(checked,keyWords)

                # arama kelimesinin kökü ürün içinde varsa +1
                for i in keyWordsCopy:
                    if i in checked:
                        puanlanmis[product] += 2
                    elif i not in checked and i in withManufact:
                        puanlanmis[product] += 2
                # ürün adındaki kelimenin kökü arama kelimesinde varsa +1
                for i in checked:
                    if i not in keyWordsCopy and i in stems and stems[i] not in checked and stems[i] in keyWordsCopy:
                        puanlanmis[product] +=2
                for i in numbers:
                    if i in [s for s in product.split() if s.isdigit()]:
                        puanlanmis[product] += 1

    if len(puanlanmis)>0  :
        puanlanmis = dict(sorted(puanlanmis.items(), reverse=True, key=operator.itemgetter(1)))
        classResult = getPredictions(keyWords)
        print(classResult)
        if puanlanmis[list(puanlanmis.keys())[0]]>0.7 and puanlanmis[list(classResult.keys())[0]]>0.7:

            size = len(keyWords)
            factor = 1
            if len(classResult)>0:
                if classResult[list(classResult.keys())[0]] < size:
                    factor = (size)/classResult[list(classResult.keys())[0]]
                for i in classResult:
                    if i in puanlanmis:
                        puanlanmis[i] += classResult[i]*factor


        puanlanmis = dict(sorted(puanlanmis.items(), reverse=True, key=operator.itemgetter(1)))
        remove_digits = str.maketrans('', '', digits)
        if keyWords!=lowerForTurkish(keys).translate(remove_digits).split():
            return take(50, puanlanmis.items()), ' '.join(keyWords)

        return take(50,puanlanmis.items()),None

    else:
        return None,None