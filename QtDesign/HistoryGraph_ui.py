# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'HistoryGraph.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_HistoryGraph(object):
    def setupUi(self, HistoryGraph):
        HistoryGraph.setObjectName("HistoryGraph")
        HistoryGraph.resize(735, 401)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(HistoryGraph.sizePolicy().hasHeightForWidth())
        HistoryGraph.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtWidgets.QHBoxLayout(HistoryGraph)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.crtCandleStick = QChartView(HistoryGraph)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.crtCandleStick.sizePolicy().hasHeightForWidth())
        self.crtCandleStick.setSizePolicy(sizePolicy)
        self.crtCandleStick.setObjectName("crtCandleStick")
        self.horizontalLayout.addWidget(self.crtCandleStick)

        self.retranslateUi(HistoryGraph)
        QtCore.QMetaObject.connectSlotsByName(HistoryGraph)

    def retranslateUi(self, HistoryGraph):
        _translate = QtCore.QCoreApplication.translate
        HistoryGraph.setWindowTitle(_translate("HistoryGraph", "K线图"))
from PyQt5.QtChart import QChartView
