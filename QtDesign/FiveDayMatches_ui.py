# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FiveDayMatches.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FiveDayMatches(object):
    def setupUi(self, FiveDayMatches):
        FiveDayMatches.setObjectName("FiveDayMatches")
        FiveDayMatches.resize(473, 246)
        self.verticalLayout = QtWidgets.QVBoxLayout(FiveDayMatches)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblTotalMatchesFound = QtWidgets.QLabel(FiveDayMatches)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.lblTotalMatchesFound.setFont(font)
        self.lblTotalMatchesFound.setObjectName("lblTotalMatchesFound")
        self.verticalLayout.addWidget(self.lblTotalMatchesFound)
        self.tableWidget = QtWidgets.QTableWidget(FiveDayMatches)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(60)
        self.verticalLayout.addWidget(self.tableWidget)

        self.retranslateUi(FiveDayMatches)
        QtCore.QMetaObject.connectSlotsByName(FiveDayMatches)

    def retranslateUi(self, FiveDayMatches):
        _translate = QtCore.QCoreApplication.translate
        FiveDayMatches.setWindowTitle(_translate("FiveDayMatches", "五日图形选股结果"))
        self.lblTotalMatchesFound.setText(_translate("FiveDayMatches", "共出现0次图形匹配，出现后平均5日涨幅0%"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("FiveDayMatches", "股票代码"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("FiveDayMatches", "股票名称"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("FiveDayMatches", "出现日期"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("FiveDayMatches", "次日涨幅"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("FiveDayMatches", "3日涨幅"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("FiveDayMatches", "5日涨幅"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("FiveDayMatches", "10日涨幅"))
