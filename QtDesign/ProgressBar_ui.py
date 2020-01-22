# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ProgressBar.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ProgressBar(object):
    def setupUi(self, ProgressBar):
        ProgressBar.setObjectName("ProgressBar")
        ProgressBar.resize(348, 73)
        self.layoutWidget = QtWidgets.QWidget(ProgressBar)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 10, 311, 51))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pgbSearching = QtWidgets.QProgressBar(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pgbSearching.setFont(font)
        self.pgbSearching.setProperty("value", 0)
        self.pgbSearching.setObjectName("pgbSearching")
        self.verticalLayout.addWidget(self.pgbSearching)
        self.lblCurrentWorking = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.lblCurrentWorking.setFont(font)
        self.lblCurrentWorking.setObjectName("lblCurrentWorking")
        self.verticalLayout.addWidget(self.lblCurrentWorking)

        self.retranslateUi(ProgressBar)
        QtCore.QMetaObject.connectSlotsByName(ProgressBar)

    def retranslateUi(self, ProgressBar):
        _translate = QtCore.QCoreApplication.translate
        ProgressBar.setWindowTitle(_translate("ProgressBar", "计算中，请耐心等待"))
        self.lblCurrentWorking.setText(_translate("ProgressBar", "正在分析："))
