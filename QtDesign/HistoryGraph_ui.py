# Form implementation generated from reading ui file 'HistoryGraph.ui'
#
# Created by: PyQt6 UI code generator 6.9.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_HistoryGraph(object):
    def setupUi(self, HistoryGraph):
        HistoryGraph.setObjectName("HistoryGraph")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(HistoryGraph.sizePolicy().hasHeightForWidth())
        HistoryGraph.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(HistoryGraph)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetNoConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.crtGraph = QChartView(parent=HistoryGraph)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
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
from PyQt6.QtCharts import QChartView
