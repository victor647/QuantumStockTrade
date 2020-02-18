# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ProgressBar.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ProgressBar(object):
    def setupUi(self, ProgressBar):
        ProgressBar.setObjectName("ProgressBar")
        ProgressBar.resize(342, 62)
        self.verticalLayout = QtWidgets.QVBoxLayout(ProgressBar)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pgbSearching = QtWidgets.QProgressBar(ProgressBar)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.pgbSearching.setFont(font)
        self.pgbSearching.setProperty("value", 0)
        self.pgbSearching.setObjectName("pgbSearching")
        self.verticalLayout.addWidget(self.pgbSearching)
        self.lblCurrentWorking = QtWidgets.QLabel(ProgressBar)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(9)
        self.lblCurrentWorking.setFont(font)
        self.lblCurrentWorking.setObjectName("lblCurrentWorking")
        self.verticalLayout.addWidget(self.lblCurrentWorking)

        self.retranslateUi(ProgressBar)
        QtCore.QMetaObject.connectSlotsByName(ProgressBar)

    def retranslateUi(self, ProgressBar):
        _translate = QtCore.QCoreApplication.translate
        ProgressBar.setWindowTitle(_translate("ProgressBar", "计算中，请耐心等待"))
        self.lblCurrentWorking.setText(_translate("ProgressBar", "正在分析："))
