# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(234, 117)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btnStockAnalyzer = QtWidgets.QPushButton(self.centralwidget)
        self.btnStockAnalyzer.setGeometry(QtCore.QRect(10, 20, 91, 31))
        self.btnStockAnalyzer.setObjectName("btnStockAnalyzer")
        self.btnStockFinder = QtWidgets.QPushButton(self.centralwidget)
        self.btnStockFinder.setGeometry(QtCore.QRect(110, 20, 91, 31))
        self.btnStockFinder.setObjectName("btnStockFinder")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 234, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.btnStockAnalyzer.clicked.connect(MainWindow.show_stock_analyzer)
        self.btnStockFinder.clicked.connect(MainWindow.show_stock_finder)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "量化交易"))
        self.btnStockAnalyzer.setText(_translate("MainWindow", "个股股性分析"))
        self.btnStockFinder.setText(_translate("MainWindow", "技术指标选股"))
