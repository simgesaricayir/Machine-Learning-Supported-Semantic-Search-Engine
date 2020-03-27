#!/usr/bin/env python
# coding: utf-8
import numpy as np
from gensim.models import Word2Vec
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import time
import os  # for file info

f = open('files/stopwords.txt', 'r', encoding='utf8')
stopwords = f.read()
f.close()
stopwords = stopwords.split('\n')
abbrev = ['lı', 'li', 'lu', 'lü', 'kg', 'gr', 'lt', 'ml', 'cm', 'Migros']

def check_corpus(context):
    #context = lowerForTurkish(context)

    valid_harf = ["a", "b", "c", "ç", "d", "e", "f", "g", "ğ", "h", "ı", "i", "j", "k", "l"
        , "m", "n", "o", "ö", "p", "r", "s", "ş", "t", "u", "ü", "v", "y", "z","w","q",'x'," ", "A","B","C","Ç","D","E","F","G","Ğ","H"
                  ,"I","İ","J","K","L","M","N","O","Ö","P","R","S","Ş","T","U","Ü","V","Y","Z","W","Q",'X']
    ncontext = ""

    for i in range(len(context)):
        if context[i] in valid_harf:
            ncontext += context[i]
        else:
            ncontext += " "
    #print(ncontext)
    return ncontext

fp = open('C:/Users/Lenovo/Desktop/aramaKelimesi_crawl.txt', 'r', encoding='utf8')
wp = open('C:/Users/Lenovo/Desktop/Bitirme/GoogleCrawl/aramaKelimesi_crawl_duzeltilmis.txt','a',encoding='utf8')
for sentence in fp:
    sentence = str(sentence).rstrip()
    #print(sentence)
    sentence= check_corpus(sentence)
    print(sentence)
    if (len(sentence)>0 and sentence.find('KARGO')==-1 and sentence.find('Teslimat')==-1 and sentence.find('eklendi')==-1 and sentence.find('müşteri')==-1
        and sentence.find('Ürün')==-1 and sentence.find('Kapıda')==-1 and sentence.find('öneri')==-1 and  sentence.find('sepetinize')==-1
        and sentence.find('Ücretsiz')==-1 and sentence.find('Kargo')==-1 ):
        splitted = sentence.split()
        for i in splitted:
            if (len(i) < 2) or (i in abbrev):
                splitted.remove(i)
        if len(splitted) > 1:
            ws = ' '.join(splitted)
            #print(ws)
            ws+='\n'
            wp.write(ws)

