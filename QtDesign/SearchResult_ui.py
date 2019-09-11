# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SearchResult.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SearchResult(object):
    def setupUi(self, SearchResult):
        SearchResult.setObjectName("SearchResult")
        SearchResult.resize(400, 300)
        self.tblStockList = QtWidgets.QTableWidget(SearchResult)
        self.tblStockList.setGeometry(QtCore.QRect(20, 20, 361, 261))
        self.tblStockList.setObjectName("tblStockList")
        self.tblStockList.setColumnCount(2)
        self.tblStockList.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tblStockList.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblStockList.setHorizontalHeaderItem(1, item)

        self.retranslateUi(SearchResult)
        QtCore.QMetaObject.connectSlotsByName(SearchResult)

    def retranslateUi(self, SearchResult):
        _translate = QtCore.QCoreApplication.translate
        SearchResult.setWindowTitle(_translate("SearchResult", "股票搜索结果"))
        item = self.tblStockList.horizontalHeaderItem(0)
        item.setText(_translate("SearchResult", "股票代码"))
        item = self.tblStockList.horizontalHeaderItem(1)
        item.setText(_translate("SearchResult", "股票名称"))
