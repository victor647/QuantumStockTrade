# Form implementation generated from reading ui file 'FiveDayMatches.ui'
#
# Created by: PyQt6 UI code generator 6.9.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_FiveDayMatches(object):
    def setupUi(self, FiveDayMatches):
        FiveDayMatches.setObjectName("FiveDayMatches")
        FiveDayMatches.resize(473, 246)
        self.verticalLayout = QtWidgets.QVBoxLayout(FiveDayMatches)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblMatchesSummary = QtWidgets.QLabel(parent=FiveDayMatches)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.lblMatchesSummary.setFont(font)
        self.lblMatchesSummary.setObjectName("lblMatchesSummary")
        self.verticalLayout.addWidget(self.lblMatchesSummary)
        self.tblMatches = QtWidgets.QTableWidget(parent=FiveDayMatches)
        self.tblMatches.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tblMatches.setObjectName("tblMatches")
        self.tblMatches.setColumnCount(7)
        self.tblMatches.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tblMatches.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblMatches.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblMatches.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblMatches.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblMatches.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblMatches.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblMatches.setHorizontalHeaderItem(6, item)
        self.tblMatches.horizontalHeader().setDefaultSectionSize(60)
        self.verticalLayout.addWidget(self.tblMatches)

        self.retranslateUi(FiveDayMatches)
        self.tblMatches.cellDoubleClicked['int','int'].connect(FiveDayMatches.stock_detailed_info) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(FiveDayMatches)

    def retranslateUi(self, FiveDayMatches):
        _translate = QtCore.QCoreApplication.translate
        FiveDayMatches.setWindowTitle(_translate("FiveDayMatches", "五日图形选股结果"))
        self.lblMatchesSummary.setText(_translate("FiveDayMatches", "共出现0次图形匹配，出现后平均5日涨幅0%"))
        self.tblMatches.setSortingEnabled(True)
        item = self.tblMatches.horizontalHeaderItem(0)
        item.setText(_translate("FiveDayMatches", "股票代码"))
        item = self.tblMatches.horizontalHeaderItem(1)
        item.setText(_translate("FiveDayMatches", "股票名称"))
        item = self.tblMatches.horizontalHeaderItem(2)
        item.setText(_translate("FiveDayMatches", "出现日期"))
        item = self.tblMatches.horizontalHeaderItem(3)
        item.setText(_translate("FiveDayMatches", "次日涨幅"))
        item = self.tblMatches.horizontalHeaderItem(4)
        item.setText(_translate("FiveDayMatches", "3日涨幅"))
        item = self.tblMatches.horizontalHeaderItem(5)
        item.setText(_translate("FiveDayMatches", "5日涨幅"))
        item = self.tblMatches.horizontalHeaderItem(6)
        item.setText(_translate("FiveDayMatches", "10日涨幅"))
