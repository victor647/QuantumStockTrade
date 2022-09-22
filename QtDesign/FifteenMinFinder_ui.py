# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FifteenMinFinder.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FifteenMinFinder(object):
    def setupUi(self, FifteenMinFinder):
        FifteenMinFinder.setObjectName("FifteenMinFinder")
        FifteenMinFinder.resize(416, 410)
        self.verticalLayout = QtWidgets.QVBoxLayout(FifteenMinFinder)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btnImportStockPool = QtWidgets.QPushButton(FifteenMinFinder)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.btnImportStockPool.setFont(font)
        self.btnImportStockPool.setObjectName("btnImportStockPool")
        self.horizontalLayout_2.addWidget(self.btnImportStockPool)
        self.lblMAShort = QtWidgets.QLabel(FifteenMinFinder)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lblMAShort.setFont(font)
        self.lblMAShort.setObjectName("lblMAShort")
        self.horizontalLayout_2.addWidget(self.lblMAShort)
        self.spbMAShortPeriod = QtWidgets.QSpinBox(FifteenMinFinder)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.spbMAShortPeriod.setFont(font)
        self.spbMAShortPeriod.setMinimum(5)
        self.spbMAShortPeriod.setMaximum(100)
        self.spbMAShortPeriod.setProperty("value", 65)
        self.spbMAShortPeriod.setObjectName("spbMAShortPeriod")
        self.horizontalLayout_2.addWidget(self.spbMAShortPeriod)
        self.lblMALong = QtWidgets.QLabel(FifteenMinFinder)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lblMALong.setFont(font)
        self.lblMALong.setObjectName("lblMALong")
        self.horizontalLayout_2.addWidget(self.lblMALong)
        self.spbMALongPeriod = QtWidgets.QSpinBox(FifteenMinFinder)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.spbMALongPeriod.setFont(font)
        self.spbMALongPeriod.setMinimum(20)
        self.spbMALongPeriod.setMaximum(200)
        self.spbMALongPeriod.setProperty("value", 130)
        self.spbMALongPeriod.setObjectName("spbMALongPeriod")
        self.horizontalLayout_2.addWidget(self.spbMALongPeriod)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(FifteenMinFinder)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.spbOccurancePeriod = QtWidgets.QSpinBox(FifteenMinFinder)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.spbOccurancePeriod.setFont(font)
        self.spbOccurancePeriod.setMaximum(20)
        self.spbOccurancePeriod.setProperty("value", 10)
        self.spbOccurancePeriod.setObjectName("spbOccurancePeriod")
        self.horizontalLayout_3.addWidget(self.spbOccurancePeriod)
        self.label_2 = QtWidgets.QLabel(FifteenMinFinder)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.rbnStayOnShort = QtWidgets.QRadioButton(FifteenMinFinder)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.rbnStayOnShort.setFont(font)
        self.rbnStayOnShort.setAutoExclusive(False)
        self.rbnStayOnShort.setObjectName("rbnStayOnShort")
        self.horizontalLayout_3.addWidget(self.rbnStayOnShort)
        self.rbnGoldCross = QtWidgets.QRadioButton(FifteenMinFinder)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.rbnGoldCross.setFont(font)
        self.rbnGoldCross.setChecked(True)
        self.rbnGoldCross.setAutoExclusive(False)
        self.rbnGoldCross.setObjectName("rbnGoldCross")
        self.horizontalLayout_3.addWidget(self.rbnGoldCross)
        self.rbnOppositeDirection = QtWidgets.QRadioButton(FifteenMinFinder)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.rbnOppositeDirection.setFont(font)
        self.rbnOppositeDirection.setAutoExclusive(False)
        self.rbnOppositeDirection.setObjectName("rbnOppositeDirection")
        self.horizontalLayout_3.addWidget(self.rbnOppositeDirection)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.tblStockList = QtWidgets.QTableWidget(FifteenMinFinder)
        self.tblStockList.setObjectName("tblStockList")
        self.tblStockList.setColumnCount(4)
        self.tblStockList.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tblStockList.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblStockList.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblStockList.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblStockList.setHorizontalHeaderItem(3, item)
        self.verticalLayout.addWidget(self.tblStockList)

        self.retranslateUi(FifteenMinFinder)
        QtCore.QMetaObject.connectSlotsByName(FifteenMinFinder)

    def retranslateUi(self, FifteenMinFinder):
        _translate = QtCore.QCoreApplication.translate
        FifteenMinFinder.setWindowTitle(_translate("FifteenMinFinder", "15分钟选股"))
        self.btnImportStockPool.setText(_translate("FifteenMinFinder", "导入股池"))
        self.lblMAShort.setText(_translate("FifteenMinFinder", "短期均线周期"))
        self.lblMALong.setText(_translate("FifteenMinFinder", "长期均线周期"))
        self.label.setText(_translate("FifteenMinFinder", "最近"))
        self.label_2.setText(_translate("FifteenMinFinder", "根K线内出现"))
        self.rbnStayOnShort.setText(_translate("FifteenMinFinder", "站稳短线"))
        self.rbnGoldCross.setText(_translate("FifteenMinFinder", "短长金叉"))
        self.rbnOppositeDirection.setText(_translate("FifteenMinFinder", "短上长下"))
        item = self.tblStockList.horizontalHeaderItem(0)
        item.setText(_translate("FifteenMinFinder", "股票代码"))
        item = self.tblStockList.horizontalHeaderItem(1)
        item.setText(_translate("FifteenMinFinder", "股票名称"))
        item = self.tblStockList.horizontalHeaderItem(2)
        item.setText(_translate("FifteenMinFinder", "当前价格"))
        item = self.tblStockList.horizontalHeaderItem(3)
        item.setText(_translate("FifteenMinFinder", "均线支撑"))
