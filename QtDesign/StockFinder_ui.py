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
        StockFinder.resize(533, 540)
        self.centralwidget = QtWidgets.QWidget(StockFinder)
        self.centralwidget.setObjectName("centralwidget")
        self.grpSearchRange = QtWidgets.QGroupBox(self.centralwidget)
        self.grpSearchRange.setGeometry(QtCore.QRect(370, 80, 151, 161))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.grpSearchRange.setFont(font)
        self.grpSearchRange.setObjectName("grpSearchRange")
        self.layoutWidget = QtWidgets.QWidget(self.grpSearchRange)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 135, 131))
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
        self.cbxShanghaiScience.setChecked(False)
        self.cbxShanghaiScience.setObjectName("cbxShanghaiScience")
        self.verticalLayout_2.addWidget(self.cbxShanghaiScience)
        self.grpTechnicalIndex = QtWidgets.QGroupBox(self.centralwidget)
        self.grpTechnicalIndex.setEnabled(True)
        self.grpTechnicalIndex.setGeometry(QtCore.QRect(10, 10, 351, 161))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.grpTechnicalIndex.setFont(font)
        self.grpTechnicalIndex.setObjectName("grpTechnicalIndex")
        self.lstCriteriaItems = QtWidgets.QListWidget(self.grpTechnicalIndex)
        self.lstCriteriaItems.setGeometry(QtCore.QRect(10, 20, 331, 131))
        self.lstCriteriaItems.setObjectName("lstCriteriaItems")
        self.grpCompanyInfo = QtWidgets.QGroupBox(self.centralwidget)
        self.grpCompanyInfo.setGeometry(QtCore.QRect(10, 180, 351, 301))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.grpCompanyInfo.setFont(font)
        self.grpCompanyInfo.setObjectName("grpCompanyInfo")
        self.layoutWidget1 = QtWidgets.QWidget(self.grpCompanyInfo)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 20, 331, 273))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.layoutWidget1.setFont(font)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.cbxPriceEarning = QtWidgets.QCheckBox(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.cbxPriceEarning.setFont(font)
        self.cbxPriceEarning.setChecked(True)
        self.cbxPriceEarning.setObjectName("cbxPriceEarning")
        self.horizontalLayout_2.addWidget(self.cbxPriceEarning)
        self.spbPriceEarningMin = QtWidgets.QSpinBox(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.spbPriceEarningMin.setFont(font)
        self.spbPriceEarningMin.setMinimum(0)
        self.spbPriceEarningMin.setMaximum(100)
        self.spbPriceEarningMin.setProperty("value", 10)
        self.spbPriceEarningMin.setObjectName("spbPriceEarningMin")
        self.horizontalLayout_2.addWidget(self.spbPriceEarningMin)
        self.lblPriceEarningMax = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.lblPriceEarningMax.setFont(font)
        self.lblPriceEarningMax.setObjectName("lblPriceEarningMax")
        self.horizontalLayout_2.addWidget(self.lblPriceEarningMax)
        self.spbPriceEarningMax = QtWidgets.QSpinBox(self.layoutWidget1)
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
        self.cbxPriceBook = QtWidgets.QCheckBox(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.cbxPriceBook.setFont(font)
        self.cbxPriceBook.setChecked(True)
        self.cbxPriceBook.setObjectName("cbxPriceBook")
        self.horizontalLayout_5.addWidget(self.cbxPriceBook)
        self.spbPriceBookMin = QtWidgets.QDoubleSpinBox(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        self.spbPriceBookMin.setFont(font)
        self.spbPriceBookMin.setDecimals(1)
        self.spbPriceBookMin.setMinimum(0.0)
        self.spbPriceBookMin.setMaximum(10.0)
        self.spbPriceBookMin.setSingleStep(0.5)
        self.spbPriceBookMin.setProperty("value", 1.0)
        self.spbPriceBookMin.setObjectName("spbPriceBookMin")
        self.horizontalLayout_5.addWidget(self.spbPriceBookMin)
        self.lblPriceBookMax = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.lblPriceBookMax.setFont(font)
        self.lblPriceBookMax.setObjectName("lblPriceBookMax")
        self.horizontalLayout_5.addWidget(self.lblPriceBookMax)
        self.spbPriceBookMax = QtWidgets.QDoubleSpinBox(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        self.spbPriceBookMax.setFont(font)
        self.spbPriceBookMax.setDecimals(1)
        self.spbPriceBookMax.setMinimum(1.0)
        self.spbPriceBookMax.setSingleStep(0.5)
        self.spbPriceBookMax.setProperty("value", 5.0)
        self.spbPriceBookMax.setObjectName("spbPriceBookMax")
        self.horizontalLayout_5.addWidget(self.spbPriceBookMax)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.cbxTotalShare = QtWidgets.QCheckBox(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.cbxTotalShare.setFont(font)
        self.cbxTotalShare.setChecked(True)
        self.cbxTotalShare.setObjectName("cbxTotalShare")
        self.horizontalLayout_7.addWidget(self.cbxTotalShare)
        self.spbTotalShareMin = QtWidgets.QSpinBox(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.spbTotalShareMin.setFont(font)
        self.spbTotalShareMin.setMinimum(0)
        self.spbTotalShareMin.setMaximum(10)
        self.spbTotalShareMin.setProperty("value", 1)
        self.spbTotalShareMin.setObjectName("spbTotalShareMin")
        self.horizontalLayout_7.addWidget(self.spbTotalShareMin)
        self.lblTotalShareMax = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.lblTotalShareMax.setFont(font)
        self.lblTotalShareMax.setObjectName("lblTotalShareMax")
        self.horizontalLayout_7.addWidget(self.lblTotalShareMax)
        self.spbTotalShareMax = QtWidgets.QSpinBox(self.layoutWidget1)
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
        self.cbxTotalAssets = QtWidgets.QCheckBox(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.cbxTotalAssets.setFont(font)
        self.cbxTotalAssets.setChecked(True)
        self.cbxTotalAssets.setObjectName("cbxTotalAssets")
        self.horizontalLayout_6.addWidget(self.cbxTotalAssets)
        self.spbTotalAssetsMin = QtWidgets.QSpinBox(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.spbTotalAssetsMin.setFont(font)
        self.spbTotalAssetsMin.setMinimum(1)
        self.spbTotalAssetsMin.setMaximum(1000)
        self.spbTotalAssetsMin.setProperty("value", 10)
        self.spbTotalAssetsMin.setObjectName("spbTotalAssetsMin")
        self.horizontalLayout_6.addWidget(self.spbTotalAssetsMin)
        self.lblTotalAssetsMax = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.lblTotalAssetsMax.setFont(font)
        self.lblTotalAssetsMax.setObjectName("lblTotalAssetsMax")
        self.horizontalLayout_6.addWidget(self.lblTotalAssetsMax)
        self.spbTotalAssetsMax = QtWidgets.QSpinBox(self.layoutWidget1)
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
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.cbxGrossProfit = QtWidgets.QCheckBox(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.cbxGrossProfit.setFont(font)
        self.cbxGrossProfit.setChecked(True)
        self.cbxGrossProfit.setObjectName("cbxGrossProfit")
        self.horizontalLayout_4.addWidget(self.cbxGrossProfit)
        self.spbGrossProfit = QtWidgets.QSpinBox(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.spbGrossProfit.setFont(font)
        self.spbGrossProfit.setMinimum(-20)
        self.spbGrossProfit.setMaximum(100)
        self.spbGrossProfit.setProperty("value", 30)
        self.spbGrossProfit.setObjectName("spbGrossProfit")
        self.horizontalLayout_4.addWidget(self.spbGrossProfit)
        self.cbxNetProfit = QtWidgets.QCheckBox(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.cbxNetProfit.setFont(font)
        self.cbxNetProfit.setChecked(True)
        self.cbxNetProfit.setObjectName("cbxNetProfit")
        self.horizontalLayout_4.addWidget(self.cbxNetProfit)
        self.spbNetProfit = QtWidgets.QSpinBox(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.spbNetProfit.setFont(font)
        self.spbNetProfit.setMinimum(-20)
        self.spbNetProfit.setMaximum(100)
        self.spbNetProfit.setProperty("value", 10)
        self.spbNetProfit.setObjectName("spbNetProfit")
        self.horizontalLayout_4.addWidget(self.spbNetProfit)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.cbxIncomeIncrease = QtWidgets.QCheckBox(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.cbxIncomeIncrease.setFont(font)
        self.cbxIncomeIncrease.setChecked(True)
        self.cbxIncomeIncrease.setObjectName("cbxIncomeIncrease")
        self.horizontalLayout_9.addWidget(self.cbxIncomeIncrease)
        self.spbIncomeIncrease = QtWidgets.QSpinBox(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.spbIncomeIncrease.setFont(font)
        self.spbIncomeIncrease.setMinimum(-20)
        self.spbIncomeIncrease.setMaximum(100)
        self.spbIncomeIncrease.setProperty("value", 10)
        self.spbIncomeIncrease.setObjectName("spbIncomeIncrease")
        self.horizontalLayout_9.addWidget(self.spbIncomeIncrease)
        self.cbxProfitIncrease = QtWidgets.QCheckBox(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.cbxProfitIncrease.setFont(font)
        self.cbxProfitIncrease.setChecked(True)
        self.cbxProfitIncrease.setObjectName("cbxProfitIncrease")
        self.horizontalLayout_9.addWidget(self.cbxProfitIncrease)
        self.spbProfitIncrease = QtWidgets.QSpinBox(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.spbProfitIncrease.setFont(font)
        self.spbProfitIncrease.setMinimum(-20)
        self.spbProfitIncrease.setMaximum(100)
        self.spbProfitIncrease.setProperty("value", 10)
        self.spbProfitIncrease.setObjectName("spbProfitIncrease")
        self.horizontalLayout_9.addWidget(self.spbProfitIncrease)
        self.verticalLayout_3.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.cbxNetAssetProfit = QtWidgets.QCheckBox(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.cbxNetAssetProfit.setFont(font)
        self.cbxNetAssetProfit.setChecked(True)
        self.cbxNetAssetProfit.setObjectName("cbxNetAssetProfit")
        self.horizontalLayout_8.addWidget(self.cbxNetAssetProfit)
        self.spbNetAssetProfit = QtWidgets.QSpinBox(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.spbNetAssetProfit.setFont(font)
        self.spbNetAssetProfit.setMinimum(0)
        self.spbNetAssetProfit.setMaximum(100)
        self.spbNetAssetProfit.setProperty("value", 5)
        self.spbNetAssetProfit.setObjectName("spbNetAssetProfit")
        self.horizontalLayout_8.addWidget(self.spbNetAssetProfit)
        self.verticalLayout_3.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.cbxTotalHolders = QtWidgets.QCheckBox(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.cbxTotalHolders.setFont(font)
        self.cbxTotalHolders.setChecked(True)
        self.cbxTotalHolders.setObjectName("cbxTotalHolders")
        self.horizontalLayout_10.addWidget(self.cbxTotalHolders)
        self.spbTotalHoldersMin = QtWidgets.QDoubleSpinBox(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        self.spbTotalHoldersMin.setFont(font)
        self.spbTotalHoldersMin.setDecimals(1)
        self.spbTotalHoldersMin.setMinimum(0.0)
        self.spbTotalHoldersMin.setMaximum(10.0)
        self.spbTotalHoldersMin.setSingleStep(0.5)
        self.spbTotalHoldersMin.setProperty("value", 1.0)
        self.spbTotalHoldersMin.setObjectName("spbTotalHoldersMin")
        self.horizontalLayout_10.addWidget(self.spbTotalHoldersMin)
        self.lblTotalHoldersMax = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.lblTotalHoldersMax.setFont(font)
        self.lblTotalHoldersMax.setObjectName("lblTotalHoldersMax")
        self.horizontalLayout_10.addWidget(self.lblTotalHoldersMax)
        self.spbTotalHoldersMax = QtWidgets.QDoubleSpinBox(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        self.spbTotalHoldersMax.setFont(font)
        self.spbTotalHoldersMax.setDecimals(1)
        self.spbTotalHoldersMax.setMinimum(1.0)
        self.spbTotalHoldersMax.setProperty("value", 10.0)
        self.spbTotalHoldersMax.setObjectName("spbTotalHoldersMax")
        self.horizontalLayout_10.addWidget(self.spbTotalHoldersMax)
        self.verticalLayout_3.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.cbxIncludeStStock = QtWidgets.QCheckBox(self.layoutWidget1)
        self.cbxIncludeStStock.setObjectName("cbxIncludeStStock")
        self.horizontalLayout_3.addWidget(self.cbxIncludeStStock)
        self.cbxIncludeNewStock = QtWidgets.QCheckBox(self.layoutWidget1)
        self.cbxIncludeNewStock.setChecked(True)
        self.cbxIncludeNewStock.setObjectName("cbxIncludeNewStock")
        self.horizontalLayout_3.addWidget(self.cbxIncludeNewStock)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.cbxTechnicalIndexEnabled = QtWidgets.QCheckBox(self.centralwidget)
        self.cbxTechnicalIndexEnabled.setGeometry(QtCore.QRect(97, 11, 21, 16))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.cbxTechnicalIndexEnabled.setFont(font)
        self.cbxTechnicalIndexEnabled.setText("")
        self.cbxTechnicalIndexEnabled.setChecked(True)
        self.cbxTechnicalIndexEnabled.setObjectName("cbxTechnicalIndexEnabled")
        self.cbxCompanyInfoEnabled = QtWidgets.QCheckBox(self.centralwidget)
        self.cbxCompanyInfoEnabled.setGeometry(QtCore.QRect(86, 181, 21, 16))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.cbxCompanyInfoEnabled.setFont(font)
        self.cbxCompanyInfoEnabled.setText("")
        self.cbxCompanyInfoEnabled.setChecked(True)
        self.cbxCompanyInfoEnabled.setObjectName("cbxCompanyInfoEnabled")
        self.layoutWidget2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget2.setGeometry(QtCore.QRect(370, 279, 151, 161))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.btnGetAllStockData = QtWidgets.QPushButton(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.btnGetAllStockData.setFont(font)
        self.btnGetAllStockData.setObjectName("btnGetAllStockData")
        self.verticalLayout.addWidget(self.btnGetAllStockData)
        self.btnSaveTechnicalConfig = QtWidgets.QPushButton(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.btnSaveTechnicalConfig.setFont(font)
        self.btnSaveTechnicalConfig.setObjectName("btnSaveTechnicalConfig")
        self.verticalLayout.addWidget(self.btnSaveTechnicalConfig)
        self.btnLoadTechnicalConfig = QtWidgets.QPushButton(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.btnLoadTechnicalConfig.setFont(font)
        self.btnLoadTechnicalConfig.setObjectName("btnLoadTechnicalConfig")
        self.verticalLayout.addWidget(self.btnLoadTechnicalConfig)
        self.btnSaveCompanyConfig = QtWidgets.QPushButton(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.btnSaveCompanyConfig.setFont(font)
        self.btnSaveCompanyConfig.setObjectName("btnSaveCompanyConfig")
        self.verticalLayout.addWidget(self.btnSaveCompanyConfig)
        self.btnLoadCompanyConfig = QtWidgets.QPushButton(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.btnLoadCompanyConfig.setFont(font)
        self.btnLoadCompanyConfig.setObjectName("btnLoadCompanyConfig")
        self.verticalLayout.addWidget(self.btnLoadCompanyConfig)
        self.lblGetStockReminder = QtWidgets.QLabel(self.centralwidget)
        self.lblGetStockReminder.setGeometry(QtCore.QRect(370, 250, 151, 16))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.lblGetStockReminder.setFont(font)
        self.lblGetStockReminder.setObjectName("lblGetStockReminder")
        self.btnStartSearch = QtWidgets.QPushButton(self.centralwidget)
        self.btnStartSearch.setGeometry(QtCore.QRect(370, 450, 149, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.btnStartSearch.setFont(font)
        self.btnStartSearch.setObjectName("btnStartSearch")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(370, 20, 151, 58))
        self.widget.setObjectName("widget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.btnAddCriteria = QtWidgets.QPushButton(self.widget)
        self.btnAddCriteria.setObjectName("btnAddCriteria")
        self.horizontalLayout_12.addWidget(self.btnAddCriteria)
        self.btnRemoveCriteria = QtWidgets.QPushButton(self.widget)
        self.btnRemoveCriteria.setObjectName("btnRemoveCriteria")
        self.horizontalLayout_12.addWidget(self.btnRemoveCriteria)
        self.verticalLayout_4.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.btnEditCriteria = QtWidgets.QPushButton(self.widget)
        self.btnEditCriteria.setObjectName("btnEditCriteria")
        self.horizontalLayout_11.addWidget(self.btnEditCriteria)
        self.btnResetCriteria = QtWidgets.QPushButton(self.widget)
        self.btnResetCriteria.setObjectName("btnResetCriteria")
        self.horizontalLayout_11.addWidget(self.btnResetCriteria)
        self.verticalLayout_4.addLayout(self.horizontalLayout_11)
        StockFinder.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(StockFinder)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 533, 23))
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
        self.cbxTotalShare.clicked['bool'].connect(self.spbTotalShareMin.setEnabled)
        self.cbxTotalShare.clicked['bool'].connect(self.spbTotalShareMax.setEnabled)
        self.cbxTotalAssets.clicked['bool'].connect(self.spbTotalAssetsMin.setEnabled)
        self.cbxTotalAssets.clicked['bool'].connect(self.spbTotalAssetsMax.setEnabled)
        self.cbxCompanyInfoEnabled.clicked['bool'].connect(self.grpCompanyInfo.setEnabled)
        self.btnAddCriteria.clicked.connect(StockFinder.add_criteria_item)
        self.btnEditCriteria.clicked.connect(StockFinder.modify_criteria_item)
        self.btnRemoveCriteria.clicked.connect(StockFinder.remove_criteria_item)
        self.btnResetCriteria.clicked.connect(StockFinder.reset_criteria_items)
        self.btnSaveTechnicalConfig.clicked.connect(StockFinder.export_technical_config)
        self.btnLoadTechnicalConfig.clicked.connect(StockFinder.import_technical_config)
        self.cbxGrossProfit.clicked['bool'].connect(self.spbGrossProfit.setEnabled)
        self.cbxNetProfit.clicked['bool'].connect(self.spbNetProfit.setEnabled)
        self.cbxIncomeIncrease.clicked['bool'].connect(self.spbIncomeIncrease.setEnabled)
        self.cbxProfitIncrease.clicked['bool'].connect(self.spbProfitIncrease.setEnabled)
        self.cbxNetAssetProfit.clicked['bool'].connect(self.spbNetAssetProfit.setEnabled)
        self.cbxTotalHolders.clicked['bool'].connect(self.spbTotalHoldersMin.setEnabled)
        self.cbxTotalHolders.clicked['bool'].connect(self.spbTotalHoldersMax.setEnabled)
        self.lstCriteriaItems.itemDoubleClicked['QListWidgetItem*'].connect(StockFinder.edit_selected_item)
        self.btnSaveCompanyConfig.clicked.connect(StockFinder.export_company_config)
        self.btnLoadCompanyConfig.clicked.connect(StockFinder.import_company_config)
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
        self.grpTechnicalIndex.setTitle(_translate("StockFinder", "短线技术指标"))
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
        self.cbxTotalAssets.setText(_translate("StockFinder", "市值最小"))
        self.spbTotalAssetsMin.setSuffix(_translate("StockFinder", "亿"))
        self.lblTotalAssetsMax.setText(_translate("StockFinder", "最大"))
        self.spbTotalAssetsMax.setSuffix(_translate("StockFinder", "亿"))
        self.cbxGrossProfit.setText(_translate("StockFinder", "毛利率大于"))
        self.spbGrossProfit.setSuffix(_translate("StockFinder", "%"))
        self.cbxNetProfit.setText(_translate("StockFinder", "净利率大于"))
        self.spbNetProfit.setSuffix(_translate("StockFinder", "%"))
        self.cbxIncomeIncrease.setText(_translate("StockFinder", "收入增长大于"))
        self.spbIncomeIncrease.setSuffix(_translate("StockFinder", "%"))
        self.cbxProfitIncrease.setText(_translate("StockFinder", "利润增长大于"))
        self.spbProfitIncrease.setSuffix(_translate("StockFinder", "%"))
        self.cbxNetAssetProfit.setText(_translate("StockFinder", "净资产收益率大于"))
        self.spbNetAssetProfit.setSuffix(_translate("StockFinder", "%"))
        self.cbxTotalHolders.setText(_translate("StockFinder", "股东人数最少"))
        self.spbTotalHoldersMin.setSuffix(_translate("StockFinder", "万人"))
        self.lblTotalHoldersMax.setText(_translate("StockFinder", "最多"))
        self.spbTotalHoldersMax.setSuffix(_translate("StockFinder", "万人"))
        self.cbxIncludeStStock.setText(_translate("StockFinder", "包含ST股"))
        self.cbxIncludeNewStock.setText(_translate("StockFinder", "包含上市半年内次新股"))
        self.btnGetAllStockData.setText(_translate("StockFinder", "获取全部股票历史日K线"))
        self.btnSaveTechnicalConfig.setText(_translate("StockFinder", "保存技术指标"))
        self.btnLoadTechnicalConfig.setText(_translate("StockFinder", "载入技术指标"))
        self.btnSaveCompanyConfig.setText(_translate("StockFinder", "导出基本面指标"))
        self.btnLoadCompanyConfig.setText(_translate("StockFinder", "导入基本面指标"))
        self.lblGetStockReminder.setText(_translate("StockFinder", "每日请先获取最新股票数据！"))
        self.btnStartSearch.setText(_translate("StockFinder", "开始搜索选股！"))
        self.btnAddCriteria.setText(_translate("StockFinder", "添加"))
        self.btnRemoveCriteria.setText(_translate("StockFinder", "删除"))
        self.btnEditCriteria.setText(_translate("StockFinder", "编辑"))
        self.btnResetCriteria.setText(_translate("StockFinder", "清空"))
