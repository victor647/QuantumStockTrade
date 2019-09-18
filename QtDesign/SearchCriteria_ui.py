# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SearchCriteria.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SearchCriteria(object):
    def setupUi(self, SearchCriteria):
        SearchCriteria.setObjectName("SearchCriteria")
        SearchCriteria.resize(547, 75)
        self.layoutWidget = QtWidgets.QWidget(SearchCriteria)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 309, 25))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.layoutWidget.setFont(font)
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblFirst = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.lblFirst.setFont(font)
        self.lblFirst.setObjectName("lblFirst")
        self.horizontalLayout.addWidget(self.lblFirst)
        self.spbFirstPeriod = QtWidgets.QSpinBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.spbFirstPeriod.setFont(font)
        self.spbFirstPeriod.setMinimum(1)
        self.spbFirstPeriod.setMaximum(10)
        self.spbFirstPeriod.setObjectName("spbFirstPeriod")
        self.horizontalLayout.addWidget(self.spbFirstPeriod)
        self.cbbQueryLogic = QtWidgets.QComboBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.cbbQueryLogic.setFont(font)
        self.cbbQueryLogic.setObjectName("cbbQueryLogic")
        self.horizontalLayout.addWidget(self.cbbQueryLogic)
        self.cbbComparisonField = QtWidgets.QComboBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.cbbComparisonField.setFont(font)
        self.cbbComparisonField.setObjectName("cbbComparisonField")
        self.horizontalLayout.addWidget(self.cbbComparisonField)
        self.cbbOperator = QtWidgets.QComboBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.cbbOperator.setFont(font)
        self.cbbOperator.setObjectName("cbbOperator")
        self.horizontalLayout.addWidget(self.cbbOperator)
        self.layoutWidget1 = QtWidgets.QWidget(SearchCriteria)
        self.layoutWidget1.setGeometry(QtCore.QRect(322, 10, 214, 58))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.layoutWidget1.setFont(font)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.rbnPastAverage = QtWidgets.QRadioButton(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.rbnPastAverage.setFont(font)
        self.rbnPastAverage.setChecked(True)
        self.rbnPastAverage.setObjectName("rbnPastAverage")
        self.horizontalLayout_2.addWidget(self.rbnPastAverage)
        self.spbAveragePeriod = QtWidgets.QSpinBox(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.spbAveragePeriod.setFont(font)
        self.spbAveragePeriod.setMinimum(1)
        self.spbAveragePeriod.setMaximum(20)
        self.spbAveragePeriod.setProperty("value", 10)
        self.spbAveragePeriod.setObjectName("spbAveragePeriod")
        self.horizontalLayout_2.addWidget(self.spbAveragePeriod)
        self.spbRelativePercentage = QtWidgets.QDoubleSpinBox(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.spbRelativePercentage.setFont(font)
        self.spbRelativePercentage.setDecimals(1)
        self.spbRelativePercentage.setMaximum(1000.0)
        self.spbRelativePercentage.setProperty("value", 20.0)
        self.spbRelativePercentage.setObjectName("spbRelativePercentage")
        self.horizontalLayout_2.addWidget(self.spbRelativePercentage)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.rbnAbsValue = QtWidgets.QRadioButton(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.rbnAbsValue.setFont(font)
        self.rbnAbsValue.setObjectName("rbnAbsValue")
        self.horizontalLayout_3.addWidget(self.rbnAbsValue)
        self.spbAbsValue = QtWidgets.QDoubleSpinBox(self.layoutWidget1)
        self.spbAbsValue.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.spbAbsValue.setFont(font)
        self.spbAbsValue.setSuffix("")
        self.spbAbsValue.setDecimals(1)
        self.spbAbsValue.setMaximum(99999.0)
        self.spbAbsValue.setProperty("value", 10.0)
        self.spbAbsValue.setObjectName("spbAbsValue")
        self.horizontalLayout_3.addWidget(self.spbAbsValue)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.layoutWidget2 = QtWidgets.QWidget(SearchCriteria)
        self.layoutWidget2.setGeometry(QtCore.QRect(70, 40, 161, 27))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.layoutWidget2.setFont(font)
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.btnConfirm = QtWidgets.QPushButton(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.btnConfirm.setFont(font)
        self.btnConfirm.setObjectName("btnConfirm")
        self.horizontalLayout_4.addWidget(self.btnConfirm)
        self.btnCancel = QtWidgets.QPushButton(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.btnCancel.setFont(font)
        self.btnCancel.setObjectName("btnCancel")
        self.horizontalLayout_4.addWidget(self.btnCancel)

        self.retranslateUi(SearchCriteria)
        self.rbnPastAverage.toggled['bool'].connect(self.spbAbsValue.setDisabled)
        self.rbnAbsValue.toggled['bool'].connect(self.spbAveragePeriod.setDisabled)
        self.rbnAbsValue.toggled['bool'].connect(self.spbRelativePercentage.setDisabled)
        self.btnConfirm.clicked.connect(SearchCriteria.save_changes)
        self.btnCancel.clicked.connect(SearchCriteria.discard_changes)
        QtCore.QMetaObject.connectSlotsByName(SearchCriteria)

    def retranslateUi(self, SearchCriteria):
        _translate = QtCore.QCoreApplication.translate
        SearchCriteria.setWindowTitle(_translate("SearchCriteria", "筛选条件"))
        self.lblFirst.setText(_translate("SearchCriteria", "最近"))
        self.spbFirstPeriod.setSuffix(_translate("SearchCriteria", "日"))
        self.rbnPastAverage.setText(_translate("SearchCriteria", "过去"))
        self.spbAveragePeriod.setSuffix(_translate("SearchCriteria", "日平均"))
        self.spbRelativePercentage.setSuffix(_translate("SearchCriteria", "%"))
        self.rbnAbsValue.setText(_translate("SearchCriteria", "绝对值"))
        self.btnConfirm.setText(_translate("SearchCriteria", "保存"))
        self.btnCancel.setText(_translate("SearchCriteria", "取消"))
