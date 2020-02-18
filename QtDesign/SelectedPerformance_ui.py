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
        SelectedPerformance.resize(1191, 437)
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
        self.spbMoneyPerTrade.setProperty("value", 20000)
        self.spbMoneyPerTrade.setObjectName("spbMoneyPerTrade")
        self.horizontalLayout.addWidget(self.spbMoneyPerTrade)
        self.cbxLoseThreshold = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.cbxLoseThreshold.setFont(font)
        self.cbxLoseThreshold.setChecked(True)
        self.cbxLoseThreshold.setObjectName("cbxLoseThreshold")
        self.horizontalLayout.addWidget(self.cbxLoseThreshold)
        self.spbLoseThreshold = QtWidgets.QSpinBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.spbLoseThreshold.setFont(font)
        self.spbLoseThreshold.setMinimum(-1000000)
        self.spbLoseThreshold.setMaximum(-100)
        self.spbLoseThreshold.setProperty("value", -1000)
        self.spbLoseThreshold.setObjectName("spbLoseThreshold")
        self.horizontalLayout.addWidget(self.spbLoseThreshold)
        self.cbxWinThreshold = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.cbxWinThreshold.setFont(font)
        self.cbxWinThreshold.setChecked(True)
        self.cbxWinThreshold.setObjectName("cbxWinThreshold")
        self.horizontalLayout.addWidget(self.cbxWinThreshold)
        self.spbWinThreshold = QtWidgets.QSpinBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.spbWinThreshold.setFont(font)
        self.spbWinThreshold.setMinimum(100)
        self.spbWinThreshold.setMaximum(1000000)
        self.spbWinThreshold.setSingleStep(1)
        self.spbWinThreshold.setProperty("value", 2000)
        self.spbWinThreshold.setObjectName("spbWinThreshold")
        self.horizontalLayout.addWidget(self.spbWinThreshold)
        self.cbxAddWhenDown = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.cbxAddWhenDown.setFont(font)
        self.cbxAddWhenDown.setChecked(True)
        self.cbxAddWhenDown.setObjectName("cbxAddWhenDown")
        self.horizontalLayout.addWidget(self.cbxAddWhenDown)
        self.spbAddThresholdDown = QtWidgets.QSpinBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.spbAddThresholdDown.setFont(font)
        self.spbAddThresholdDown.setMinimum(-50)
        self.spbAddThresholdDown.setMaximum(0)
        self.spbAddThresholdDown.setProperty("value", -2)
        self.spbAddThresholdDown.setObjectName("spbAddThresholdDown")
        self.horizontalLayout.addWidget(self.spbAddThresholdDown)
        self.cbxAddWhenUp = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.cbxAddWhenUp.setFont(font)
        self.cbxAddWhenUp.setChecked(True)
        self.cbxAddWhenUp.setObjectName("cbxAddWhenUp")
        self.horizontalLayout.addWidget(self.cbxAddWhenUp)
        self.spbAddThresholdUp = QtWidgets.QSpinBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.spbAddThresholdUp.setFont(font)
        self.spbAddThresholdUp.setMinimum(0)
        self.spbAddThresholdUp.setMaximum(50)
        self.spbAddThresholdUp.setProperty("value", 2)
        self.spbAddThresholdUp.setObjectName("spbAddThresholdUp")
        self.horizontalLayout.addWidget(self.spbAddThresholdUp)
        self.lblAddDeadline = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.lblAddDeadline.setFont(font)
        self.lblAddDeadline.setObjectName("lblAddDeadline")
        self.horizontalLayout.addWidget(self.lblAddDeadline)
        self.spbAddDeadline = QtWidgets.QSpinBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.spbAddDeadline.setFont(font)
        self.spbAddDeadline.setMinimum(1)
        self.spbAddDeadline.setMaximum(20)
        self.spbAddDeadline.setSingleStep(1)
        self.spbAddDeadline.setProperty("value", 3)
        self.spbAddDeadline.setObjectName("spbAddDeadline")
        self.horizontalLayout.addWidget(self.spbAddDeadline)
        self.lblMaxHoldTime = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.lblMaxHoldTime.setFont(font)
        self.lblMaxHoldTime.setObjectName("lblMaxHoldTime")
        self.horizontalLayout.addWidget(self.lblMaxHoldTime)
        self.spbMaxHoldTime = QtWidgets.QSpinBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.spbMaxHoldTime.setFont(font)
        self.spbMaxHoldTime.setMinimum(2)
        self.spbMaxHoldTime.setMaximum(20)
        self.spbMaxHoldTime.setSingleStep(1)
        self.spbMaxHoldTime.setProperty("value", 5)
        self.spbMaxHoldTime.setObjectName("spbMaxHoldTime")
        self.horizontalLayout.addWidget(self.spbMaxHoldTime)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tblStockList = QtWidgets.QTableWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.tblStockList.setFont(font)
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
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1191, 22))
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
        self.cbxAddWhenUp.toggled['bool'].connect(self.spbAddThresholdUp.setEnabled)
        self.cbxAddWhenDown.toggled['bool'].connect(self.spbAddThresholdDown.setEnabled)
        self.dteSearchDate.editingFinished.connect(SelectedPerformance.update_start_date)
        self.tblStockList.cellDoubleClicked['int','int'].connect(SelectedPerformance.show_stock_graph)
        self.cbxLoseThreshold.toggled['bool'].connect(self.spbLoseThreshold.setEnabled)
        self.cbxWinThreshold.toggled['bool'].connect(self.spbWinThreshold.setEnabled)
        self.btnExportStrategy.clicked.connect(SelectedPerformance.export_trade_strategy)
        self.btnImporttrategy.clicked.connect(SelectedPerformance.import_trade_strategy)
        QtCore.QMetaObject.connectSlotsByName(SelectedPerformance)

    def retranslateUi(self, SelectedPerformance):
        _translate = QtCore.QCoreApplication.translate
        SelectedPerformance.setWindowTitle(_translate("SelectedPerformance", "选股器回测"))
        self.lblSearchDate.setText(_translate("SelectedPerformance", "选股日期（次日开盘买入）："))
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
        self.lblMoneyPerTrade.setText(_translate("SelectedPerformance", "操作策略：每支股票买入"))
        self.spbMoneyPerTrade.setSuffix(_translate("SelectedPerformance", "元"))
        self.cbxLoseThreshold.setText(_translate("SelectedPerformance", "割肉止损"))
        self.spbLoseThreshold.setSuffix(_translate("SelectedPerformance", "元"))
        self.cbxWinThreshold.setText(_translate("SelectedPerformance", "获利止盈"))
        self.spbWinThreshold.setSuffix(_translate("SelectedPerformance", "元"))
        self.cbxAddWhenDown.setText(_translate("SelectedPerformance", "下跌补仓"))
        self.spbAddThresholdDown.setSuffix(_translate("SelectedPerformance", "%"))
        self.cbxAddWhenUp.setText(_translate("SelectedPerformance", "上涨追进"))
        self.spbAddThresholdUp.setSuffix(_translate("SelectedPerformance", "%"))
        self.lblAddDeadline.setText(_translate("SelectedPerformance", "加仓期限"))
        self.spbAddDeadline.setSuffix(_translate("SelectedPerformance", "天内"))
        self.lblMaxHoldTime.setText(_translate("SelectedPerformance", "最长持仓时间"))
        self.spbMaxHoldTime.setSuffix(_translate("SelectedPerformance", "天"))
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
        item.setText(_translate("SelectedPerformance", "次日收盘"))
        item = self.tblStockList.horizontalHeaderItem(6)
        item.setText(_translate("SelectedPerformance", "加仓期限表现"))
        item = self.tblStockList.horizontalHeaderItem(7)
        item.setText(_translate("SelectedPerformance", "清仓期限表现"))
        item = self.tblStockList.horizontalHeaderItem(8)
        item.setText(_translate("SelectedPerformance", "期间最高涨幅"))
        item = self.tblStockList.horizontalHeaderItem(9)
        item.setText(_translate("SelectedPerformance", "期间最大回撤"))
        item = self.tblStockList.horizontalHeaderItem(10)
        item.setText(_translate("SelectedPerformance", "最佳操作策略"))
        item = self.tblStockList.horizontalHeaderItem(11)
        item.setText(_translate("SelectedPerformance", "实际操作记录"))
        self.lblTradeSummary.setText(_translate("SelectedPerformance", "共买入0只股票，盈利0只，成本0元，获利0元，收益率0%"))
        self.actHoldersStatus.setText(_translate("SelectedPerformance", "十大流通股东"))
        self.actAutoTest.setText(_translate("SelectedPerformance", "导入多个股票列表"))
