from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QListWidgetItem

from SearchEngines.SearchEngineV4 import searchEngine as searchEnginev4
from SearchEngines.SearchEngineV3 import searchEngine as searchEnginev3
res = dict()
class sender:
    def __init__(self,res):
        self.res= res
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("MAKİNE ÖĞRENMESİ DESTEKLİ ANLAMSAL ÜRÜN ARAMA MOTORU")
        Form.resize(905, 595)


        Form.setStyleSheet("QWidget {background-image: url(images/images.png)}")

        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setIcon(QtGui.QIcon('images/indir.png'))

        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setGeometry(QtCore.QRect(50, 150, 821, 341))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 819, 339))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        #self.scrollAreaWidgetContents.setStyleSheet("QWidget {background-image: url(images/shopping.png)}")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(50, 80, 351, 31))
        self.widget.setObjectName("widget")
        self.widget.setStyleSheet("QWidget {background-image: url(images/white.png)}")
        self.widget1 = QtWidgets.QWidget(Form)
        self.widget1.setGeometry(QtCore.QRect(440, 55, 206, 61))
        self.widget1.setObjectName("widget1")
        self.widget1.setStyleSheet("QWidget {background-image: url(images/white.png)}")
        self.widget1.hide()
        

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")


        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")


        self.v3 = QtWidgets.QListWidget(self.scrollAreaWidgetContents)
        self.v3.setGeometry(QtCore.QRect(20, 40, 381, 281))
        self.v3.setObjectName("v3")
        self.v3.setStyleSheet("QWidget {background-image: url(images/white.png)}")


        self.v4 = QtWidgets.QListWidget(self.scrollAreaWidgetContents)
        self.v4.setGeometry(QtCore.QRect(420, 40, 381, 281))
        self.v4.setObjectName("v4")
        self.v4.setStyleSheet("QWidget {background-image: url(images/white.png)}")

        newfont = QtGui.QFont("Times", 13)
        self.bulunamadi = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.bulunamadi.setGeometry(QtCore.QRect(30, 10, 331, 20))
        self.bulunamadi.setObjectName("bulunamadi")
        self.bulunamadi.setText('Word2Vec Vektörleri ile Sonuçlar')
        self.bulunamadi.setFont(newfont)
        self.bulunamadi_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.bulunamadi_2.setGeometry(QtCore.QRect(420, 10, 361, 20))
        self.bulunamadi_2.setObjectName("bulunamadi_2")
        self.bulunamadi_2.setText('Makine Öğrenmesi ile Sonuçlar')
        self.bulunamadi_2.setFont(newfont)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.demekIstemistiniz = QtWidgets.QLabel(Form)
        self.demekIstemistiniz.setObjectName("demekIstemistiniz")

        self.header = QtWidgets.QLabel(Form)
        self.header.setGeometry(QtCore.QRect(30, 20, 751, 20))
        self.header.setObjectName("header")

        self.ask = QtWidgets.QLabel(Form)
        self.ask.setObjectName("ask")

        self.onay = QtWidgets.QPushButton(Form)
        self.onay.setObjectName("onay")
        self.onay.setText('Evet')

        self.horizontalLayout.addWidget(self.lineEdit)
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addWidget(self.ask)
        self.horizontalLayout_2.addWidget(self.demekIstemistiniz)
        spacerItem = QtWidgets.QSpacerItem(68, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.horizontalLayout_2.addWidget(self.onay)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.ask.setText('Bunu mu demek istemiştiniz?')
        self.ask.hide()

        self.header.setText('MAKİNE ÖĞRENMESİ DESTEKLİ ANLAMSAL ÜRÜN ARAMA MOTORU')
        newfont = QtGui.QFont("Times", 15, QtGui.QFont.Bold)
        self.header.setFont(newfont)
        self.onay.hide()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.pushButton.clicked.connect(self.search)

    def search(self):
        global res
        print('search')
        res,keys = searchEnginev3(self.lineEdit.text())
        if keys!=None:
            print('keys')
            self.widget1.show()
            self.ask.show()
            self.demekIstemistiniz.setText(keys)
            self.demekIstemistiniz.show()

            self.onay.show()
            print('onay')
            self.onay.clicked.connect(self.result)
        else:
            self.result()
    def result(self):
        newfont = QtGui.QFont("Times", 12)
        global res
        if res is None:
            self.v3.clear()
            self.bulunamadi.setText('Sonuç Bulunamadı')
            self.bulunamadi.show()
        else:

            print('result')
            index = 1
            self.v3.clear()
            for i in res:
                i = str(index) + ". "+ i
                item = QListWidgetItem(i)
                item.setFont(newfont)
                self.v3.addItem(item)
                index+=1

        res, keys = searchEnginev4(self.lineEdit.text())
        if res is None:
            self.v4.clear()
            self.bulunamadi_2.setText('Sonuç Bulunamadı')
        else:
            self.v4.clear()
            index = 1
            for i in res:
                i = str(index) + ". " + i
                item = QListWidgetItem(i)
                item.setFont(newfont)
                self.v4.addItem(item)
                index+=1
        self.onay.hide()
        self.ask.hide()
        self.demekIstemistiniz.hide()
        self.widget1.hide()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Arama Motoru", "Arama Motoru"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
