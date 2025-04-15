# Form implementation generated from reading ui file 'StockFinder.ui'
#
# Created by: PyQt6 UI code generator 6.9.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_StockFinder(object):
    def setupUi(self, StockFinder):
        StockFinder.setObjectName("StockFinder")
        StockFinder.resize(520, 610)
        self.centralwidget = QtWidgets.QWidget(parent=StockFinder)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.grpSearchRange = QtWidgets.QGroupBox(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.grpSearchRange.setFont(font)
        self.grpSearchRange.setObjectName("grpSearchRange")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.grpSearchRange)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.cbxShanghaiMain = QtWidgets.QCheckBox(parent=self.grpSearchRange)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.cbxShanghaiMain.setFont(font)
        self.cbxShanghaiMain.setChecked(True)
        self.cbxShanghaiMain.setObjectName("cbxShanghaiMain")
        self.horizontalLayout_6.addWidget(self.cbxShanghaiMain)
        self.cbxShenZhenNew = QtWidgets.QCheckBox(parent=self.grpSearchRange)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.cbxShenZhenNew.setFont(font)
        self.cbxShenZhenNew.setChecked(True)
        self.cbxShenZhenNew.setObjectName("cbxShenZhenNew")
        self.horizontalLayout_6.addWidget(self.cbxShenZhenNew)
        self.cbxShenZhenSmall = QtWidgets.QCheckBox(parent=self.grpSearchRange)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.cbxShenZhenSmall.setFont(font)
        self.cbxShenZhenSmall.setChecked(True)
        self.cbxShenZhenSmall.setObjectName("cbxShenZhenSmall")
        self.horizontalLayout_6.addWidget(self.cbxShenZhenSmall)
        self.cbxShenZhenMain = QtWidgets.QCheckBox(parent=self.grpSearchRange)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.cbxShenZhenMain.setFont(font)
        self.cbxShenZhenMain.setChecked(True)
        self.cbxShenZhenMain.setObjectName("cbxShenZhenMain")
        self.horizontalLayout_6.addWidget(self.cbxShenZhenMain)
        self.cbxShanghaiScience = QtWidgets.QCheckBox(parent=self.grpSearchRange)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.cbxShanghaiScience.setFont(font)
        self.cbxShanghaiScience.setChecked(True)
        self.cbxShanghaiScience.setObjectName("cbxShanghaiScience")
        self.horizontalLayout_6.addWidget(self.cbxShanghaiScience)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.lblSearchDate = QtWidgets.QLabel(parent=self.grpSearchRange)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.lblSearchDate.setFont(font)
        self.lblSearchDate.setObjectName("lblSearchDate")
        self.horizontalLayout_13.addWidget(self.lblSearchDate)
        self.dteSearchDate = QtWidgets.QDateEdit(parent=self.grpSearchRange)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.dteSearchDate.setFont(font)
        self.dteSearchDate.setObjectName("dteSearchDate")
        self.horizontalLayout_13.addWidget(self.dteSearchDate)
        self.btnStartSearch = QtWidgets.QPushButton(parent=self.grpSearchRange)
        self.btnStartSearch.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.btnStartSearch.setFont(font)
        self.btnStartSearch.setObjectName("btnStartSearch")
        self.horizontalLayout_13.addWidget(self.btnStartSearch)
        self.btnAutoSearch = QtWidgets.QPushButton(parent=self.grpSearchRange)
        self.btnAutoSearch.setObjectName("btnAutoSearch")
        self.horizontalLayout_13.addWidget(self.btnAutoSearch)
        self.verticalLayout_2.addLayout(self.horizontalLayout_13)
        self.verticalLayout_6.addWidget(self.grpSearchRange)
        self.grpBasicCriterias = QtWidgets.QGroupBox(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.grpBasicCriterias.setFont(font)
        self.grpBasicCriterias.setObjectName("grpBasicCriterias")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.grpBasicCriterias)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.cbxPE = QtWidgets.QCheckBox(parent=self.grpBasicCriterias)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.cbxPE.setFont(font)
        self.cbxPE.setChecked(False)
        self.cbxPE.setObjectName("cbxPE")
        self.horizontalLayout_12.addWidget(self.cbxPE)
        self.spbPEMax = QtWidgets.QSpinBox(parent=self.grpBasicCriterias)
        self.spbPEMax.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.spbPEMax.setFont(font)
        self.spbPEMax.setMinimum(-100)
        self.spbPEMax.setMaximum(1000)
        self.spbPEMax.setProperty("value", 50)
        self.spbPEMax.setObjectName("spbPEMax")
        self.horizontalLayout_12.addWidget(self.spbPEMax)
        self.cbxPB = QtWidgets.QCheckBox(parent=self.grpBasicCriterias)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.cbxPB.setFont(font)
        self.cbxPB.setChecked(False)
        self.cbxPB.setObjectName("cbxPB")
        self.horizontalLayout_12.addWidget(self.cbxPB)
        self.spbPBMax = QtWidgets.QDoubleSpinBox(parent=self.grpBasicCriterias)
        self.spbPBMax.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.spbPBMax.setFont(font)
        self.spbPBMax.setDecimals(1)
        self.spbPBMax.setMinimum(-1.0)
        self.spbPBMax.setSingleStep(0.5)
        self.spbPBMax.setProperty("value", 5.0)
        self.spbPBMax.setObjectName("spbPBMax")
        self.horizontalLayout_12.addWidget(self.spbPBMax)
        self.verticalLayout_3.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.cbxPS = QtWidgets.QCheckBox(parent=self.grpBasicCriterias)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.cbxPS.setFont(font)
        self.cbxPS.setChecked(False)
        self.cbxPS.setObjectName("cbxPS")
        self.horizontalLayout_2.addWidget(self.cbxPS)
        self.spbPSMax = QtWidgets.QDoubleSpinBox(parent=self.grpBasicCriterias)
        self.spbPSMax.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.spbPSMax.setFont(font)
        self.spbPSMax.setSuffix("")
        self.spbPSMax.setDecimals(1)
        self.spbPSMax.setMinimum(0.0)
        self.spbPSMax.setMaximum(10.0)
        self.spbPSMax.setSingleStep(0.1)
        self.spbPSMax.setProperty("value", 2.0)
        self.spbPSMax.setObjectName("spbPSMax")
        self.horizontalLayout_2.addWidget(self.spbPSMax)
        self.cbxIncludeST = QtWidgets.QCheckBox(parent=self.grpBasicCriterias)
        self.cbxIncludeST.setObjectName("cbxIncludeST")
        self.horizontalLayout_2.addWidget(self.cbxIncludeST)
        self.btnExportBasicConfig = QtWidgets.QPushButton(parent=self.grpBasicCriterias)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.btnExportBasicConfig.setFont(font)
        self.btnExportBasicConfig.setObjectName("btnExportBasicConfig")
        self.horizontalLayout_2.addWidget(self.btnExportBasicConfig)
        self.btnImportBasicConfig = QtWidgets.QPushButton(parent=self.grpBasicCriterias)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.btnImportBasicConfig.setFont(font)
        self.btnImportBasicConfig.setObjectName("btnImportBasicConfig")
        self.horizontalLayout_2.addWidget(self.btnImportBasicConfig)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout_6.addWidget(self.grpBasicCriterias)
        self.grpTechnicalCriterias = QtWidgets.QGroupBox(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.grpTechnicalCriterias.setFont(font)
        self.grpTechnicalCriterias.setObjectName("grpTechnicalCriterias")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.grpTechnicalCriterias)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.spbTechnicalTimePeriod = QtWidgets.QSpinBox(parent=self.grpTechnicalCriterias)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.spbTechnicalTimePeriod.setFont(font)
        self.spbTechnicalTimePeriod.setMinimum(1)
        self.spbTechnicalTimePeriod.setMaximum(100)
        self.spbTechnicalTimePeriod.setProperty("value", 3)
        self.spbTechnicalTimePeriod.setObjectName("spbTechnicalTimePeriod")
        self.horizontalLayout_3.addWidget(self.spbTechnicalTimePeriod)
        self.lblTechnicalTimePeriod = QtWidgets.QLabel(parent=self.grpTechnicalCriterias)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.lblTechnicalTimePeriod.setFont(font)
        self.lblTechnicalTimePeriod.setObjectName("lblTechnicalTimePeriod")
        self.horizontalLayout_3.addWidget(self.lblTechnicalTimePeriod)
        self.btnExportTechnicalConfig = QtWidgets.QPushButton(parent=self.grpTechnicalCriterias)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.btnExportTechnicalConfig.setFont(font)
        self.btnExportTechnicalConfig.setObjectName("btnExportTechnicalConfig")
        self.horizontalLayout_3.addWidget(self.btnExportTechnicalConfig)
        self.btnImportTechnicalConfig = QtWidgets.QPushButton(parent=self.grpTechnicalCriterias)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.btnImportTechnicalConfig.setFont(font)
        self.btnImportTechnicalConfig.setObjectName("btnImportTechnicalConfig")
        self.horizontalLayout_3.addWidget(self.btnImportTechnicalConfig)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.cbxMACD = QtWidgets.QCheckBox(parent=self.grpTechnicalCriterias)
        self.cbxMACD.setMaximumSize(QtCore.QSize(100, 16777215))
        self.cbxMACD.setChecked(False)
        self.cbxMACD.setObjectName("cbxMACD")
        self.horizontalLayout_10.addWidget(self.cbxMACD)
        self.cbbMACDBehaviour = QtWidgets.QComboBox(parent=self.grpTechnicalCriterias)
        self.cbbMACDBehaviour.setEnabled(False)
        self.cbbMACDBehaviour.setObjectName("cbbMACDBehaviour")
        self.horizontalLayout_10.addWidget(self.cbbMACDBehaviour)
        self.cbxBOLL = QtWidgets.QCheckBox(parent=self.grpTechnicalCriterias)
        self.cbxBOLL.setEnabled(True)
        self.cbxBOLL.setChecked(False)
        self.cbxBOLL.setObjectName("cbxBOLL")
        self.horizontalLayout_10.addWidget(self.cbxBOLL)
        self.cbbBOLLTrack = QtWidgets.QComboBox(parent=self.grpTechnicalCriterias)
        self.cbbBOLLTrack.setEnabled(False)
        self.cbbBOLLTrack.setObjectName("cbbBOLLTrack")
        self.horizontalLayout_10.addWidget(self.cbbBOLLTrack)
        self.cbxBBI = QtWidgets.QCheckBox(parent=self.grpTechnicalCriterias)
        self.cbxBBI.setObjectName("cbxBBI")
        self.horizontalLayout_10.addWidget(self.cbxBBI)
        self.verticalLayout_4.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.cbxMA = QtWidgets.QCheckBox(parent=self.grpTechnicalCriterias)
        self.cbxMA.setMaximumSize(QtCore.QSize(50, 16777215))
        self.cbxMA.setChecked(False)
        self.cbxMA.setObjectName("cbxMA")
        self.horizontalLayout_7.addWidget(self.cbxMA)
        self.spbMaShort = QtWidgets.QSpinBox(parent=self.grpTechnicalCriterias)
        self.spbMaShort.setEnabled(False)
        self.spbMaShort.setMinimum(5)
        self.spbMaShort.setMaximum(20)
        self.spbMaShort.setObjectName("spbMaShort")
        self.horizontalLayout_7.addWidget(self.spbMaShort)
        self.lblMABehaviour = QtWidgets.QLabel(parent=self.grpTechnicalCriterias)
        self.lblMABehaviour.setMaximumSize(QtCore.QSize(40, 16777215))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.lblMABehaviour.setFont(font)
        self.lblMABehaviour.setObjectName("lblMABehaviour")
        self.horizontalLayout_7.addWidget(self.lblMABehaviour)
        self.spbMaLong = QtWidgets.QSpinBox(parent=self.grpTechnicalCriterias)
        self.spbMaLong.setEnabled(False)
        self.spbMaLong.setMinimum(10)
        self.spbMaLong.setMaximum(60)
        self.spbMaLong.setObjectName("spbMaLong")
        self.horizontalLayout_7.addWidget(self.spbMaLong)
        self.cbxSpecialShape = QtWidgets.QCheckBox(parent=self.grpTechnicalCriterias)
        self.cbxSpecialShape.setChecked(False)
        self.cbxSpecialShape.setObjectName("cbxSpecialShape")
        self.horizontalLayout_7.addWidget(self.cbxSpecialShape)
        self.cbbSpecialShape = QtWidgets.QComboBox(parent=self.grpTechnicalCriterias)
        self.cbbSpecialShape.setEnabled(False)
        self.cbbSpecialShape.setObjectName("cbbSpecialShape")
        self.horizontalLayout_7.addWidget(self.cbbSpecialShape)
        self.verticalLayout_4.addLayout(self.horizontalLayout_7)
        self.verticalLayout_6.addWidget(self.grpTechnicalCriterias)
        self.grpCustomCriterias = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.grpCustomCriterias.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.grpCustomCriterias.setFont(font)
        self.grpCustomCriterias.setObjectName("grpCustomCriterias")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.grpCustomCriterias)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.lstCriteriaItems = QtWidgets.QListWidget(parent=self.grpCustomCriterias)
        self.lstCriteriaItems.setMinimumSize(QtCore.QSize(250, 0))
        self.lstCriteriaItems.setObjectName("lstCriteriaItems")
        self.verticalLayout_5.addWidget(self.lstCriteriaItems)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnAddCriteria = QtWidgets.QPushButton(parent=self.grpCustomCriterias)
        self.btnAddCriteria.setObjectName("btnAddCriteria")
        self.horizontalLayout.addWidget(self.btnAddCriteria)
        self.btnEditCriteria = QtWidgets.QPushButton(parent=self.grpCustomCriterias)
        self.btnEditCriteria.setObjectName("btnEditCriteria")
        self.horizontalLayout.addWidget(self.btnEditCriteria)
        self.btnRemoveCriteria = QtWidgets.QPushButton(parent=self.grpCustomCriterias)
        self.btnRemoveCriteria.setObjectName("btnRemoveCriteria")
        self.horizontalLayout.addWidget(self.btnRemoveCriteria)
        self.btnResetCriteria = QtWidgets.QPushButton(parent=self.grpCustomCriterias)
        self.btnResetCriteria.setObjectName("btnResetCriteria")
        self.horizontalLayout.addWidget(self.btnResetCriteria)
        self.btnExportCustomConfig = QtWidgets.QPushButton(parent=self.grpCustomCriterias)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.btnExportCustomConfig.setFont(font)
        self.btnExportCustomConfig.setObjectName("btnExportCustomConfig")
        self.horizontalLayout.addWidget(self.btnExportCustomConfig)
        self.btnImportCustomConfig = QtWidgets.QPushButton(parent=self.grpCustomCriterias)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.btnImportCustomConfig.setFont(font)
        self.btnImportCustomConfig.setObjectName("btnImportCustomConfig")
        self.horizontalLayout.addWidget(self.btnImportCustomConfig)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.verticalLayout_6.addWidget(self.grpCustomCriterias)
        StockFinder.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=StockFinder)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 520, 23))
        self.menubar.setObjectName("menubar")
        StockFinder.setMenuBar(self.menubar)

        self.retranslateUi(StockFinder)
        QtCore.QMetaObject.connectSlotsByName(StockFinder)

    def retranslateUi(self, StockFinder):
        _translate = QtCore.QCoreApplication.translate
        StockFinder.setWindowTitle(_translate("StockFinder", "智能选股器"))
        self.grpSearchRange.setTitle(_translate("StockFinder", "搜索范围"))
        self.cbxShanghaiMain.setText(_translate("StockFinder", "上海主板"))
        self.cbxShenZhenNew.setText(_translate("StockFinder", "创业板"))
        self.cbxShenZhenSmall.setText(_translate("StockFinder", "中小板"))
        self.cbxShenZhenMain.setText(_translate("StockFinder", "深圳主板"))
        self.cbxShanghaiScience.setText(_translate("StockFinder", "科创板"))
        self.lblSearchDate.setText(_translate("StockFinder", "选股日期"))
        self.dteSearchDate.setDisplayFormat(_translate("StockFinder", "yyyy-MM-dd"))
        self.btnStartSearch.setText(_translate("StockFinder", "开始搜索选股"))
        self.btnAutoSearch.setText(_translate("StockFinder", "定时自动选股"))
        self.grpBasicCriterias.setTitle(_translate("StockFinder", "基本面指标"))
        self.cbxPE.setText(_translate("StockFinder", "市盈率（TTM）"))
        self.spbPEMax.setSuffix(_translate("StockFinder", "倍"))
        self.spbPEMax.setPrefix(_translate("StockFinder", "<"))
        self.cbxPB.setText(_translate("StockFinder", "市净率（MRQ）"))
        self.spbPBMax.setPrefix(_translate("StockFinder", "<"))
        self.spbPBMax.setSuffix(_translate("StockFinder", "倍"))
        self.cbxPS.setText(_translate("StockFinder", "市销率（TTM）"))
        self.spbPSMax.setPrefix(_translate("StockFinder", "<"))
        self.cbxIncludeST.setText(_translate("StockFinder", "包含ST股"))
        self.btnExportBasicConfig.setText(_translate("StockFinder", "保存"))
        self.btnImportBasicConfig.setText(_translate("StockFinder", "载入"))
        self.grpTechnicalCriterias.setTitle(_translate("StockFinder", "技术面指标"))
        self.spbTechnicalTimePeriod.setSuffix(_translate("StockFinder", "日内"))
        self.spbTechnicalTimePeriod.setPrefix(_translate("StockFinder", "最近"))
        self.lblTechnicalTimePeriod.setText(_translate("StockFinder", "指标出现以下信号"))
        self.btnExportTechnicalConfig.setText(_translate("StockFinder", "保存"))
        self.btnImportTechnicalConfig.setText(_translate("StockFinder", "载入"))
        self.cbxMACD.setText(_translate("StockFinder", "MACD"))
        self.cbxBOLL.setText(_translate("StockFinder", "BOLL"))
        self.cbxBBI.setText(_translate("StockFinder", "站稳BBI"))
        self.cbxMA.setText(_translate("StockFinder", "MA"))
        self.spbMaShort.setSuffix(_translate("StockFinder", "日"))
        self.lblMABehaviour.setText(_translate("StockFinder", "金叉"))
        self.spbMaLong.setSuffix(_translate("StockFinder", "日"))
        self.cbxSpecialShape.setText(_translate("StockFinder", "特殊K线组合"))
        self.grpCustomCriterias.setTitle(_translate("StockFinder", "自定义指标"))
        self.btnAddCriteria.setText(_translate("StockFinder", "添加"))
        self.btnEditCriteria.setText(_translate("StockFinder", "编辑"))
        self.btnRemoveCriteria.setText(_translate("StockFinder", "删除"))
        self.btnResetCriteria.setText(_translate("StockFinder", "清空"))
        self.btnExportCustomConfig.setText(_translate("StockFinder", "导出"))
        self.btnImportCustomConfig.setText(_translate("StockFinder", "导入"))
