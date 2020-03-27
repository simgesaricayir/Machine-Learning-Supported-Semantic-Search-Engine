import xlrd

from Word2VecTrain import SearchEngineV2
import xlsxwriter

loc = ("C:/Users/Lenovo/Desktop/Bitirme/Word2Vec.v3/files/arama_sonuclar_komple.xlsx")

workbook = xlsxwriter.Workbook('C:/Users/Lenovo/Desktop/Bitirme/Word2Vec.v3/files/test_sonuc2.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write(0, 0, "Ürün Adı")
worksheet.write(0, 1, "Arama Kelimeleri")
worksheet.write(0, 2, "Bulunma Sırası")

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
sheet.cell_value(0, 0)

for i in range(1,sheet.nrows):
    ürün = sheet.cell_value(i, 0)
    aramakelimesi = sheet.cell_value(i, 1)

    worksheet.write(i, 0,ürün)
    worksheet.write(i, 1,aramakelimesi)

    sonuclar = SearchEngineV2.searchEngine(aramakelimesi)

    if sonuclar is not None and ürün in sonuclar:
        index = list(sonuclar.keys()).index(ürün) + 1
        print(i,ürün,index)
        worksheet.write(i, 2, str(index))


workbook.close()