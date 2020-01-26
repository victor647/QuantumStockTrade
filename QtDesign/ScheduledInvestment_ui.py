# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ScheduledInvestment.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ScheduledInvestment(object):
    def setupUi(self, ScheduledInvestment):
        ScheduledInvestment.setObjectName("ScheduledInvestment")
        ScheduledInvestment.resize(575, 355)
        self.centralwidget = QtWidgets.QWidget(ScheduledInvestment)
        self.centralwidget.setObjectName("centralwidget")
        self.tblStockList = QtWidgets.QTableWidget(self.centralwidget)
        self.tblStockList.setGeometry(QtCore.QRect(10, 110, 551, 192))
        self.tblStockList.setObjectName("tblStockList")
        self.tblStockList.setColumnCount(6)
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
        self.lblTradeSummary = QtWidgets.QLabel(self.centralwidget)
        self.lblTradeSummary.setGeometry(QtCore.QRect(10, 303, 611, 25))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.lblTradeSummary.setFont(font)
        self.lblTradeSummary.setObjectName("lblTradeSummary")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 9, 551, 103))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lblInitialInvestment = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.lblInitialInvestment.setFont(font)
        self.lblInitialInvestment.setObjectName("lblInitialInvestment")
        self.horizontalLayout_2.addWidget(self.lblInitialInvestment)
        self.spbInitialInvestment = QtWidgets.QSpinBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.spbInitialInvestment.setFont(font)
        self.spbInitialInvestment.setPrefix("")
        self.spbInitialInvestment.setMinimum(1)
        self.spbInitialInvestment.setMaximum(1000)
        self.spbInitialInvestment.setProperty("value", 20)
        self.spbInitialInvestment.setObjectName("spbInitialInvestment")
        self.horizontalLayout_2.addWidget(self.spbInitialInvestment)
        self.lblInterval = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.lblInterval.setFont(font)
        self.lblInterval.setObjectName("lblInterval")
        self.horizontalLayout_2.addWidget(self.lblInterval)
        self.spbInterval = QtWidgets.QSpinBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.spbInterval.setFont(font)
        self.spbInterval.setPrefix("")
        self.spbInterval.setMinimum(1)
        self.spbInterval.setMaximum(10)
        self.spbInterval.setObjectName("spbInterval")
        self.horizontalLayout_2.addWidget(self.spbInterval)
        self.cbbIntervalType = QtWidgets.QComboBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.cbbIntervalType.setFont(font)
        self.cbbIntervalType.setObjectName("cbbIntervalType")
        self.horizontalLayout_2.addWidget(self.cbbIntervalType)
        self.lblEachInvestment = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.lblEachInvestment.setFont(font)
        self.lblEachInvestment.setObjectName("lblEachInvestment")
        self.horizontalLayout_2.addWidget(self.lblEachInvestment)
        self.spbEachInvestment = QtWidgets.QSpinBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.spbEachInvestment.setFont(font)
        self.spbEachInvestment.setPrefix("")
        self.spbEachInvestment.setMinimum(1)
        self.spbEachInvestment.setMaximum(1000)
        self.spbEachInvestment.setProperty("value", 5)
        self.spbEachInvestment.setObjectName("spbEachInvestment")
        self.horizontalLayout_2.addWidget(self.spbEachInvestment)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lblStartDate = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.lblStartDate.setFont(font)
        self.lblStartDate.setObjectName("lblStartDate")
        self.horizontalLayout_3.addWidget(self.lblStartDate)
        self.dteStartDate = QtWidgets.QDateEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.dteStartDate.setFont(font)
        self.dteStartDate.setObjectName("dteStartDate")
        self.horizontalLayout_3.addWidget(self.dteStartDate)
        self.btnExportPlan = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.btnExportPlan.setFont(font)
        self.btnExportPlan.setObjectName("btnExportPlan")
        self.horizontalLayout_3.addWidget(self.btnExportPlan)
        self.btnImportPlan = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.btnImportPlan.setFont(font)
        self.btnImportPlan.setObjectName("btnImportPlan")
        self.horizontalLayout_3.addWidget(self.btnImportPlan)
        self.btnExportStockList = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.btnExportStockList.setFont(font)
        self.btnExportStockList.setObjectName("btnExportStockList")
        self.horizontalLayout_3.addWidget(self.btnExportStockList)
        self.btnImportStockList = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.btnImportStockList.setFont(font)
        self.btnImportStockList.setObjectName("btnImportStockList")
        self.horizontalLayout_3.addWidget(self.btnImportStockList)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblNewStockCode = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.lblNewStockCode.setFont(font)
        self.lblNewStockCode.setObjectName("lblNewStockCode")
        self.horizontalLayout.addWidget(self.lblNewStockCode)
        self.iptStockCode = QtWidgets.QLineEdit(self.layoutWidget)
        self.iptStockCode.setMaximumSize(QtCore.QSize(70, 16777215))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.iptStockCode.setFont(font)
        self.iptStockCode.setMaxLength(6)
        self.iptStockCode.setObjectName("iptStockCode")
        self.horizontalLayout.addWidget(self.iptStockCode)
        self.btnAddStock = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.btnAddStock.setFont(font)
        self.btnAddStock.setObjectName("btnAddStock")
        self.horizontalLayout.addWidget(self.btnAddStock)
        self.btnRemoveStock = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.btnRemoveStock.setFont(font)
        self.btnRemoveStock.setObjectName("btnRemoveStock")
        self.horizontalLayout.addWidget(self.btnRemoveStock)
        self.btnClearStocks = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.btnClearStocks.setFont(font)
        self.btnClearStocks.setObjectName("btnClearStocks")
        self.horizontalLayout.addWidget(self.btnClearStocks)
        self.btnStartInvesting = QtWidgets.QPushButton(self.layoutWidget)
        self.btnStartInvesting.setMinimumSize(QtCore.QSize(120, 0))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btnStartInvesting.setFont(font)
        self.btnStartInvesting.setObjectName("btnStartInvesting")
        self.horizontalLayout.addWidget(self.btnStartInvesting)
        self.verticalLayout.addLayout(self.horizontalLayout)
        ScheduledInvestment.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ScheduledInvestment)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 575, 22))
        self.menubar.setObjectName("menubar")
        ScheduledInvestment.setMenuBar(self.menubar)

        self.retranslateUi(ScheduledInvestment)
        self.btnExportPlan.clicked.connect(ScheduledInvestment.export_investment_plan)
        self.btnImportPlan.clicked.connect(ScheduledInvestment.import_investment_plan)
        self.btnExportStockList.clicked.connect(ScheduledInvestment.export_stock_list)
        self.btnImportStockList.clicked.connect(ScheduledInvestment.import_stock_list)
        self.btnAddStock.clicked.connect(ScheduledInvestment.add_stock_code)
        self.btnRemoveStock.clicked.connect(ScheduledInvestment.remove_stock_code)
        self.btnClearStocks.clicked.connect(ScheduledInvestment.clear_stock_list)
        self.btnStartInvesting.clicked.connect(ScheduledInvestment.start_investing)
        QtCore.QMetaObject.connectSlotsByName(ScheduledInvestment)

    def retranslateUi(self, ScheduledInvestment):
        _translate = QtCore.QCoreApplication.translate
        ScheduledInvestment.setWindowTitle(_translate("ScheduledInvestment", "定投组合表现"))
        self.tblStockList.setSortingEnabled(True)
        item = self.tblStockList.horizontalHeaderItem(0)
        item.setText(_translate("ScheduledInvestment", "股票代码"))
        item = self.tblStockList.horizontalHeaderItem(1)
        item.setText(_translate("ScheduledInvestment", "股票名称"))
        item = self.tblStockList.horizontalHeaderItem(2)
        item.setText(_translate("ScheduledInvestment", "持股仓位"))
        item = self.tblStockList.horizontalHeaderItem(3)
        item.setText(_translate("ScheduledInvestment", "年化复利"))
        item = self.tblStockList.horizontalHeaderItem(4)
        item.setText(_translate("ScheduledInvestment", "投入成本"))
        item = self.tblStockList.horizontalHeaderItem(5)
        item.setText(_translate("ScheduledInvestment", "持仓盈亏"))
        self.lblTradeSummary.setText(_translate("ScheduledInvestment", "共计成本0元，至今获利0元，收益率0%"))
        self.lblInitialInvestment.setText(_translate("ScheduledInvestment", "初始金额"))
        self.spbInitialInvestment.setSuffix(_translate("ScheduledInvestment", "万元"))
        self.lblInterval.setText(_translate("ScheduledInvestment", "定投间隔"))
        self.lblEachInvestment.setText(_translate("ScheduledInvestment", "每期金额"))
        self.spbEachInvestment.setSuffix(_translate("ScheduledInvestment", "万元"))
        self.lblStartDate.setText(_translate("ScheduledInvestment", "开始日期"))
        self.dteStartDate.setDisplayFormat(_translate("ScheduledInvestment", "yyyy-MM-dd"))
        self.btnExportPlan.setText(_translate("ScheduledInvestment", "导出策略"))
        self.btnImportPlan.setText(_translate("ScheduledInvestment", "导入策略"))
        self.btnExportStockList.setText(_translate("ScheduledInvestment", "导出列表"))
        self.btnImportStockList.setText(_translate("ScheduledInvestment", "导入列表"))
        self.lblNewStockCode.setText(_translate("ScheduledInvestment", "股票代码/名称"))
        self.iptStockCode.setText(_translate("ScheduledInvestment", "贵州茅台"))
        self.btnAddStock.setText(_translate("ScheduledInvestment", "添加股票"))
        self.btnRemoveStock.setText(_translate("ScheduledInvestment", "删除股票"))
        self.btnClearStocks.setText(_translate("ScheduledInvestment", "清空列表"))
        self.btnStartInvesting.setText(_translate("ScheduledInvestment", "开始定投"))
