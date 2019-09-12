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
        SearchResult.resize(478, 377)
        self.tblStockList = QtWidgets.QTableWidget(SearchResult)
        self.tblStockList.setGeometry(QtCore.QRect(21, 40, 441, 311))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.tblStockList.setFont(font)
        self.tblStockList.setObjectName("tblStockList")
        self.tblStockList.setColumnCount(5)
        self.tblStockList.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tblStockList.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblStockList.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblStockList.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblStockList.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblStockList.setHorizontalHeaderItem(4, item)
        self.tblStockList.horizontalHeader().setDefaultSectionSize(60)
        self.tblStockList.horizontalHeader().setSortIndicatorShown(True)
        self.lblTotalStockFound = QtWidgets.QLabel(SearchResult)
        self.lblTotalStockFound.setGeometry(QtCore.QRect(21, 11, 181, 16))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.lblTotalStockFound.setFont(font)
        self.lblTotalStockFound.setObjectName("lblTotalStockFound")

        self.retranslateUi(SearchResult)
        self.tblStockList.cellDoubleClicked['int','int'].connect(SearchResult.open_stock_page)
        QtCore.QMetaObject.connectSlotsByName(SearchResult)

    def retranslateUi(self, SearchResult):
        _translate = QtCore.QCoreApplication.translate
        SearchResult.setWindowTitle(_translate("SearchResult", "股票搜索结果"))
        item = self.tblStockList.horizontalHeaderItem(0)
        item.setText(_translate("SearchResult", "股票代码"))
        item = self.tblStockList.horizontalHeaderItem(1)
        item.setText(_translate("SearchResult", "股票名称"))
        item = self.tblStockList.horizontalHeaderItem(2)
        item.setText(_translate("SearchResult", "市盈率"))
        item = self.tblStockList.horizontalHeaderItem(3)
        item.setText(_translate("SearchResult", "市净率"))
        item = self.tblStockList.horizontalHeaderItem(4)
        item.setText(_translate("SearchResult", "总市值"))
        self.lblTotalStockFound.setText(_translate("SearchResult", "共找到0只股票！"))
