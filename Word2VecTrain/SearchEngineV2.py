import pandas as pd  # For data handling
from gensim.models import Word2Vec
import operator
from numpy import take
from Word2VecTrain.Word2Vec_train import check_corpus
import time
import copy
from itertools import islice
from Word2VecTrain.EditDistance import controlKeywords
####   bütün crawl edilmiş veriler kullanılarak eğitilmiş modeli kullanarak search engine


model = Word2Vec.load('C:/Users/Lenovo/Desktop/Bitirme/Word2Vec.v3/models/trained_data.model.bin')
df = pd.read_csv('C:/Users/Lenovo/Desktop/Bitirme/Word2Vec.v3/files/product_catalog.v2.csv')

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
    filename =('C:/Users/Lenovo/Desktop/Bitirme/Word2Vec.v3/files/stems_withoutverb.txt')
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
        elif i not in model.wv.vocab:
            splitted.remove(i)
            if i not in manufacturers:
                withManufac.remove(i)
        elif i in abbrev:
            splitted.remove(i)
    return splitted,withManufac

def searchEngine(keys):

    fread = open('C:/Users/Lenovo/Desktop/Bitirme/Word2Vec.v3/files/checked_product.txt', 'r',encoding='utf8')

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
        if i not in model.wv.vocab:
            keyWords.remove(i)

    stems = readStems()

    for i in keyWordsCopy:
        if i in stems:
            newWord = stems[i]
            if newWord not in keyWordsCopy and newWord in model.wv.vocab:
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
                puanlanmis[product]=model.wv.n_similarity(checked,keyWords)

                # arama kelimesinin kökü ürün içinde varsa +1
                for i in keyWordsCopy:
                    if i in checked:
                        puanlanmis[product] += 1
                    if i not in checked and i in withManufact:
                        puanlanmis[product] += 1
                # ürün adındaki kelimenin kökü arama kelimesinde varsa +1
                for i in checked:
                    if i not in keyWordsCopy and i in stems and stems[i] not in checked and stems[i] in keyWordsCopy:
                        puanlanmis[product] += 1



    #print("KEYWORDS: ", keyWords)
    #print('keywordscopy',keyWordsCopy)
    #print("KeywordsCopy: ", keyWordsCopy)
    if len(puanlanmis)>0:
        puanlanmis = dict(sorted(puanlanmis.items(),reverse=True, key=operator.itemgetter(1)),)

        j = 1
        top10 = take(10, puanlanmis.items())
        for i in top10:
            print(j,i, top10[i])
            j += 1

        return top10
    else:
        return None

"""
start = time.time()
searchEngine("incir")
print(time.time()-start)
"""
#print(model.wv.n_similarity(['sarıyer','gurme','taze','kaşar'],['sarıyer','gurme','peyniri','kaşar']))