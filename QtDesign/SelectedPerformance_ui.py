# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SelectedPerformance.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SelectedPerformance(object):
    def setupUi(self, SelectedPerformance):
        SelectedPerformance.setObjectName("SelectedPerformance")
        SelectedPerformance.resize(1171, 429)
        self.centralwidget = QtWidgets.QWidget(SelectedPerformance)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lblSearchDate = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.lblSearchDate.setFont(font)
        self.lblSearchDate.setObjectName("lblSearchDate")
        self.horizontalLayout_2.addWidget(self.lblSearchDate)
        self.dteSearchDate = QtWidgets.QDateEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.dteSearchDate.setFont(font)
        self.dteSearchDate.setObjectName("dteSearchDate")
        self.horizontalLayout_2.addWidget(self.dteSearchDate)
        self.lblNewStockCode = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.lblNewStockCode.setFont(font)
        self.lblNewStockCode.setObjectName("lblNewStockCode")
        self.horizontalLayout_2.addWidget(self.lblNewStockCode)
        self.iptStockCode = QtWidgets.QLineEdit(self.centralwidget)
        self.iptStockCode.setMaximumSize(QtCore.QSize(70, 16777215))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.iptStockCode.setFont(font)
        self.iptStockCode.setMaxLength(6)
        self.iptStockCode.setObjectName("iptStockCode")
        self.horizontalLayout_2.addWidget(self.iptStockCode)
        self.btnAddStock = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.btnAddStock.setFont(font)
        self.btnAddStock.setObjectName("btnAddStock")
        self.horizontalLayout_2.addWidget(self.btnAddStock)
        self.btnRemoveStock = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.btnRemoveStock.setFont(font)
        self.btnRemoveStock.setObjectName("btnRemoveStock")
        self.horizontalLayout_2.addWidget(self.btnRemoveStock)
        self.btnClearStocks = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.btnClearStocks.setFont(font)
        self.btnClearStocks.setObjectName("btnClearStocks")
        self.horizontalLayout_2.addWidget(self.btnClearStocks)
        self.btnExportStockList = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.btnExportStockList.setFont(font)
        self.btnExportStockList.setObjectName("btnExportStockList")
        self.horizontalLayout_2.addWidget(self.btnExportStockList)
        self.btnImportStockList = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.btnImportStockList.setFont(font)
        self.btnImportStockList.setObjectName("btnImportStockList")
        self.horizontalLayout_2.addWidget(self.btnImportStockList)
        self.btnExportStrategy = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.btnExportStrategy.setFont(font)
        self.btnExportStrategy.setObjectName("btnExportStrategy")
        self.horizontalLayout_2.addWidget(self.btnExportStrategy)
        self.btnImporttrategy = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.btnImporttrategy.setFont(font)
        self.btnImporttrategy.setObjectName("btnImporttrategy")
        self.horizontalLayout_2.addWidget(self.btnImporttrategy)
        self.btnStartCalculation = QtWidgets.QPushButton(self.centralwidget)
        self.btnStartCalculation.setMinimumSize(QtCore.QSize(120, 0))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.btnStartCalculation.setFont(font)
        self.btnStartCalculation.setObjectName("btnStartCalculation")
        self.horizontalLayout_2.addWidget(self.btnStartCalculation)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblMoneyPerTrade = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.lblMoneyPerTrade.setFont(font)
        self.lblMoneyPerTrade.setObjectName("lblMoneyPerTrade")
        self.horizontalLayout.addWidget(self.lblMoneyPerTrade)
        self.spbMoneyPerTrade = QtWidgets.QSpinBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.spbMoneyPerTrade.setFont(font)
        self.spbMoneyPerTrade.setMinimum(5000)
        self.spbMoneyPerTrade.setMaximum(5000000)
        self.spbMoneyPerTrade.setSingleStep(1000)
        self.spbMoneyPerTrade.setProperty("value", 30000)
        self.spbMoneyPerTrade.setObjectName("spbMoneyPerTrade")
        self.horizontalLayout.addWidget(self.spbMoneyPerTrade)
        self.rbnNeverAdd = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.rbnNeverAdd.setFont(font)
        self.rbnNeverAdd.setObjectName("rbnNeverAdd")
        self.horizontalLayout.addWidget(self.rbnNeverAdd)
        self.rbnAddByMa = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.rbnAddByMa.setFont(font)
        self.rbnAddByMa.setChecked(True)
        self.rbnAddByMa.setObjectName("rbnAddByMa")
        self.horizontalLayout.addWidget(self.rbnAddByMa)
        self.spbAddMaPeriod = QtWidgets.QSpinBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.spbAddMaPeriod.setFont(font)
        self.spbAddMaPeriod.setMinimum(3)
        self.spbAddMaPeriod.setMaximum(20)
        self.spbAddMaPeriod.setProperty("value", 5)
        self.spbAddMaPeriod.setObjectName("spbAddMaPeriod")
        self.horizontalLayout.addWidget(self.spbAddMaPeriod)
        self.lblAddByMa = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lblAddByMa.setFont(font)
        self.lblAddByMa.setObjectName("lblAddByMa")
        self.horizontalLayout.addWidget(self.lblAddByMa)
        self.rbnAddByPercent = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.rbnAddByPercent.setFont(font)
        self.rbnAddByPercent.setObjectName("rbnAddByPercent")
        self.horizontalLayout.addWidget(self.rbnAddByPercent)
        self.spbAddPercent = QtWidgets.QSpinBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.spbAddPercent.setFont(font)
        self.spbAddPercent.setMinimum(-50)
        self.spbAddPercent.setMaximum(50)
        self.spbAddPercent.setProperty("value", -3)
        self.spbAddPercent.setObjectName("spbAddPercent")
        self.horizontalLayout.addWidget(self.spbAddPercent)
        self.lblAddByPercent = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lblAddByPercent.setFont(font)
        self.lblAddByPercent.setObjectName("lblAddByPercent")
        self.horizontalLayout.addWidget(self.lblAddByPercent)
        self.cbxClearByEarning = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.cbxClearByEarning.setFont(font)
        self.cbxClearByEarning.setChecked(True)
        self.cbxClearByEarning.setObjectName("cbxClearByEarning")
        self.horizontalLayout.addWidget(self.cbxClearByEarning)
        self.spbClearEarning = QtWidgets.QSpinBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.spbClearEarning.setFont(font)
        self.spbClearEarning.setMinimum(100)
        self.spbClearEarning.setMaximum(1000000)
        self.spbClearEarning.setSingleStep(1)
        self.spbClearEarning.setProperty("value", 4000)
        self.spbClearEarning.setObjectName("spbClearEarning")
        self.horizontalLayout.addWidget(self.spbClearEarning)
        self.cbxClearByLosing = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.cbxClearByLosing.setFont(font)
        self.cbxClearByLosing.setChecked(True)
        self.cbxClearByLosing.setObjectName("cbxClearByLosing")
        self.horizontalLayout.addWidget(self.cbxClearByLosing)
        self.spbClearLosing = QtWidgets.QSpinBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.spbClearLosing.setFont(font)
        self.spbClearLosing.setMinimum(-1000000)
        self.spbClearLosing.setMaximum(-100)
        self.spbClearLosing.setProperty("value", -2000)
        self.spbClearLosing.setObjectName("spbClearLosing")
        self.horizontalLayout.addWidget(self.spbClearLosing)
        self.cbxClearByMa = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.cbxClearByMa.setFont(font)
        self.cbxClearByMa.setChecked(True)
        self.cbxClearByMa.setObjectName("cbxClearByMa")
        self.horizontalLayout.addWidget(self.cbxClearByMa)
        self.spbClearMaPeriod = QtWidgets.QSpinBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.spbClearMaPeriod.setFont(font)
        self.spbClearMaPeriod.setMinimum(5)
        self.spbClearMaPeriod.setMaximum(60)
        self.spbClearMaPeriod.setObjectName("spbClearMaPeriod")
        self.horizontalLayout.addWidget(self.spbClearMaPeriod)
        self.lblClearByMa = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lblClearByMa.setFont(font)
        self.lblClearByMa.setObjectName("lblClearByMa")
        self.horizontalLayout.addWidget(self.lblClearByMa)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tblStockList = QtWidgets.QTableWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.tblStockList.setFont(font)
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
        self.tblStockList.horizontalHeader().setDefaultSectionSize(90)
        self.tblStockList.horizontalHeader().setSortIndicatorShown(True)
        self.verticalLayout.addWidget(self.tblStockList)
        self.lblTradeSummary = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.lblTradeSummary.setFont(font)
        self.lblTradeSummary.setObjectName("lblTradeSummary")
        self.verticalLayout.addWidget(self.lblTradeSummary)
        SelectedPerformance.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(SelectedPerformance)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1171, 22))
        self.menubar.setObjectName("menubar")
        SelectedPerformance.setMenuBar(self.menubar)
        self.actHoldersStatus = QtWidgets.QAction(SelectedPerformance)
        self.actHoldersStatus.setObjectName("actHoldersStatus")
        self.actAutoTest = QtWidgets.QAction(SelectedPerformance)
        self.actAutoTest.setObjectName("actAutoTest")

        self.retranslateUi(SelectedPerformance)
        self.btnStartCalculation.clicked.connect(SelectedPerformance.start_trade_simulation)
        self.btnImportStockList.clicked.connect(SelectedPerformance.import_stock_list)
        self.btnRemoveStock.clicked.connect(SelectedPerformance.remove_stock_code)
        self.btnAddStock.clicked.connect(SelectedPerformance.add_stock_code)
        self.btnClearStocks.clicked.connect(SelectedPerformance.clear_stock_list)
        self.btnExportStockList.clicked.connect(SelectedPerformance.export_stock_list)
        self.dteSearchDate.editingFinished.connect(SelectedPerformance.update_start_date)
        self.tblStockList.cellDoubleClicked['int','int'].connect(SelectedPerformance.show_stock_graph)
        self.cbxClearByLosing.toggled['bool'].connect(self.spbClearLosing.setEnabled)
        self.cbxClearByEarning.toggled['bool'].connect(self.spbClearEarning.setEnabled)
        self.btnExportStrategy.clicked.connect(SelectedPerformance.export_trade_strategy)
        self.btnImporttrategy.clicked.connect(SelectedPerformance.import_trade_strategy)
        QtCore.QMetaObject.connectSlotsByName(SelectedPerformance)

    def retranslateUi(self, SelectedPerformance):
        _translate = QtCore.QCoreApplication.translate
        SelectedPerformance.setWindowTitle(_translate("SelectedPerformance", "选股器回测"))
        self.lblSearchDate.setText(_translate("SelectedPerformance", "选股日期："))
        self.dteSearchDate.setDisplayFormat(_translate("SelectedPerformance", "yyyy-MM-dd"))
        self.lblNewStockCode.setText(_translate("SelectedPerformance", "股票代码/名称"))
        self.iptStockCode.setText(_translate("SelectedPerformance", "贵州茅台"))
        self.btnAddStock.setText(_translate("SelectedPerformance", "添加股票"))
        self.btnRemoveStock.setText(_translate("SelectedPerformance", "删除股票"))
        self.btnClearStocks.setText(_translate("SelectedPerformance", "清空股票列表"))
        self.btnExportStockList.setText(_translate("SelectedPerformance", "导出股票列表"))
        self.btnImportStockList.setText(_translate("SelectedPerformance", "导入股票列表"))
        self.btnExportStrategy.setText(_translate("SelectedPerformance", "导出操作策略"))
        self.btnImporttrategy.setText(_translate("SelectedPerformance", "导入操作策略"))
        self.btnStartCalculation.setText(_translate("SelectedPerformance", "获取回测数据"))
        self.lblMoneyPerTrade.setText(_translate("SelectedPerformance", "每支股票买入底仓"))
        self.spbMoneyPerTrade.setSuffix(_translate("SelectedPerformance", "元"))
        self.rbnNeverAdd.setText(_translate("SelectedPerformance", "从不补仓"))
        self.rbnAddByMa.setText(_translate("SelectedPerformance", "回踩"))
        self.spbAddMaPeriod.setSuffix(_translate("SelectedPerformance", "日"))
        self.lblAddByMa.setText(_translate("SelectedPerformance", "均线补仓"))
        self.rbnAddByPercent.setText(_translate("SelectedPerformance", "涨跌幅达到"))
        self.spbAddPercent.setSuffix(_translate("SelectedPerformance", "%"))
        self.lblAddByPercent.setText(_translate("SelectedPerformance", "补仓"))
        self.cbxClearByEarning.setText(_translate("SelectedPerformance", "获利止盈"))
        self.spbClearEarning.setSuffix(_translate("SelectedPerformance", "元"))
        self.cbxClearByLosing.setText(_translate("SelectedPerformance", "割肉止损"))
        self.spbClearLosing.setSuffix(_translate("SelectedPerformance", "元"))
        self.cbxClearByMa.setText(_translate("SelectedPerformance", "收盘跌破"))
        self.spbClearMaPeriod.setSuffix(_translate("SelectedPerformance", "日"))
        self.lblClearByMa.setText(_translate("SelectedPerformance", "均线清仓"))
        self.tblStockList.setSortingEnabled(True)
        item = self.tblStockList.horizontalHeaderItem(0)
        item.setText(_translate("SelectedPerformance", "股票代码"))
        item = self.tblStockList.horizontalHeaderItem(1)
        item.setText(_translate("SelectedPerformance", "股票名称"))
        item = self.tblStockList.horizontalHeaderItem(2)
        item.setText(_translate("SelectedPerformance", "选股日期"))
        item = self.tblStockList.horizontalHeaderItem(3)
        item.setText(_translate("SelectedPerformance", "当日收盘"))
        item = self.tblStockList.horizontalHeaderItem(4)
        item.setText(_translate("SelectedPerformance", "次日开盘"))
        item = self.tblStockList.horizontalHeaderItem(5)
        item.setText(_translate("SelectedPerformance", "清仓日期"))
        item = self.tblStockList.horizontalHeaderItem(6)
        item.setText(_translate("SelectedPerformance", "清仓时涨幅"))
        item = self.tblStockList.horizontalHeaderItem(7)
        item.setText(_translate("SelectedPerformance", "期间最高涨幅"))
        item = self.tblStockList.horizontalHeaderItem(8)
        item.setText(_translate("SelectedPerformance", "期间最大回撤"))
        item = self.tblStockList.horizontalHeaderItem(9)
        item.setText(_translate("SelectedPerformance", "最佳操作策略"))
        item = self.tblStockList.horizontalHeaderItem(10)
        item.setText(_translate("SelectedPerformance", "实际操作记录"))
        self.lblTradeSummary.setText(_translate("SelectedPerformance", "共买入0只股票，盈利0只，成本0元，获利0元，收益率0%"))
        self.actHoldersStatus.setText(_translate("SelectedPerformance", "十大流通股东"))
        self.actAutoTest.setText(_translate("SelectedPerformance", "导入多个股票列表"))
