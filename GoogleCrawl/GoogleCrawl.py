import urllib
from inscriptis import get_text
from googlesearch import search
import pandas as pd

f = open("son_crawl.txt", "a",encoding="utf-8")
df = pd.read_csv('C:/Users/Lenovo/Desktop/Bitirme/Word2Vec.v3/files/product_catalog.v2.csv')
df_clean = df.drop_duplicates(subset=['ProductName', 'ManufacturerName'])
i =0
for query in df_clean['ProductName']:
    print(query,i,len(df_clean['ProductName']))
    for url in search(query, tld="co.in",lang="tr", num=5, stop=5, pause=1):
        print(url)
        if url.find('youtube')==-1 and url.find('wikipedia')==-1 and url.find('carrefour')==-1 :
            try:
                html = urllib.request.urlopen(url,timeout=1).read().decode('utf-8')
                text = get_text(html)
                f.write(text)
                #print(text)
            except:
                print("An exception occurred")
    i+=1



