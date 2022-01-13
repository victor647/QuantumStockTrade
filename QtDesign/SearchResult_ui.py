# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SearchResult.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SearchResult(object):
    def setupUi(self, SearchResult):
        SearchResult.setObjectName("SearchResult")
        SearchResult.resize(830, 311)
        self.verticalLayout = QtWidgets.QVBoxLayout(SearchResult)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lblTotalStockFound = QtWidgets.QLabel(SearchResult)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.lblTotalStockFound.setFont(font)
        self.lblTotalStockFound.setObjectName("lblTotalStockFound")
        self.horizontalLayout_2.addWidget(self.lblTotalStockFound)
        self.lblSearchDate = QtWidgets.QLabel(SearchResult)
        self.lblSearchDate.setMinimumSize(QtCore.QSize(150, 0))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.lblSearchDate.setFont(font)
        self.lblSearchDate.setObjectName("lblSearchDate")
        self.horizontalLayout_2.addWidget(self.lblSearchDate)
        self.btnDeleteStock = QtWidgets.QPushButton(SearchResult)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.btnDeleteStock.setFont(font)
        self.btnDeleteStock.setObjectName("btnDeleteStock")
        self.horizontalLayout_2.addWidget(self.btnDeleteStock)
        self.btnExportStockList = QtWidgets.QPushButton(SearchResult)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.btnExportStockList.setFont(font)
        self.btnExportStockList.setObjectName("btnExportStockList")
        self.horizontalLayout_2.addWidget(self.btnExportStockList)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.tblStockList = QtWidgets.QTableWidget(SearchResult)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.tblStockList.setFont(font)
        self.tblStockList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tblStockList.setObjectName("tblStockList")
        self.tblStockList.setColumnCount(12)
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
        item = QtWidgets.QTableWidgetItem()
        self.tblStockList.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblStockList.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblStockList.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblStockList.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblStockList.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblStockList.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblStockList.setHorizontalHeaderItem(11, item)
        self.tblStockList.horizontalHeader().setDefaultSectionSize(60)
        self.tblStockList.horizontalHeader().setSortIndicatorShown(True)
        self.verticalLayout.addWidget(self.tblStockList)

        self.retranslateUi(SearchResult)
        self.tblStockList.cellDoubleClicked['int','int'].connect(SearchResult.stock_detailed_info) # type: ignore
        self.btnExportStockList.clicked.connect(SearchResult.export_stock_list) # type: ignore
        self.btnDeleteStock.clicked.connect(SearchResult.delete_selected_stocks) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(SearchResult)

    def retranslateUi(self, SearchResult):
        _translate = QtCore.QCoreApplication.translate
        SearchResult.setWindowTitle(_translate("SearchResult", "股票搜索结果"))
        self.lblTotalStockFound.setText(_translate("SearchResult", "共找到0只股票！"))
        self.lblSearchDate.setText(_translate("SearchResult", "选股日期："))
        self.btnDeleteStock.setText(_translate("SearchResult", "删除选中股票"))
        self.btnExportStockList.setText(_translate("SearchResult", "导出选股列表"))
        self.tblStockList.setSortingEnabled(True)
        item = self.tblStockList.horizontalHeaderItem(0)
        item.setText(_translate("SearchResult", "股票代码"))
        item = self.tblStockList.horizontalHeaderItem(1)
        item.setText(_translate("SearchResult", "股票名称"))
        item = self.tblStockList.horizontalHeaderItem(2)
        item.setText(_translate("SearchResult", "收盘价"))
        item = self.tblStockList.horizontalHeaderItem(3)
        item.setText(_translate("SearchResult", "次日开盘"))
        item = self.tblStockList.horizontalHeaderItem(4)
        item.setText(_translate("SearchResult", "五日收盘"))
        item = self.tblStockList.horizontalHeaderItem(5)
        item.setText(_translate("SearchResult", "跑赢大盘"))
        item = self.tblStockList.horizontalHeaderItem(6)
        item.setText(_translate("SearchResult", "次日最低"))
        item = self.tblStockList.horizontalHeaderItem(7)
        item.setText(_translate("SearchResult", "五日最高"))
        item = self.tblStockList.horizontalHeaderItem(8)
        item.setText(_translate("SearchResult", "最大收益"))
        item = self.tblStockList.horizontalHeaderItem(9)
        item.setText(_translate("SearchResult", "市盈率"))
        item = self.tblStockList.horizontalHeaderItem(10)
        item.setText(_translate("SearchResult", "市净率"))
        item = self.tblStockList.horizontalHeaderItem(11)
        item.setText(_translate("SearchResult", "市销率"))
