# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TradeSimulator.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TradeSimulator(object):
    def setupUi(self, TradeSimulator):
        TradeSimulator.setObjectName("TradeSimulator")
        TradeSimulator.resize(1122, 763)
        self.tblTradeHistory = QtWidgets.QTableWidget(TradeSimulator)
        self.tblTradeHistory.setGeometry(QtCore.QRect(10, 90, 1101, 661))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.tblTradeHistory.setFont(font)
        self.tblTradeHistory.setRowCount(0)
        self.tblTradeHistory.setColumnCount(14)
        self.tblTradeHistory.setObjectName("tblTradeHistory")
        item = QtWidgets.QTableWidgetItem()
        self.tblTradeHistory.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblTradeHistory.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblTradeHistory.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblTradeHistory.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblTradeHistory.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblTradeHistory.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblTradeHistory.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblTradeHistory.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblTradeHistory.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblTradeHistory.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblTradeHistory.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblTradeHistory.setHorizontalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblTradeHistory.setHorizontalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblTradeHistory.setHorizontalHeaderItem(13, item)
        self.tblTradeHistory.horizontalHeader().setDefaultSectionSize(70)
        self.tblTradeHistory.verticalHeader().setDefaultSectionSize(25)
        self.layoutWidget = QtWidgets.QWidget(TradeSimulator)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 531, 71))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.layoutWidget.setFont(font)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblBuyCount = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.lblBuyCount.setFont(font)
        self.lblBuyCount.setObjectName("lblBuyCount")
        self.horizontalLayout.addWidget(self.lblBuyCount)
        self.lblSellCount = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.lblSellCount.setFont(font)
        self.lblSellCount.setObjectName("lblSellCount")
        self.horizontalLayout.addWidget(self.lblSellCount)
        self.lblSameDayPerformance = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.lblSameDayPerformance.setFont(font)
        self.lblSameDayPerformance.setObjectName("lblSameDayPerformance")
        self.horizontalLayout.addWidget(self.lblSameDayPerformance)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lblOriginalInvestment = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.lblOriginalInvestment.setFont(font)
        self.lblOriginalInvestment.setObjectName("lblOriginalInvestment")
        self.horizontalLayout_2.addWidget(self.lblOriginalInvestment)
        self.lblFinalAsset = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.lblFinalAsset.setFont(font)
        self.lblFinalAsset.setObjectName("lblFinalAsset")
        self.horizontalLayout_2.addWidget(self.lblFinalAsset)
        self.lblTotalProfit = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.lblTotalProfit.setFont(font)
        self.lblTotalProfit.setObjectName("lblTotalProfit")
        self.horizontalLayout_2.addWidget(self.lblTotalProfit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lblTotalReturn = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.lblTotalReturn.setFont(font)
        self.lblTotalReturn.setObjectName("lblTotalReturn")
        self.horizontalLayout_3.addWidget(self.lblTotalReturn)
        self.lblTotalFee = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.lblTotalFee.setFont(font)
        self.lblTotalFee.setObjectName("lblTotalFee")
        self.horizontalLayout_3.addWidget(self.lblTotalFee)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.btnShowDiagram = QtWidgets.QPushButton(TradeSimulator)
        self.btnShowDiagram.setGeometry(QtCore.QRect(560, 10, 91, 23))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        self.btnShowDiagram.setFont(font)
        self.btnShowDiagram.setObjectName("btnShowDiagram")

        self.retranslateUi(TradeSimulator)
        self.btnShowDiagram.clicked.connect(TradeSimulator.show_history_diagram)
        QtCore.QMetaObject.connectSlotsByName(TradeSimulator)

    def retranslateUi(self, TradeSimulator):
        _translate = QtCore.QCoreApplication.translate
        TradeSimulator.setWindowTitle(_translate("TradeSimulator", "模拟交易"))
        item = self.tblTradeHistory.horizontalHeaderItem(0)
        item.setText(_translate("TradeSimulator", "交易时间"))
        item = self.tblTradeHistory.horizontalHeaderItem(1)
        item.setText(_translate("TradeSimulator", "交易操作"))
        item = self.tblTradeHistory.horizontalHeaderItem(2)
        item.setText(_translate("TradeSimulator", "成交价格"))
        item = self.tblTradeHistory.horizontalHeaderItem(3)
        item.setText(_translate("TradeSimulator", "成交数量"))
        item = self.tblTradeHistory.horizontalHeaderItem(4)
        item.setText(_translate("TradeSimulator", "持仓股数"))
        item = self.tblTradeHistory.horizontalHeaderItem(5)
        item.setText(_translate("TradeSimulator", "当日开盘"))
        item = self.tblTradeHistory.horizontalHeaderItem(6)
        item.setText(_translate("TradeSimulator", "当日最高"))
        item = self.tblTradeHistory.horizontalHeaderItem(7)
        item.setText(_translate("TradeSimulator", "当日最低"))
        item = self.tblTradeHistory.horizontalHeaderItem(8)
        item.setText(_translate("TradeSimulator", "当日收盘"))
        item = self.tblTradeHistory.horizontalHeaderItem(9)
        item.setText(_translate("TradeSimulator", "当日换手"))
        item = self.tblTradeHistory.horizontalHeaderItem(10)
        item.setText(_translate("TradeSimulator", "运行趋势 / 多空信号"))
        item = self.tblTradeHistory.horizontalHeaderItem(11)
        item.setText(_translate("TradeSimulator", "平均成本"))
        item = self.tblTradeHistory.horizontalHeaderItem(12)
        item.setText(_translate("TradeSimulator", "累计收益"))
        item = self.tblTradeHistory.horizontalHeaderItem(13)
        item.setText(_translate("TradeSimulator", "盈亏比例"))
        self.lblBuyCount.setText(_translate("TradeSimulator", "买入次数："))
        self.lblSellCount.setText(_translate("TradeSimulator", "卖出次数："))
        self.lblSameDayPerformance.setText(_translate("TradeSimulator", "做T次数："))
        self.lblOriginalInvestment.setText(_translate("TradeSimulator", "初始成本："))
        self.lblFinalAsset.setText(_translate("TradeSimulator", "最终资产："))
        self.lblTotalProfit.setText(_translate("TradeSimulator", "累计收益："))
        self.lblTotalReturn.setText(_translate("TradeSimulator", "盈亏比例："))
        self.lblTotalFee.setText(_translate("TradeSimulator", "总手续费："))
        self.btnShowDiagram.setText(_translate("TradeSimulator", "显示K线图"))
