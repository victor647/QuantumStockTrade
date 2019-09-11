# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'StockFinder.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_StockFinder(object):
    def setupUi(self, StockFinder):
        StockFinder.setObjectName("StockFinder")
        StockFinder.resize(403, 251)
        self.centralwidget = QtWidgets.QWidget(StockFinder)
        self.centralwidget.setObjectName("centralwidget")
        StockFinder.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(StockFinder)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 403, 23))
        self.menubar.setObjectName("menubar")
        StockFinder.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(StockFinder)
        self.statusbar.setObjectName("statusbar")
        StockFinder.setStatusBar(self.statusbar)

        self.retranslateUi(StockFinder)
        QtCore.QMetaObject.connectSlotsByName(StockFinder)

    def retranslateUi(self, StockFinder):
        _translate = QtCore.QCoreApplication.translate
        StockFinder.setWindowTitle(_translate("StockFinder", "技术指标选股"))
