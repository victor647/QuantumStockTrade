# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LiveTracker.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LiveTracker(object):
    def setupUi(self, LiveTracker):
        LiveTracker.setObjectName("LiveTracker")
        LiveTracker.resize(377, 529)
        self.centralwidget = QtWidgets.QWidget(LiveTracker)
        self.centralwidget.setObjectName("centralwidget")
        self.tblStockList = QtWidgets.QTableWidget(self.centralwidget)
        self.tblStockList.setGeometry(QtCore.QRect(10, 80, 351, 192))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.tblStockList.setFont(font)
        self.tblStockList.setObjectName("tblStockList")
        self.tblStockList.setColumnCount(3)
        self.tblStockList.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tblStockList.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblStockList.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblStockList.setHorizontalHeaderItem(2, item)
        self.tblStockList.horizontalHeader().setDefaultSectionSize(70)
        self.grpEventSignal = QtWidgets.QGroupBox(self.centralwidget)
        self.grpEventSignal.setGeometry(QtCore.QRect(10, 320, 351, 151))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.grpEventSignal.setFont(font)
        self.grpEventSignal.setObjectName("grpEventSignal")
        self.layoutWidget = QtWidgets.QWidget(self.grpEventSignal)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 334, 120))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.layoutWidget.setFont(font)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.cbxDailyUpPercent = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.cbxDailyUpPercent.setFont(font)
        self.cbxDailyUpPercent.setChecked(True)
        self.cbxDailyUpPercent.setObjectName("cbxDailyUpPercent")
        self.horizontalLayout_3.addWidget(self.cbxDailyUpPercent)
        self.spbDailyUpPercent = QtWidgets.QSpinBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.spbDailyUpPercent.setFont(font)
        self.spbDailyUpPercent.setMaximum(10)
        self.spbDailyUpPercent.setProperty("value", 5)
        self.spbDailyUpPercent.setObjectName("spbDailyUpPercent")
        self.horizontalLayout_3.addWidget(self.spbDailyUpPercent)
        self.cbxDailyDownPercent = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.cbxDailyDownPercent.setFont(font)
        self.cbxDailyDownPercent.setChecked(True)
        self.cbxDailyDownPercent.setObjectName("cbxDailyDownPercent")
        self.horizontalLayout_3.addWidget(self.cbxDailyDownPercent)
        self.spbDailyDownPercent = QtWidgets.QSpinBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.spbDailyDownPercent.setFont(font)
        self.spbDailyDownPercent.setMaximum(10)
        self.spbDailyDownPercent.setProperty("value", 5)
        self.spbDailyDownPercent.setObjectName("spbDailyDownPercent")
        self.horizontalLayout_3.addWidget(self.spbDailyDownPercent)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.cbxFiveMinUpPercent = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.cbxFiveMinUpPercent.setFont(font)
        self.cbxFiveMinUpPercent.setChecked(True)
        self.cbxFiveMinUpPercent.setObjectName("cbxFiveMinUpPercent")
        self.horizontalLayout_4.addWidget(self.cbxFiveMinUpPercent)
        self.spbFiveMinUpPercent = QtWidgets.QSpinBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.spbFiveMinUpPercent.setFont(font)
        self.spbFiveMinUpPercent.setMaximum(10)
        self.spbFiveMinUpPercent.setProperty("value", 1)
        self.spbFiveMinUpPercent.setObjectName("spbFiveMinUpPercent")
        self.horizontalLayout_4.addWidget(self.spbFiveMinUpPercent)
        self.cbxFiveMinDownPercent = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.cbxFiveMinDownPercent.setFont(font)
        self.cbxFiveMinDownPercent.setChecked(True)
        self.cbxFiveMinDownPercent.setObjectName("cbxFiveMinDownPercent")
        self.horizontalLayout_4.addWidget(self.cbxFiveMinDownPercent)
        self.spbFiveMinDownPercent = QtWidgets.QSpinBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.spbFiveMinDownPercent.setFont(font)
        self.spbFiveMinDownPercent.setMaximum(10)
        self.spbFiveMinDownPercent.setProperty("value", 1)
        self.spbFiveMinDownPercent.setObjectName("spbFiveMinDownPercent")
        self.horizontalLayout_4.addWidget(self.spbFiveMinDownPercent)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.cbxSingleBuyAmount = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.cbxSingleBuyAmount.setFont(font)
        self.cbxSingleBuyAmount.setChecked(True)
        self.cbxSingleBuyAmount.setObjectName("cbxSingleBuyAmount")
        self.horizontalLayout_5.addWidget(self.cbxSingleBuyAmount)
        self.spbSingleBuyAmount = QtWidgets.QSpinBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.spbSingleBuyAmount.setFont(font)
        self.spbSingleBuyAmount.setMinimum(10)
        self.spbSingleBuyAmount.setMaximum(10000)
        self.spbSingleBuyAmount.setProperty("value", 100)
        self.spbSingleBuyAmount.setObjectName("spbSingleBuyAmount")
        self.horizontalLayout_5.addWidget(self.spbSingleBuyAmount)
        self.cbxSingleSellAmount = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.cbxSingleSellAmount.setFont(font)
        self.cbxSingleSellAmount.setChecked(True)
        self.cbxSingleSellAmount.setObjectName("cbxSingleSellAmount")
        self.horizontalLayout_5.addWidget(self.cbxSingleSellAmount)
        self.spbSingleSellAmount = QtWidgets.QSpinBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.spbSingleSellAmount.setFont(font)
        self.spbSingleSellAmount.setMinimum(10)
        self.spbSingleSellAmount.setMaximum(10000)
        self.spbSingleSellAmount.setProperty("value", 100)
        self.spbSingleSellAmount.setObjectName("spbSingleSellAmount")
        self.horizontalLayout_5.addWidget(self.spbSingleSellAmount)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.cbxActiveBuy = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.cbxActiveBuy.setFont(font)
        self.cbxActiveBuy.setChecked(True)
        self.cbxActiveBuy.setObjectName("cbxActiveBuy")
        self.horizontalLayout_6.addWidget(self.cbxActiveBuy)
        self.spbActiveBuyPercent = QtWidgets.QSpinBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.spbActiveBuyPercent.setFont(font)
        self.spbActiveBuyPercent.setMinimum(50)
        self.spbActiveBuyPercent.setMaximum(100)
        self.spbActiveBuyPercent.setProperty("value", 80)
        self.spbActiveBuyPercent.setObjectName("spbActiveBuyPercent")
        self.horizontalLayout_6.addWidget(self.spbActiveBuyPercent)
        self.cbxActiveSell = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.cbxActiveSell.setFont(font)
        self.cbxActiveSell.setChecked(True)
        self.cbxActiveSell.setObjectName("cbxActiveSell")
        self.horizontalLayout_6.addWidget(self.cbxActiveSell)
        self.spbActiveSellPercent = QtWidgets.QSpinBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.spbActiveSellPercent.setFont(font)
        self.spbActiveSellPercent.setMinimum(50)
        self.spbActiveSellPercent.setMaximum(100)
        self.spbActiveSellPercent.setProperty("value", 80)
        self.spbActiveSellPercent.setObjectName("spbActiveSellPercent")
        self.horizontalLayout_6.addWidget(self.spbActiveSellPercent)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 10, 351, 60))
        self.widget.setObjectName("widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnImportStockList = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.btnImportStockList.setFont(font)
        self.btnImportStockList.setObjectName("btnImportStockList")
        self.horizontalLayout.addWidget(self.btnImportStockList)
        self.btnStartTracking = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.btnStartTracking.setFont(font)
        self.btnStartTracking.setObjectName("btnStartTracking")
        self.horizontalLayout.addWidget(self.btnStartTracking)
        self.btnStopTracking = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.btnStopTracking.setFont(font)
        self.btnStopTracking.setObjectName("btnStopTracking")
        self.horizontalLayout.addWidget(self.btnStopTracking)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lblLastUpdateTime = QtWidgets.QLabel(self.widget)
        self.lblLastUpdateTime.setMinimumSize(QtCore.QSize(150, 0))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        self.lblLastUpdateTime.setFont(font)
        self.lblLastUpdateTime.setObjectName("lblLastUpdateTime")
        self.horizontalLayout_2.addWidget(self.lblLastUpdateTime)
        self.lblUpdateFrequency = QtWidgets.QLabel(self.widget)
        self.lblUpdateFrequency.setMaximumSize(QtCore.QSize(60, 16777215))
        self.lblUpdateFrequency.setObjectName("lblUpdateFrequency")
        self.horizontalLayout_2.addWidget(self.lblUpdateFrequency)
        self.spbUpdateFrequency = QtWidgets.QSpinBox(self.widget)
        self.spbUpdateFrequency.setMaximumSize(QtCore.QSize(60, 16777215))
        self.spbUpdateFrequency.setMinimum(1)
        self.spbUpdateFrequency.setMaximum(10)
        self.spbUpdateFrequency.setProperty("value", 3)
        self.spbUpdateFrequency.setObjectName("spbUpdateFrequency")
        self.horizontalLayout_2.addWidget(self.spbUpdateFrequency)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(10, 280, 351, 27))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.iptStockCode = QtWidgets.QLineEdit(self.widget1)
        self.iptStockCode.setMaxLength(6)
        self.iptStockCode.setObjectName("iptStockCode")
        self.horizontalLayout_7.addWidget(self.iptStockCode)
        self.btnAddStock = QtWidgets.QPushButton(self.widget1)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.btnAddStock.setFont(font)
        self.btnAddStock.setObjectName("btnAddStock")
        self.horizontalLayout_7.addWidget(self.btnAddStock)
        self.btnRemoveStock = QtWidgets.QPushButton(self.widget1)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.btnRemoveStock.setFont(font)
        self.btnRemoveStock.setObjectName("btnRemoveStock")
        self.horizontalLayout_7.addWidget(self.btnRemoveStock)
        self.btnClearStocks = QtWidgets.QPushButton(self.widget1)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.btnClearStocks.setFont(font)
        self.btnClearStocks.setObjectName("btnClearStocks")
        self.horizontalLayout_7.addWidget(self.btnClearStocks)
        LiveTracker.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(LiveTracker)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 377, 23))
        self.menubar.setObjectName("menubar")
        LiveTracker.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(LiveTracker)
        self.statusbar.setObjectName("statusbar")
        LiveTracker.setStatusBar(self.statusbar)

        self.retranslateUi(LiveTracker)
        self.btnImportStockList.clicked.connect(LiveTracker.import_stock_list)
        self.btnStartTracking.clicked.connect(LiveTracker.start_monitoring)
        self.btnStopTracking.clicked.connect(LiveTracker.stop_monitoring)
        self.btnAddStock.clicked.connect(LiveTracker.add_stock_code)
        self.btnRemoveStock.clicked.connect(LiveTracker.remove_stock_code)
        self.btnClearStocks.clicked.connect(LiveTracker.clear_stock_list)
        self.cbxDailyUpPercent.clicked['bool'].connect(self.spbDailyUpPercent.setEnabled)
        self.cbxDailyDownPercent.clicked['bool'].connect(self.spbDailyDownPercent.setEnabled)
        self.cbxFiveMinUpPercent.clicked['bool'].connect(self.spbFiveMinUpPercent.setEnabled)
        self.cbxFiveMinDownPercent.clicked['bool'].connect(self.spbFiveMinDownPercent.setEnabled)
        self.cbxSingleBuyAmount.clicked['bool'].connect(self.spbSingleBuyAmount.setEnabled)
        self.cbxSingleSellAmount.clicked['bool'].connect(self.spbSingleSellAmount.setEnabled)
        self.cbxActiveBuy.clicked['bool'].connect(self.spbActiveBuyPercent.setEnabled)
        self.cbxActiveSell.clicked['bool'].connect(self.spbActiveSellPercent.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(LiveTracker)

    def retranslateUi(self, LiveTracker):
        _translate = QtCore.QCoreApplication.translate
        LiveTracker.setWindowTitle(_translate("LiveTracker", "实时盯盘助手"))
        item = self.tblStockList.horizontalHeaderItem(0)
        item.setText(_translate("LiveTracker", "股票代码"))
        item = self.tblStockList.horizontalHeaderItem(1)
        item.setText(_translate("LiveTracker", "股票名称"))
        item = self.tblStockList.horizontalHeaderItem(2)
        item.setText(_translate("LiveTracker", "当前价格"))
        self.grpEventSignal.setTitle(_translate("LiveTracker", "盘中异动提示"))
        self.cbxDailyUpPercent.setText(_translate("LiveTracker", "日内涨幅达到"))
        self.spbDailyUpPercent.setSuffix(_translate("LiveTracker", "%"))
        self.cbxDailyDownPercent.setText(_translate("LiveTracker", "跌幅达到"))
        self.spbDailyDownPercent.setSuffix(_translate("LiveTracker", "%"))
        self.cbxFiveMinUpPercent.setText(_translate("LiveTracker", "5分钟涨幅达到"))
        self.spbFiveMinUpPercent.setSuffix(_translate("LiveTracker", "%"))
        self.cbxFiveMinDownPercent.setText(_translate("LiveTracker", "跌幅达到"))
        self.spbFiveMinDownPercent.setSuffix(_translate("LiveTracker", "%"))
        self.cbxSingleBuyAmount.setText(_translate("LiveTracker", "单笔买单"))
        self.spbSingleBuyAmount.setSuffix(_translate("LiveTracker", "万元"))
        self.cbxSingleSellAmount.setText(_translate("LiveTracker", "单笔卖单"))
        self.spbSingleSellAmount.setSuffix(_translate("LiveTracker", "万元"))
        self.cbxActiveBuy.setText(_translate("LiveTracker", "1分钟外盘大于"))
        self.spbActiveBuyPercent.setSuffix(_translate("LiveTracker", "%"))
        self.cbxActiveSell.setText(_translate("LiveTracker", "内盘大于"))
        self.spbActiveSellPercent.setSuffix(_translate("LiveTracker", "%"))
        self.btnImportStockList.setText(_translate("LiveTracker", "导入股票列表"))
        self.btnStartTracking.setText(_translate("LiveTracker", "开始盯盘"))
        self.btnStopTracking.setText(_translate("LiveTracker", "停止盯盘"))
        self.lblLastUpdateTime.setText(_translate("LiveTracker", "上次刷新："))
        self.lblUpdateFrequency.setText(_translate("LiveTracker", "刷新频率："))
        self.spbUpdateFrequency.setSuffix(_translate("LiveTracker", "秒"))
        self.iptStockCode.setText(_translate("LiveTracker", "600519"))
        self.btnAddStock.setText(_translate("LiveTracker", "添加股票"))
        self.btnRemoveStock.setText(_translate("LiveTracker", "删除股票"))
        self.btnClearStocks.setText(_translate("LiveTracker", "清空列表"))
