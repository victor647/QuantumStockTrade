# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PoolMonitor.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PoolMonitor(object):
    def setupUi(self, PoolMonitor):
        PoolMonitor.setObjectName("PoolMonitor")
        PoolMonitor.resize(872, 836)
        self.verticalLayout = QtWidgets.QVBoxLayout(PoolMonitor)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnImportStockList = QtWidgets.QPushButton(PoolMonitor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnImportStockList.sizePolicy().hasHeightForWidth())
        self.btnImportStockList.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.btnImportStockList.setFont(font)
        self.btnImportStockList.setObjectName("btnImportStockList")
        self.horizontalLayout.addWidget(self.btnImportStockList)
        self.btnStartAnalyze = QtWidgets.QPushButton(PoolMonitor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnStartAnalyze.sizePolicy().hasHeightForWidth())
        self.btnStartAnalyze.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.btnStartAnalyze.setFont(font)
        self.btnStartAnalyze.setObjectName("btnStartAnalyze")
        self.horizontalLayout.addWidget(self.btnStartAnalyze)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tblStockList = QtWidgets.QTableWidget(PoolMonitor)
        self.tblStockList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tblStockList.setObjectName("tblStockList")
        self.tblStockList.setColumnCount(11)
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
        self.tblStockList.horizontalHeader().setDefaultSectionSize(80)
        self.verticalLayout.addWidget(self.tblStockList)

        self.retranslateUi(PoolMonitor)
        QtCore.QMetaObject.connectSlotsByName(PoolMonitor)

    def retranslateUi(self, PoolMonitor):
        _translate = QtCore.QCoreApplication.translate
        PoolMonitor.setWindowTitle(_translate("PoolMonitor", "股池每日监测"))
        self.btnImportStockList.setText(_translate("PoolMonitor", "导入股池列表"))
        self.btnStartAnalyze.setText(_translate("PoolMonitor", "开始分析计算"))
        self.tblStockList.setSortingEnabled(True)
        item = self.tblStockList.horizontalHeaderItem(0)
        item.setText(_translate("PoolMonitor", "股票代码"))
        item = self.tblStockList.horizontalHeaderItem(1)
        item.setText(_translate("PoolMonitor", "股票名称"))
        item = self.tblStockList.horizontalHeaderItem(2)
        item.setText(_translate("PoolMonitor", "最新价格"))
        item = self.tblStockList.horizontalHeaderItem(3)
        item.setText(_translate("PoolMonitor", "3日涨跌幅"))
        item = self.tblStockList.horizontalHeaderItem(4)
        item.setText(_translate("PoolMonitor", "历史最高"))
        item = self.tblStockList.horizontalHeaderItem(5)
        item.setText(_translate("PoolMonitor", "回撤幅度"))
        item = self.tblStockList.horizontalHeaderItem(6)
        item.setText(_translate("PoolMonitor", "距离MA5"))
        item = self.tblStockList.horizontalHeaderItem(7)
        item.setText(_translate("PoolMonitor", "距离MA20"))
        item = self.tblStockList.horizontalHeaderItem(8)
        item.setText(_translate("PoolMonitor", "距离MA60"))
        item = self.tblStockList.horizontalHeaderItem(9)
        item.setText(_translate("PoolMonitor", "距离MA120"))
        item = self.tblStockList.horizontalHeaderItem(10)
        item.setText(_translate("PoolMonitor", "距离MA250"))
