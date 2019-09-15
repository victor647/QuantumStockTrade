# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'StockReviewer.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_StockReviewer(object):
    def setupUi(self, StockReviewer):
        StockReviewer.setObjectName("StockReviewer")
        StockReviewer.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(StockReviewer)
        self.centralwidget.setObjectName("centralwidget")
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(80, 20, 42, 22))
        self.spinBox.setMinimum(3)
        self.spinBox.setMaximum(10)
        self.spinBox.setProperty("value", 5)
        self.spinBox.setObjectName("spinBox")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 20, 71, 16))
        self.label.setObjectName("label")
        self.btnGetStockList = QtWidgets.QPushButton(self.centralwidget)
        self.btnGetStockList.setGeometry(QtCore.QRect(140, 20, 75, 23))
        self.btnGetStockList.setObjectName("btnGetStockList")
        StockReviewer.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(StockReviewer)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        StockReviewer.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(StockReviewer)
        self.statusbar.setObjectName("statusbar")
        StockReviewer.setStatusBar(self.statusbar)

        self.retranslateUi(StockReviewer)
        QtCore.QMetaObject.connectSlotsByName(StockReviewer)

    def retranslateUi(self, StockReviewer):
        _translate = QtCore.QCoreApplication.translate
        StockReviewer.setWindowTitle(_translate("StockReviewer", "今日牛股复盘"))
        self.spinBox.setSuffix(_translate("StockReviewer", "%"))
        self.label.setText(_translate("StockReviewer", "今日涨幅超过"))
        self.btnGetStockList.setText(_translate("StockReviewer", "获取股票列表"))
