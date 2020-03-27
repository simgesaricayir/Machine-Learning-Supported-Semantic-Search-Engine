#!/usr/bin/env python
# coding: utf-8
import numpy as np
import pandas as pd  # For data handling
from gensim.models import Word2Vec
from sklearn.manifold import TSNE
import copy
import matplotlib.pyplot as plt
import time
import os  # for file info

f = open('C:/Users/Lenovo/Desktop/Bitirme/SearchEngine/files/stopwords.txt', 'r', encoding='utf8')
df = pd.read_csv('C:/Users/Lenovo/Desktop/Bitirme/SearchEngine/files/product_catalog.v2.csv')
df_clean = df.drop_duplicates(subset=['ProductName', 'ManufacturerName'])
stopwords = f.read()
stopwords = stopwords.split('\n')
abbrev = ['lı', 'li', 'lu', 'lü', 'kg', 'gr', 'lt', 'ml', 'cm', 'migros']
def lowerForTurkish(str):
    rep = [('I', 'ı'), ('İ', 'i')]
    for search, replace in rep:
        str = str.replace(search, replace)
    return str.lower()

manufacturer = []
for i in set(df_clean['ManufacturerName'].astype(str)):
    manufacturer.append(lowerForTurkish(i))

def check_corpus(context):

    context = lowerForTurkish(context)
    splitted = context.split()
    found=False
    text = copy.deepcopy(context)
    for i in splitted:
        if i in manufacturer:
            index = context.find(lowerForTurkish(i))
            found=True
            manufactur = context[:index+len(i)]
            text = context[index+len(i):]
            break

    valid_harf = ["a", "b", "c", "ç", "d", "e", "f", "g", "ğ", "h", "ı", "i", "j", "k", "l"
        , "m", "n", "o", "ö", "p", "r", "s", "ş", "t", "u", "ü", "v", "y", "z","w","q",'x',' ','-',"'"]

    ncontext = ""

    for i in range(len(text)):
        if text[i] in valid_harf:
            ncontext += text[i]
        else:
            ncontext += ' '
    if found:
        ncontext=manufactur+' '+ncontext
    return ncontext,manufacturer



def createCorpus(fileName):
    startTime = time.asctime()
    print("start time", startTime)

    corpus = []
    fp = open(fileName, 'r', encoding='utf8')
    for sentence in fp:
        sentence = str(sentence).rstrip()
        print(sentence)
        sentence,manufac = check_corpus(sentence)
        splitted = sentence.split()
        if len(splitted)>0:
            for i in splitted:
                if (len(i) < 2) or (i in stopwords): #or (i in abbrev):
                    splitted.remove(i)
            if len(splitted)>1:
                corpus.append(splitted)
    fp.close()
    print("corpus created")
    return corpus


def trainModel(fileName):
    print("training ")
    corpus = createCorpus(fileName)
    model = Word2Vec(corpus, size=300, window=5, min_count=5, sg=0,iter=4)
    model.save('C:/Users/Lenovo/Desktop/Bitirme/SearchEngine/models/trained_data.model.bin')
    print("done")


def testModel():
    model = Word2Vec.load('C:/Users/Lenovo/Desktop/Bitirme/SearchEngine/models/trained_data.model.bin')
    print(model.wv.most_similar(positive=["tavuk"], topn=60))
    print(model.wv.most_similar(positive=["çikolata"], topn=60))
    print(model.wv.most_similar(positive=["sırma"], topn=60))
    print(model.wv.most_similar(positive=["havlu"], topn=60))
    print(model.wv.most_similar(positive=["limon"], topn=60))
    print(model.wv.most_similar(positive=["salatalık"], topn=60))
    print(model.wv.most_similar(positive=["torku"], topn=60))
    print(model.wv.most_similar(positive=["içim"], topn=60))
    print(model.wv.most_similar(positive=["kaşar"], topn=60))
    print(model.wv.most_similar(positive=["oyuncak"], topn=60))
    print(model.wv.most_similar(positive=["mercimek"], topn=60))
    print(model.wv.most_similar(positive=["tereyağı"], topn=60))


def closestwords_tsneplot( word):
    model = Word2Vec.load('C:/Users/Lenovo/Desktop/Bitirme/SearchEngine/models/trained_data.model.bin')
    word_vectors = np.empty((0, 300))
    word_labels = [word]

    close_words = model.wv.most_similar(word)

    word_vectors = np.append(word_vectors, np.array([model.wv[word]]), axis=0)

    for w, _ in close_words:
        word_labels.append(w)
        word_vectors = np.append(word_vectors, np.array([model.wv[w]]), axis=0)

    tsne = TSNE(random_state=0)
    Y = tsne.fit_transform(word_vectors)

    x_coords = Y[:, 0]
    y_coords = Y[:, 1]

    plt.scatter(x_coords, y_coords)

    for label, x, y in zip(word_labels, x_coords, y_coords):
        plt.annotate(label, xy=(x, y), xytext=(5, -2), textcoords='offset points')

    plt.show()

#closestwords_tsneplot( 'peçete')
#trainModel("C:/Users/Lenovo/Desktop/Bitirme/SearchEngine/files/train_data.txt")
#testModel()