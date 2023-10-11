# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'untitled.ui'
##
# Created by: Qt User Interface Compiler version 6.5.0
##
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QLineEdit,
                               QListWidget, QListWidgetItem, QMainWindow, QMenuBar,
                               QPushButton, QSizePolicy, QStatusBar, QWidget, QHBoxLayout, QListView, QDialog)
from functions import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(299, 472)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.checkBox = QCheckBox(self.centralwidget)
        self.checkBox.setObjectName(u"checkBox")

        self.gridLayout.addWidget(self.checkBox, 0, 0, 1, 1)

        self.checkBox_2 = QCheckBox(self.centralwidget)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.gridLayout.addWidget(self.checkBox_2, 0, 1, 1, 1)

        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.gridLayout.addWidget(self.lineEdit, 1, 0, 1, 1)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout.addWidget(self.pushButton, 1, 1, 1, 1)

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.gridLayout.addWidget(self.pushButton_2, 2, 0, 1, 1)

        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.gridLayout.addWidget(self.pushButton_3, 2, 1, 1, 1)

        self.listWidget = QListWidget(self.centralwidget)
        self.listWidget.setObjectName(u"listWidget")

        self.gridLayout.addWidget(self.listWidget, 3, 0, 1, 2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.lineEdit.raise_()
        self.checkBox.raise_()
        self.checkBox_2.raise_()
        self.listWidget.raise_()
        self.pushButton.raise_()
        self.pushButton_2.raise_()
        self.pushButton_3.raise_()
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 299, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.checkBox_2.toggled.connect(
            lambda checked: checked and self.checkBox.setCheckState(Qt.Unchecked))
        self.checkBox.toggled.connect(
            lambda checked: checked and self.checkBox_2.setCheckState(Qt.Unchecked))
        self.pushButton.clicked.connect(self.searchName)
        self.pushButton_3.clicked.connect(self.addToFavorite)
        self.pushButton_2.clicked.connect(self.plotGraph)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate(
            "MainWindow", u"CryptoFinder", None))
        self.checkBox.setText(
            QCoreApplication.translate("MainWindow", u"API", None))
        self.checkBox_2.setText(QCoreApplication.translate(
            "MainWindow", u"Scraping", None))
        self.pushButton.setText(QCoreApplication.translate(
            "MainWindow", u"Search", None))
        self.pushButton_2.setText(
            QCoreApplication.translate("MainWindow", u"Details", None))
        self.pushButton_3.setText(QCoreApplication.translate(
            "MainWindow", u"Favorite", None))
    # retranslateUi

    def searchName(self):
        self.names = []
        self.text = self.lineEdit.text()
        self.lineEdit.clear()
        scrape = self.checkBox_2.isChecked()
        api = self.checkBox.isChecked()
        if scrape:
            try:
                data = scraperDataGetter(self.text)
                name = data["name"]
                self.names.append(name)
            except:
                data = "No Results"
            self.checkBox_2.setCheckState(Qt.Unchecked)
        elif api:
            try:
                data = apiDataGetter(self.text)
                name = data["name"]
                self.names.append(name)
            except:
                data = "No Results"
            self.checkBox.setCheckState(Qt.Unchecked)
        self.listWidget.addItem(str(data))

    def plotGraph(self):
        index = self.listWidget.row(self.listWidget.currentItem())
        print(index)
        item = self.names[index-1]
        print(item)
        df = pd.read_csv("{}.csv".format(item))
        print(df)
        xAxis = [i for i in df["time"]]
        print(xAxis)
        yAxis = [i for i in df["price"]]
        print(yAxis)
        num = len(xAxis)/2
        for i in range(int(num)):
            xAxis.remove("time")
            yAxis.remove("price")
        plt.plot(xAxis, yAxis, color='blue')
        for i in range(len(xAxis)):
            x = xAxis[i]
            y = yAxis[i]
            plt.plot(x, y, "oy")
        plt.show()

    def addToFavorite(self):
        index = self.listWidget.row(self.listWidget.currentItem())
        item = self.names[index-1]
        new = 1
        with open(r"data\favorite.txt", "r") as file:
            for line in file:
                if line == item:
                    print("already added")
                    new = 0
                    break
                else:
                    new = 1
        with open(r"data\favorite.txt", "a") as file:
            if new == 1:
                file.write(item)
        with open(r"data\favorite.txt", "r") as file:
            for line in file:
                print(line)

    def delCurrent(self):
        index = self.listWidget.row(self.listWidget.currentItem())
        item = self.names[index-1]
        self.listWidget.clearSelection()
        text = []
        with open(r"data\favorite.txt", "r") as file:
            for line in file:
                if line == item:
                    continue
                else:
                    text.append(line)
        with open(r"data\favorite.txt", "w") as file:
            for line in text:
                file.write(line+"\n")
        with open(r"data\favorite.txt", "r") as file:
            for line in file:
                print(line)
