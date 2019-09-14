# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'StockFinder.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_StockFinder(object):
    def setupUi(self, StockFinder):
        StockFinder.setObjectName("StockFinder")
        StockFinder.resize(545, 374)
        self.centralwidget = QtWidgets.QWidget(StockFinder)
        self.centralwidget.setObjectName("centralwidget")
        self.grpSearchRange = QtWidgets.QGroupBox(self.centralwidget)
        self.grpSearchRange.setGeometry(QtCore.QRect(370, 10, 151, 151))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.grpSearchRange.setFont(font)
        self.grpSearchRange.setObjectName("grpSearchRange")
        self.layoutWidget = QtWidgets.QWidget(self.grpSearchRange)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 135, 126))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.layoutWidget.setFont(font)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.cbxShanghaiMain = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.cbxShanghaiMain.setFont(font)
        self.cbxShanghaiMain.setChecked(True)
        self.cbxShanghaiMain.setObjectName("cbxShanghaiMain")
        self.verticalLayout_2.addWidget(self.cbxShanghaiMain)
        self.cbxShenZhenMain = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.cbxShenZhenMain.setFont(font)
        self.cbxShenZhenMain.setChecked(True)
        self.cbxShenZhenMain.setObjectName("cbxShenZhenMain")
        self.verticalLayout_2.addWidget(self.cbxShenZhenMain)
        self.cbxShenZhenSmall = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.cbxShenZhenSmall.setFont(font)
        self.cbxShenZhenSmall.setChecked(True)
        self.cbxShenZhenSmall.setObjectName("cbxShenZhenSmall")
        self.verticalLayout_2.addWidget(self.cbxShenZhenSmall)
        self.cbxShenZhenNew = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.cbxShenZhenNew.setFont(font)
        self.cbxShenZhenNew.setChecked(True)
        self.cbxShenZhenNew.setObjectName("cbxShenZhenNew")
        self.verticalLayout_2.addWidget(self.cbxShenZhenNew)
        self.cbxShanghaiScience = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.cbxShanghaiScience.setFont(font)
        self.cbxShanghaiScience.setChecked(True)
        self.cbxShanghaiScience.setObjectName("cbxShanghaiScience")
        self.verticalLayout_2.addWidget(self.cbxShanghaiScience)
        self.grpTechnicalIndex = QtWidgets.QGroupBox(self.centralwidget)
        self.grpTechnicalIndex.setEnabled(True)
        self.grpTechnicalIndex.setGeometry(QtCore.QRect(10, 10, 351, 141))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.grpTechnicalIndex.setFont(font)
        self.grpTechnicalIndex.setObjectName("grpTechnicalIndex")
        self.lstCriteriaItems = QtWidgets.QListWidget(self.grpTechnicalIndex)
        self.lstCriteriaItems.setGeometry(QtCore.QRect(10, 20, 331, 91))
        self.lstCriteriaItems.setObjectName("lstCriteriaItems")
        self.layoutWidget1 = QtWidgets.QWidget(self.grpTechnicalIndex)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 115, 331, 21))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnAddCriteria = QtWidgets.QPushButton(self.layoutWidget1)
        self.btnAddCriteria.setObjectName("btnAddCriteria")
        self.horizontalLayout.addWidget(self.btnAddCriteria)
        self.btnEditCriteria = QtWidgets.QPushButton(self.layoutWidget1)
        self.btnEditCriteria.setObjectName("btnEditCriteria")
        self.horizontalLayout.addWidget(self.btnEditCriteria)
        self.btnRemoveCriteria = QtWidgets.QPushButton(self.layoutWidget1)
        self.btnRemoveCriteria.setObjectName("btnRemoveCriteria")
        self.horizontalLayout.addWidget(self.btnRemoveCriteria)
        self.btnResetCriteria = QtWidgets.QPushButton(self.layoutWidget1)
        self.btnResetCriteria.setObjectName("btnResetCriteria")
        self.horizontalLayout.addWidget(self.btnResetCriteria)
        self.grpCompanyInfo = QtWidgets.QGroupBox(self.centralwidget)
        self.grpCompanyInfo.setGeometry(QtCore.QRect(10, 160, 351, 161))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.grpCompanyInfo.setFont(font)
        self.grpCompanyInfo.setObjectName("grpCompanyInfo")
        self.layoutWidget2 = QtWidgets.QWidget(self.grpCompanyInfo)
        self.layoutWidget2.setGeometry(QtCore.QRect(10, 20, 331, 136))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.layoutWidget2.setFont(font)
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.cbxPriceEarning = QtWidgets.QCheckBox(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.cbxPriceEarning.setFont(font)
        self.cbxPriceEarning.setChecked(True)
        self.cbxPriceEarning.setObjectName("cbxPriceEarning")
        self.horizontalLayout_2.addWidget(self.cbxPriceEarning)
        self.spbPriceEarningMin = QtWidgets.QSpinBox(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.spbPriceEarningMin.setFont(font)
        self.spbPriceEarningMin.setMinimum(0)
        self.spbPriceEarningMin.setMaximum(100)
        self.spbPriceEarningMin.setProperty("value", 10)
        self.spbPriceEarningMin.setObjectName("spbPriceEarningMin")
        self.horizontalLayout_2.addWidget(self.spbPriceEarningMin)
        self.lblPriceEarningMax = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.lblPriceEarningMax.setFont(font)
        self.lblPriceEarningMax.setObjectName("lblPriceEarningMax")
        self.horizontalLayout_2.addWidget(self.lblPriceEarningMax)
        self.spbPriceEarningMax = QtWidgets.QSpinBox(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.spbPriceEarningMax.setFont(font)
        self.spbPriceEarningMax.setMinimum(5)
        self.spbPriceEarningMax.setMaximum(1000)
        self.spbPriceEarningMax.setProperty("value", 50)
        self.spbPriceEarningMax.setObjectName("spbPriceEarningMax")
        self.horizontalLayout_2.addWidget(self.spbPriceEarningMax)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.cbxPriceBook = QtWidgets.QCheckBox(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.cbxPriceBook.setFont(font)
        self.cbxPriceBook.setChecked(True)
        self.cbxPriceBook.setObjectName("cbxPriceBook")
        self.horizontalLayout_5.addWidget(self.cbxPriceBook)
        self.spbPriceBookMin = QtWidgets.QSpinBox(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.spbPriceBookMin.setFont(font)
        self.spbPriceBookMin.setMinimum(0)
        self.spbPriceBookMin.setMaximum(10)
        self.spbPriceBookMin.setProperty("value", 1)
        self.spbPriceBookMin.setObjectName("spbPriceBookMin")
        self.horizontalLayout_5.addWidget(self.spbPriceBookMin)
        self.lblPriceBookMax = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.lblPriceBookMax.setFont(font)
        self.lblPriceBookMax.setObjectName("lblPriceBookMax")
        self.horizontalLayout_5.addWidget(self.lblPriceBookMax)
        self.spbPriceBookMax = QtWidgets.QSpinBox(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.spbPriceBookMax.setFont(font)
        self.spbPriceBookMax.setMinimum(1)
        self.spbPriceBookMax.setMaximum(50)
        self.spbPriceBookMax.setProperty("value", 5)
        self.spbPriceBookMax.setObjectName("spbPriceBookMax")
        self.horizontalLayout_5.addWidget(self.spbPriceBookMax)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.cbxTotalShare = QtWidgets.QCheckBox(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.cbxTotalShare.setFont(font)
        self.cbxTotalShare.setChecked(True)
        self.cbxTotalShare.setObjectName("cbxTotalShare")
        self.horizontalLayout_7.addWidget(self.cbxTotalShare)
        self.spbTotalShareMin = QtWidgets.QSpinBox(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.spbTotalShareMin.setFont(font)
        self.spbTotalShareMin.setMinimum(0)
        self.spbTotalShareMin.setMaximum(10)
        self.spbTotalShareMin.setProperty("value", 1)
        self.spbTotalShareMin.setObjectName("spbTotalShareMin")
        self.horizontalLayout_7.addWidget(self.spbTotalShareMin)
        self.lblTotalShareMax = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.lblTotalShareMax.setFont(font)
        self.lblTotalShareMax.setObjectName("lblTotalShareMax")
        self.horizontalLayout_7.addWidget(self.lblTotalShareMax)
        self.spbTotalShareMax = QtWidgets.QSpinBox(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.spbTotalShareMax.setFont(font)
        self.spbTotalShareMax.setMinimum(1)
        self.spbTotalShareMax.setMaximum(10000)
        self.spbTotalShareMax.setProperty("value", 10)
        self.spbTotalShareMax.setObjectName("spbTotalShareMax")
        self.horizontalLayout_7.addWidget(self.spbTotalShareMax)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.cbxTotalAsset = QtWidgets.QCheckBox(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.cbxTotalAsset.setFont(font)
        self.cbxTotalAsset.setChecked(True)
        self.cbxTotalAsset.setObjectName("cbxTotalAsset")
        self.horizontalLayout_6.addWidget(self.cbxTotalAsset)
        self.spbTotalAssetsMin = QtWidgets.QSpinBox(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.spbTotalAssetsMin.setFont(font)
        self.spbTotalAssetsMin.setMinimum(1)
        self.spbTotalAssetsMin.setMaximum(1000)
        self.spbTotalAssetsMin.setProperty("value", 10)
        self.spbTotalAssetsMin.setObjectName("spbTotalAssetsMin")
        self.horizontalLayout_6.addWidget(self.spbTotalAssetsMin)
        self.lblTotalAssetsMax = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.lblTotalAssetsMax.setFont(font)
        self.lblTotalAssetsMax.setObjectName("lblTotalAssetsMax")
        self.horizontalLayout_6.addWidget(self.lblTotalAssetsMax)
        self.spbTotalAssetsMax = QtWidgets.QSpinBox(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.spbTotalAssetsMax.setFont(font)
        self.spbTotalAssetsMax.setMinimum(10)
        self.spbTotalAssetsMax.setMaximum(99999)
        self.spbTotalAssetsMax.setProperty("value", 100)
        self.spbTotalAssetsMax.setObjectName("spbTotalAssetsMax")
        self.horizontalLayout_6.addWidget(self.spbTotalAssetsMax)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.cbxIncludeStStock = QtWidgets.QCheckBox(self.layoutWidget2)
        self.cbxIncludeStStock.setObjectName("cbxIncludeStStock")
        self.horizontalLayout_3.addWidget(self.cbxIncludeStStock)
        self.cbxIncludeNewStock = QtWidgets.QCheckBox(self.layoutWidget2)
        self.cbxIncludeNewStock.setChecked(True)
        self.cbxIncludeNewStock.setObjectName("cbxIncludeNewStock")
        self.horizontalLayout_3.addWidget(self.cbxIncludeNewStock)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.cbxTechnicalIndexEnabled = QtWidgets.QCheckBox(self.centralwidget)
        self.cbxTechnicalIndexEnabled.setGeometry(QtCore.QRect(73, 9, 21, 16))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.cbxTechnicalIndexEnabled.setFont(font)
        self.cbxTechnicalIndexEnabled.setText("")
        self.cbxTechnicalIndexEnabled.setChecked(True)
        self.cbxTechnicalIndexEnabled.setObjectName("cbxTechnicalIndexEnabled")
        self.cbxCompanyInfoEnabled = QtWidgets.QCheckBox(self.centralwidget)
        self.cbxCompanyInfoEnabled.setGeometry(QtCore.QRect(85, 159, 21, 16))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.cbxCompanyInfoEnabled.setFont(font)
        self.cbxCompanyInfoEnabled.setText("")
        self.cbxCompanyInfoEnabled.setChecked(True)
        self.cbxCompanyInfoEnabled.setObjectName("cbxCompanyInfoEnabled")
        self.layoutWidget3 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget3.setGeometry(QtCore.QRect(370, 200, 151, 116))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget3)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.btnGetAllStockData = QtWidgets.QPushButton(self.layoutWidget3)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.btnGetAllStockData.setFont(font)
        self.btnGetAllStockData.setObjectName("btnGetAllStockData")
        self.verticalLayout.addWidget(self.btnGetAllStockData)
        self.btnStartSearch = QtWidgets.QPushButton(self.layoutWidget3)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.btnStartSearch.setFont(font)
        self.btnStartSearch.setObjectName("btnStartSearch")
        self.verticalLayout.addWidget(self.btnStartSearch)
        self.btnSaveConfig = QtWidgets.QPushButton(self.layoutWidget3)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.btnSaveConfig.setFont(font)
        self.btnSaveConfig.setObjectName("btnSaveConfig")
        self.verticalLayout.addWidget(self.btnSaveConfig)
        self.btnLoadConfig = QtWidgets.QPushButton(self.layoutWidget3)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.btnLoadConfig.setFont(font)
        self.btnLoadConfig.setObjectName("btnLoadConfig")
        self.verticalLayout.addWidget(self.btnLoadConfig)
        self.lblGetStockReminder = QtWidgets.QLabel(self.centralwidget)
        self.lblGetStockReminder.setGeometry(QtCore.QRect(370, 171, 151, 16))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.lblGetStockReminder.setFont(font)
        self.lblGetStockReminder.setObjectName("lblGetStockReminder")
        StockFinder.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(StockFinder)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 545, 22))
        self.menubar.setObjectName("menubar")
        StockFinder.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(StockFinder)
        self.statusbar.setObjectName("statusbar")
        StockFinder.setStatusBar(self.statusbar)

        self.retranslateUi(StockFinder)
        self.btnStartSearch.clicked.connect(StockFinder.search_all_stocks)
        self.btnGetAllStockData.clicked.connect(StockFinder.export_all_stock_data)
        self.cbxTechnicalIndexEnabled.clicked['bool'].connect(self.grpTechnicalIndex.setEnabled)
        self.cbxPriceEarning.clicked['bool'].connect(self.spbPriceEarningMin.setEnabled)
        self.cbxPriceEarning.clicked['bool'].connect(self.spbPriceEarningMax.setEnabled)
        self.cbxPriceBook.clicked['bool'].connect(self.spbPriceBookMin.setEnabled)
        self.cbxPriceBook.clicked['bool'].connect(self.spbPriceBookMax.setEnabled)
        self.cbxTotalShare.clicked['bool'].connect(self.spbTotalShareMin.setEnabled)
        self.cbxTotalShare.clicked['bool'].connect(self.spbTotalShareMax.setEnabled)
        self.cbxTotalAsset.clicked['bool'].connect(self.spbTotalAssetsMin.setEnabled)
        self.cbxTotalAsset.clicked['bool'].connect(self.spbTotalAssetsMax.setEnabled)
        self.cbxCompanyInfoEnabled.clicked['bool'].connect(self.grpCompanyInfo.setEnabled)
        self.btnAddCriteria.clicked.connect(StockFinder.add_criteria_item)
        self.btnEditCriteria.clicked.connect(StockFinder.modify_criteria_item)
        self.btnRemoveCriteria.clicked.connect(StockFinder.remove_criteria_item)
        self.btnResetCriteria.clicked.connect(StockFinder.reset_criteria_items)
        self.btnSaveConfig.clicked.connect(StockFinder.export_search_config)
        self.btnLoadConfig.clicked.connect(StockFinder.import_search_config)
        QtCore.QMetaObject.connectSlotsByName(StockFinder)

    def retranslateUi(self, StockFinder):
        _translate = QtCore.QCoreApplication.translate
        StockFinder.setWindowTitle(_translate("StockFinder", "智能选股器"))
        self.grpSearchRange.setTitle(_translate("StockFinder", "搜索范围"))
        self.cbxShanghaiMain.setText(_translate("StockFinder", "上海主板（60****）"))
        self.cbxShenZhenMain.setText(_translate("StockFinder", "深圳主板（000***）"))
        self.cbxShenZhenSmall.setText(_translate("StockFinder", "中小板（002***）"))
        self.cbxShenZhenNew.setText(_translate("StockFinder", "创业板（300***）"))
        self.cbxShanghaiScience.setText(_translate("StockFinder", "科创板（688***）"))
        self.grpTechnicalIndex.setTitle(_translate("StockFinder", "技术指标"))
        self.btnAddCriteria.setText(_translate("StockFinder", "添加"))
        self.btnEditCriteria.setText(_translate("StockFinder", "编辑"))
        self.btnRemoveCriteria.setText(_translate("StockFinder", "删除"))
        self.btnResetCriteria.setText(_translate("StockFinder", "重置"))
        self.grpCompanyInfo.setTitle(_translate("StockFinder", "基本面指标"))
        self.cbxPriceEarning.setText(_translate("StockFinder", "市盈率最低"))
        self.spbPriceEarningMin.setSuffix(_translate("StockFinder", "倍"))
        self.lblPriceEarningMax.setText(_translate("StockFinder", "最高"))
        self.spbPriceEarningMax.setSuffix(_translate("StockFinder", "倍"))
        self.cbxPriceBook.setText(_translate("StockFinder", "市净率最低"))
        self.spbPriceBookMin.setSuffix(_translate("StockFinder", "倍"))
        self.lblPriceBookMax.setText(_translate("StockFinder", "最高"))
        self.spbPriceBookMax.setSuffix(_translate("StockFinder", "倍"))
        self.cbxTotalShare.setText(_translate("StockFinder", "总股本最小"))
        self.spbTotalShareMin.setSuffix(_translate("StockFinder", "亿"))
        self.lblTotalShareMax.setText(_translate("StockFinder", "最大"))
        self.spbTotalShareMax.setSuffix(_translate("StockFinder", "亿"))
        self.cbxTotalAsset.setText(_translate("StockFinder", "市值最小"))
        self.spbTotalAssetsMin.setSuffix(_translate("StockFinder", "亿"))
        self.lblTotalAssetsMax.setText(_translate("StockFinder", "最大"))
        self.spbTotalAssetsMax.setSuffix(_translate("StockFinder", "亿"))
        self.cbxIncludeStStock.setText(_translate("StockFinder", "包含ST股"))
        self.cbxIncludeNewStock.setText(_translate("StockFinder", "包含上市半年内次新股"))
        self.btnGetAllStockData.setText(_translate("StockFinder", "获取股票数据"))
        self.btnStartSearch.setText(_translate("StockFinder", "开始搜索选股"))
        self.btnSaveConfig.setText(_translate("StockFinder", "保存指标"))
        self.btnLoadConfig.setText(_translate("StockFinder", "载入指标"))
        self.lblGetStockReminder.setText(_translate("StockFinder", "每日请先获取最新股票数据！"))
