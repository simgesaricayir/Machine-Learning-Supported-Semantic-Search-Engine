import operator
import sys
import time
from Word2VecTrain.Word2Vec_train import check_corpus
from gensim.models import Word2Vec
from nltk.metrics import *

from pandas import read_csv
import copy

model = Word2Vec.load('C:/Users/Lenovo/Desktop/Bitirme/SearchEngine/models/trained_data.model.bin')
dataset = read_csv('C:/Users/Lenovo/Desktop/Bitirme/SearchEngine/files/product_catalog.v2.csv')
abbrev = ['lı', 'li', 'lu', 'lü', 'kg', 'gr', 'lt', 'ml', 'cm']

def lowerForTurkish(str):
    rep = [('I', 'ı'), ('İ', 'i')]
    for search, replace in rep:
        str = str.replace(search, replace)
    return str.lower()

vocab = []
for i in dataset['ProductName']:
    i = lowerForTurkish(i)
    #print(i)
    splitted = i.split()
    for k in splitted:
        if k in model.wv.vocab and k not in vocab:
            vocab.append(k)
#rint('len',len(vocab))

def transition(keyword):

    if len(keyword)>0 and keyword!=' ':
        translationTable= [str.maketrans("iuocsg", "ıüöçşğ"),str.maketrans("scg", "şçğ"),
                           str.maketrans("scg", "şçğ"),str.maketrans("ıuocsg", "iüöçşğ"),
                           str.maketrans("ıuo", "iüö"),str.maketrans("iüö", "ıuo"),str.maketrans("ıc", "iç")
                            ]
        comb = []
        for i in translationTable:
            tr = keyword.translate(i)
            if tr in vocab:
                return tr
    return None

def controlKeywords(aranan):


    manufacturNames = []
    kelimeler = copy.deepcopy(aranan)
    kelimeler,manufacturNames = check_corpus(kelimeler)
    kelimeler=kelimeler.split()


    for i in kelimeler.copy():
        if (len(i) < 2):
            kelimeler.remove(i)
        elif i in abbrev:
            kelimeler.remove(i)

    control = [0] * len(kelimeler)
    for i in range(len(kelimeler)):
        if kelimeler[i] not in model.wv.vocab and kelimeler[i] not in manufacturNames :
            control[i]=0

            trans = transition(kelimeler[i])
            if trans is not None:
                kelimeler[i]=trans
                control[i]=1
        else:
            control[i]=1
    if 0 not in control:
        return kelimeler
    else:

        sonuc = [None] * len(kelimeler)
        for i in range(len(kelimeler)):
            if kelimeler[i] in model.wv.vocab:
                sonuc[i] = kelimeler[i]

        combinations = dict()
        for i in range(len(kelimeler)):

            if kelimeler[i] not in model.wv.vocab and kelimeler[i] not in manufacturNames:

                lst = copy.deepcopy(sonuc)
                minval = sys.maxsize
                for word in vocab :
                    if word in model.wv.vocab:
                        new = edit_distance(word,kelimeler[i])

                        if len(kelimeler)>1 and new<=minval:
                            minval = new
                            minWord = word

                            for ind in range(len(kelimeler)):

                                if len(combinations)>0 and kelimeler[ind] == kelimeler[i] and i>0:

                                    for y in combinations.copy():
                                        lst = list(copy.deepcopy(y))
                                        lst[i]=word
                                        combinations[tuple(lst)] = minval
                                        if len(kelimeler)==2 and i<len(kelimeler)-1:
                                            del combinations[y]

                                        else:
                                            del combinations[y]

                                elif sonuc[ind] is not None:
                                    lst[ind]=sonuc[ind]

                                elif kelimeler[ind] == kelimeler[i]:
                                    lst[ind]=word
                                elif i == 0:
                                    lst[ind]=kelimeler[ind]
                            combinations[tuple(lst)]=minval

                        elif len(kelimeler)==1 and new <= minval:
                            minval = new
                            minWord = word

            else:
                sonuc[i]=kelimeler[i]
                if len(kelimeler)==1:
                    minWord=kelimeler[i]
                #print(sonuc)



        if len(combinations)>0:
            combinations = dict(sorted(combinations.items(), key=operator.itemgetter(1)))
            combinations = {x: combinations[x] for x in combinations if combinations[x] == combinations[list(combinations.keys())[0]]}
            for i in combinations:
                s = list(i)
                sum = 0
                for k in range(len(s)-1):
                    if s[k] in model.wv.vocab and s[k+1] in model.wv.vocab:
                        sum+= model.wv.similarity(s[k],s[k+1])
                combinations[i]=sum


            combinations  = dict(sorted(combinations.items(), key=operator.itemgetter(1),reverse=True))
            #print(combinations)
            return list(list(combinations.keys())[0])#,combinations[list(combinations.keys())[0]]
        elif len(kelimeler)==1:
            return [minWord]
        else:
            return [i for i in sonuc if i]
"""
start = time.time()
print('sonuc',controlKeywords('anjelika'))
print(time.time()-start)
"""







""""
def memoize(func):
    mem = {}

    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in mem:
            mem[key] = func(*args, **kwargs)
        return mem[key]

    return memoizer



@memoize
def levenshtein(s, t):
    if s == "":
        return len(t)
    if t == "":
        return len(s)
    if s[-1] == t[-1]:
        cost = 0
    else:
        cost = 1

    res = min([levenshtein(s[:-1], t) + 1,
               levenshtein(s, t[:-1]) + 1,
               levenshtein(s[:-1], t[:-1]) + cost])

    return res
    """
