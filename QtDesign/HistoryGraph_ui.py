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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(HistoryGraph.sizePolicy().hasHeightForWidth())
        HistoryGraph.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(HistoryGraph)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.crtGraph = QChartView(HistoryGraph)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.crtGraph.sizePolicy().hasHeightForWidth())
        self.crtGraph.setSizePolicy(sizePolicy)
        self.crtGraph.setObjectName("crtGraph")
        self.verticalLayout.addWidget(self.crtGraph)

        self.retranslateUi(HistoryGraph)
        QtCore.QMetaObject.connectSlotsByName(HistoryGraph)

    def retranslateUi(self, HistoryGraph):
        _translate = QtCore.QCoreApplication.translate
        HistoryGraph.setWindowTitle(_translate("HistoryGraph", "K线图"))
from PyQt5.QtChart import QChartView
