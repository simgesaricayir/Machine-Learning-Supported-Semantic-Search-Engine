import operator
from itertools import islice

import xlrd
import xlsxwriter
from gensim.models import Word2Vec

from SearchEngines import SearchEngineV4
from pandas import read_csv
def take(n, iterable):
    return list(islice(iterable, n))
def takeDict(n, iterable):
    return dict(islice(iterable, n))
testData = read_csv('C:/Users/Lenovo/Desktop/Bitirme/SearchEngine/files/classlar.csv')
data = dict()


def read_dataset():
    for p, k in zip(testData['Product'], testData['Keyword']):
        if k not in data:
            data[k]=dict()
            data[k][p]=1
        else:
            if p not in data[k]:
                data[k][p]= 1
            else:
                data[k][p] +=1

    for k in data:
        data[k]= takeDict(10,dict(sorted(data[k].items(), reverse=True, key=operator.itemgetter(1))).items())
        data[k]= {k: v for k, v in data[k].items() if v >1 }
    return data


def test1():
    workbook = xlsxwriter.Workbook('C:/Users/Lenovo/Desktop/Bitirme/SearchEngine/files/son_test2.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, "Arama Kelimeleri")
    worksheet.write(0, 1, "Ürün Sayısı")
    worksheet.write(0, 2, "İlk 10'da Bulunan Ürün Sayısı")
    worksheet.write(0, 3, "Sıra Ortalaması")

    data = read_dataset()
    data = {k: v for k, v in data.items() if len(v) >=2 }
    for i in data:
        print(i,data[i])
    print(len(data))
    kCount = 1
    for keywords in data:
        sonuclar,y = SearchEngineV4.searchEngine(keywords)
        indexes = 0
        foundCount = 0
        if sonuclar is not None:
            products = take(10,data[keywords])
            for i in products:
                if i in sonuclar:
                    foundCount+=1
                    indexes+= sonuclar.index(i)
            if foundCount>0:
                if indexes==0: avr = 0
                else: avr = indexes/foundCount
                worksheet.write(kCount, 0, keywords)
                worksheet.write(kCount, 1, len(products))
                worksheet.write(kCount, 2, foundCount)
                worksheet.write(kCount, 3,avr )
                print(products)
                print(kCount, keywords)
                print(kCount, 0, keywords)
                print(kCount, 1, len(products))
                print(kCount, 2, foundCount)
                print(kCount, 3, indexes / foundCount)

            else:
                print(products)
                worksheet.write(kCount, 0, keywords)
                worksheet.write(kCount, 1, len(products))
                worksheet.write(kCount, 2, 0)
                worksheet.write(kCount, 3, 0)
                print(kCount, keywords)
                print(kCount, 0, keywords)
                print(kCount, 1, len(products))
                print(kCount, 2, 0)
                print(kCount, 3, 0)
            kCount += 1
    workbook.close()


def sonuc():
    loc = ('C:/Users/Lenovo/Desktop/Bitirme/SearchEngine/files/son_test2.xlsx')

    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)
    count = 0
    for i in range(1, sheet.nrows):
        if int(sheet.cell_value(i, 1)) < 5 and int(sheet.cell_value(i, 2)) == int(sheet.cell_value(i, 1)):
            count += 1
        elif int(sheet.cell_value(i, 2)) >= 5 :
            count+=1

    print(count)
    print(sheet.nrows)
def kriter2():
    #v3
    loc = ('C:/Users/Lenovo/Desktop/Bitirme/Word2Vec.v3/files/lda.xlsx')
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)
    count = 0
    avr = 0
    for i in range(1, sheet.nrows):
        if int(sheet.cell_value(i, 2)) != 0:
            avr += int(sheet.cell_value(i, 2))* int(sheet.cell_value(i, 3))
            count+= int(sheet.cell_value(i, 2))
    print(avr/count)

def kriter3():
    fread = open('C:/Users/Lenovo/Desktop/Bitirme/Word2Vec.v3/files/checked_product.txt', 'r', encoding='utf8')
    Word2VecModel = Word2Vec.load('C:/Users/Lenovo/Desktop/Bitirme/Word2Vec.v3/models/trained_data.model.bin')
    pro = []
    checkedPro = []
    withManufactPro = []
    for sentence in fread:
        sentence = sentence.rstrip('\n')
        sp = sentence.split(',')
        pro.append(sp[0])
        checkedPro.append(sp[1].split())
        withManufactPro.append(sp[2].split())

    keys = list(set(testData['Keyword']))
    #keys = ['elma','soda','peynir','meyveli yoğurt','süzme yoğurt','yoğurt']
    count = 0
    keyCount = 0

    keywwordIn = 0
    for i in range(500):
        print(i)
        sonuclar,keywords = SearchEngineV4.searchEngine(keys[i].split()[0])
        if keywords[0] in Word2VecModel.wv.vocab :
            keywwordIn+=1

        #print(sonuclar)
        pcount = 0
        checked=0
        count = 0
        if sonuclar is not None:
            for p in sonuclar:   #sonuçlar içerisindeki ürün
                ch = checkedPro[pro.index(p)]


                for kelime in ch:  #ürün içerisindeki kelime

                    if kelime in Word2VecModel.wv.vocab and keywords[0] in Word2VecModel.wv.vocab:
                        pcount+=1

                         #kelime ile arama kelimesi karşılaştırıllması
                        if Word2VecModel.wv.similarity(kelime,keywords[0]) >= 0.7:
                            count+=1
                            break
                if pcount>=1:
                    checked+=1
            print(count,checked)
            if count==checked:
                keyCount+=1
                print(keyCount)

    print(keyCount)
    print(keywwordIn)

test1()
sonuc()
#kriter3()