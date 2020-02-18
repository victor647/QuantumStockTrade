# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TradeSettings.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TradeSettings(object):
    def setupUi(self, TradeSettings):
        TradeSettings.setObjectName("TradeSettings")
        TradeSettings.resize(248, 79)
        self.verticalLayout = QtWidgets.QVBoxLayout(TradeSettings)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(TradeSettings)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.spbBrokerFeePercentage = QtWidgets.QDoubleSpinBox(TradeSettings)
        self.spbBrokerFeePercentage.setMinimumSize(QtCore.QSize(65, 0))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.spbBrokerFeePercentage.setFont(font)
        self.spbBrokerFeePercentage.setDecimals(1)
        self.spbBrokerFeePercentage.setMaximum(10.0)
        self.spbBrokerFeePercentage.setSingleStep(0.1)
        self.spbBrokerFeePercentage.setProperty("value", 1.5)
        self.spbBrokerFeePercentage.setObjectName("spbBrokerFeePercentage")
        self.horizontalLayout.addWidget(self.spbBrokerFeePercentage)
        self.label_3 = QtWidgets.QLabel(TradeSettings)
        self.label_3.setMaximumSize(QtCore.QSize(30, 16777215))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.spbMinBrokerFee = QtWidgets.QSpinBox(TradeSettings)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.spbMinBrokerFee.setFont(font)
        self.spbMinBrokerFee.setPrefix("")
        self.spbMinBrokerFee.setProperty("value", 5)
        self.spbMinBrokerFee.setObjectName("spbMinBrokerFee")
        self.horizontalLayout.addWidget(self.spbMinBrokerFee)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(TradeSettings)
        self.label_2.setMaximumSize(QtCore.QSize(60, 16777215))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.spbStampDuty = QtWidgets.QDoubleSpinBox(TradeSettings)
        self.spbStampDuty.setMaximumSize(QtCore.QSize(65, 16777215))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.spbStampDuty.setFont(font)
        self.spbStampDuty.setPrefix("")
        self.spbStampDuty.setDecimals(1)
        self.spbStampDuty.setMaximum(10.0)
        self.spbStampDuty.setSingleStep(0.1)
        self.spbStampDuty.setProperty("value", 1.0)
        self.spbStampDuty.setObjectName("spbStampDuty")
        self.horizontalLayout_2.addWidget(self.spbStampDuty)
        self.btnSave = QtWidgets.QPushButton(TradeSettings)
        self.btnSave.setObjectName("btnSave")
        self.horizontalLayout_2.addWidget(self.btnSave)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(TradeSettings)
        self.btnSave.clicked.connect(TradeSettings.save_settings)
        QtCore.QMetaObject.connectSlotsByName(TradeSettings)

    def retranslateUi(self, TradeSettings):
        _translate = QtCore.QCoreApplication.translate
        TradeSettings.setWindowTitle(_translate("TradeSettings", "交易设置"))
        self.label.setText(_translate("TradeSettings", "券商佣金："))
        self.spbBrokerFeePercentage.setPrefix(_translate("TradeSettings", "万"))
        self.label_3.setText(_translate("TradeSettings", "最低"))
        self.spbMinBrokerFee.setSuffix(_translate("TradeSettings", "元"))
        self.label_2.setText(_translate("TradeSettings", "印花税："))
        self.spbStampDuty.setSuffix(_translate("TradeSettings", "‰"))
        self.btnSave.setText(_translate("TradeSettings", "确定"))
