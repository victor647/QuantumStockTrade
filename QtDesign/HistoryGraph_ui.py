# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'HistoryGraph.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_HistoryGraph(object):
    def setupUi(self, HistoryGraph):
        HistoryGraph.setObjectName("HistoryGraph")
        HistoryGraph.resize(1117, 444)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(HistoryGraph.sizePolicy().hasHeightForWidth())
        HistoryGraph.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(HistoryGraph)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.crtMainGraph = QChartView(HistoryGraph)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.crtMainGraph.sizePolicy().hasHeightForWidth())
        self.crtMainGraph.setSizePolicy(sizePolicy)
        self.crtMainGraph.setMinimumSize(QtCore.QSize(0, 300))
        self.crtMainGraph.setObjectName("crtMainGraph")
        self.verticalLayout.addWidget(self.crtMainGraph)
        self.crtSecondaryGraph = QChartView(HistoryGraph)
        self.crtSecondaryGraph.setMinimumSize(QtCore.QSize(0, 120))
        self.crtSecondaryGraph.setMaximumSize(QtCore.QSize(16777215, 150))
        self.crtSecondaryGraph.setObjectName("crtSecondaryGraph")
        self.verticalLayout.addWidget(self.crtSecondaryGraph)

        self.retranslateUi(HistoryGraph)
        QtCore.QMetaObject.connectSlotsByName(HistoryGraph)

    def retranslateUi(self, HistoryGraph):
        _translate = QtCore.QCoreApplication.translate
        HistoryGraph.setWindowTitle(_translate("HistoryGraph", "K线图"))
from PyQt5.QtChart import QChartView
