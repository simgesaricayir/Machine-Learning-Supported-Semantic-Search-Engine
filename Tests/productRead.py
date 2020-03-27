import xlrd 
import pandas as pd
import xlwt 
from xlwt import Workbook 

loc = ("C:/Users/Lenovo/Desktop/Bitirme/Word2Vec.v3/files/test_sonuc2.xlsx")
f = open("C:/Users/Lenovo/Desktop/Bitirme/Word2Vec.v3/files/class_data.csv","a",encoding="utf-8")
#f.close()
#fwrite = open("C:/Users/Lenovo/Desktop/new.txt", "a",encoding="utf-8")
#wp = open("C:/Users/Lenovo/Desktop/Bitirme/Word2Vec.v3/files/excelProducts.txt", "r",encoding="utf-8")
#df = pd.read_csv('C:/Users/Lenovo/Desktop/product_catalog (1).csv')
#df_clean = df.drop_duplicates(subset=['ProductName', 'ManufacturerName'])
""""
wbook = Workbook() 
sheet1 = wbook.add_sheet('Sheet 1', cell_overwrite_ok=True) 
 
sheet1.write(0, 0, 'Ürün adı')
sheet1.write(0, 1, 'Arama Kelimeleri') 
j=1
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
sheet.cell_value(0, 0) 
for i in range(1,sheet.nrows):
	ürün =sheet.cell_value(i,0)
	aramakelimesi = sheet.cell_value(i,1)
	if ürün!="NULL" and aramakelimesi != "NULL" :

		sheet1.write(j, 0, ürün)
		sheet1.write(j, 1, aramakelimesi)
		j+=1

wbook.save('C:/Users/Lenovo/Desktop/tam_eslesme.xls')
"""
result = dict()
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
sheet.cell_value(0, 0) 
for i in range(0,sheet.nrows): 
	if sheet.cell_value(i,2) is not None:
		if sheet.cell_value(i,2) in result:
			result[str(sheet.cell_value(i,2))]+=1
		else:
			result[str(sheet.cell_value(i,2))]=1


print(sheet.nrows)
print(result)
"""

wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
sheet.cell_value(0, 0) 
for i in range(1,sheet.nrows):
	text =sheet.cell_value(i,0)
	keys = sheet.cell_value(i,1).replace(',', '')
	text += ','+keys+'\n'
	print(text)
	f.write(text)

list(df_clean['ProductName'])
count =0
for sentence in wp:
    sentence = str(sentence).rstrip()
    #sentence = sentence.split(',')[0]
    if sentence not in list(df_clean['ProductName']):
    	print(sentence)
    	sentence=sentence+'\n'
    	fwrite.write(sentence)
    	count+=1
print(count)
	
"""