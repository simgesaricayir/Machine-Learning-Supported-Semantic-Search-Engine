import pandas as pd  # For data handling
from gensim.models import Word2Vec
import operator
from numpy import take
from snowballstemmer import TurkishStemmer
import itertools

####   Migros ürün açıklamaları ve productstxt kullanılarak eğitilmiş modeli kullanarak search engine


model = Word2Vec.load('C:/Users/Lenovo/Desktop/Bitirme/Word2Vec.v3/models/trained_data.model.bin')
df = pd.read_csv('C:/Users/Lenovo/Desktop/Bitirme/Word2Vec.v3/files/product_catalog.v2.csv')
df_clean = df.drop_duplicates(subset=['ProductName', 'ManufacturerName'])
abbrev = ['lı', 'li', 'lu', 'lü', 'kg', 'gr', 'lt', 'ml', 'cm', 'migros']
f = open('files/stopwords.txt', 'r', encoding='utf8')
stopwords = f.read()

# For Turkish Character
translationTable = str.maketrans("ğĞıİöÖüÜşŞçÇ", "gGiIoOuUsScC")
from itertools import islice

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

def lowerForTurkish(str):
    rep = [('I', 'ı'), ('İ', 'i')]
    for search, replace in rep:
        str = str.replace(search, replace)
    return str.lower()
def check_corpus(context):
    context = lowerForTurkish(context)
    valid_harf = ["a", "b", "c", "ç", "d", "e", "f", "g", "ğ", "h", "ı", "i", "j", "k", "l"
        , "m", "n", "o", "ö", "p", "r", "s", "ş", "t", "u", "ü", "v", "y", "z","w","q", "w",' ' ]

    ncontext = ""
    for i in range(len(context)):
        if context[i] in valid_harf:
            ncontext += context[i]
        else:
            ncontext += ' '
    return ncontext

def controlProduct(product):

    product = check_corpus(product)
    splitted = product.split()

    for i in splitted.copy():
        if (len(i) < 2) or (i in stopwords) or (i in abbrev) :
            splitted.remove(i)
        elif i not in model.wv.vocab:
            splitted.remove(i)
            #print(i)
    return splitted

def searchEngine(keys):
    #wp = open('files/productNames.txt', 'a', encoding='utf8')
    keyWords = keys.split()
    keyWords = [lowerForTurkish(x) for x in keyWords]
    #stemmer = TurkishStemmer()
    """
    for i in keyWords:
        newWord = stemmer.stemWord(i)
        if newWord not in keyWords and newWord in model.wv.vocab:
            keyWords.append(newWord)
    """
    transed = [x.translate(translationTable) for x in keyWords]

    # keyWords = list(set(keyWords))
    for a in keyWords:
        if a not in model.wv.vocab:
            keyWords.remove(a)
            keyWords.append(a.translate(translationTable))

    puanlanmis = dict()
    compareCount=0

    for product in df_clean['ProductName']:
        #wr = product + '\n'
        #wp.write(wr)
        puanlanmis[product]=0
        controlled= controlProduct(product)
        for word in controlled:
            for key in keyWords:
                puanlanmis[product] += model.wv.similarity(word, key)
                compareCount+=1
        if len(controlled)>0:
            puanlanmis[product] = puanlanmis[product] / compareCount
            compareCount=0
            for i in keyWords:
                if i in controlled:
                    puanlanmis[product]+=1

    puanlanmis = dict(sorted(puanlanmis.items(),reverse=True, key=operator.itemgetter(1)),)
    print("KEYWORDS",keyWords)
    print("most similar: ", model.wv.most_similar(positive=keyWords,topn=100))
    j = 1
    for i in take(20,puanlanmis.items()):
        #if puanlanmis[i]>0:
        print(j,i)
        j+=1
searchEngine("")




