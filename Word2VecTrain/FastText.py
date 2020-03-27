import pandas as pd  # For data handling
from gensim.models import Word2Vec, FastText
import copy
import time


f = open('C:/Users/Lenovo/Desktop/Bitirme/Word2Vec.v3/files/stopwords.txt', 'r', encoding='utf8')
df = pd.read_csv('C:/Users/Lenovo/Desktop/Bitirme/Word2Vec.v3/files/product_catalog.v2.csv')
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
    model = FastText(corpus, size=300, window=5, min_count=5, sg=0,iter=4)
    model.save('C:/Users/Lenovo/Desktop/Bitirme/Word2Vec.v3/models/fasttext.model.bin')
    print("done")
def testModel():

    model = FastText.load('C:/Users/Lenovo/Desktop/Bitirme/Word2Vec.v3/models/fasttext.model.bin')
    print('model')
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
#trainModel("C:/Users/Lenovo/Desktop/Bitirme/Word2Vec.v3/files/train_data.txt")
testModel()
