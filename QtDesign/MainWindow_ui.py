# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(225, 143)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 201, 81))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnStockAnalyzer = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnStockAnalyzer.sizePolicy().hasHeightForWidth())
        self.btnStockAnalyzer.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.btnStockAnalyzer.setFont(font)
        self.btnStockAnalyzer.setObjectName("btnStockAnalyzer")
        self.horizontalLayout.addWidget(self.btnStockAnalyzer)
        self.btnStockFinder = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnStockFinder.sizePolicy().hasHeightForWidth())
        self.btnStockFinder.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.btnStockFinder.setFont(font)
        self.btnStockFinder.setObjectName("btnStockFinder")
        self.horizontalLayout.addWidget(self.btnStockFinder)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btnLiveTracker = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnLiveTracker.sizePolicy().hasHeightForWidth())
        self.btnLiveTracker.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.btnLiveTracker.setFont(font)
        self.btnLiveTracker.setObjectName("btnLiveTracker")
        self.horizontalLayout_2.addWidget(self.btnLiveTracker)
        self.btnStockReview = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnStockReview.sizePolicy().hasHeightForWidth())
        self.btnStockReview.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.btnStockReview.setFont(font)
        self.btnStockReview.setObjectName("btnStockReview")
        self.horizontalLayout_2.addWidget(self.btnStockReview)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 225, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actReconnect = QtWidgets.QAction(MainWindow)
        self.actReconnect.setObjectName("actReconnect")
        self.menu.addAction(self.actReconnect)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        self.btnStockAnalyzer.clicked.connect(MainWindow.show_stock_analyzer)
        self.btnStockFinder.clicked.connect(MainWindow.show_stock_finder)
        self.btnLiveTracker.clicked.connect(MainWindow.show_live_tracker)
        self.btnStockReview.clicked.connect(MainWindow.show_stock_reviewer)
        self.actReconnect.triggered.connect(MainWindow.reconnect_server)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "647炒股神器"))
        self.btnStockAnalyzer.setText(_translate("MainWindow", "分析模拟交易"))
        self.btnStockFinder.setText(_translate("MainWindow", "指标选股工具"))
        self.btnLiveTracker.setText(_translate("MainWindow", "实时盯盘助手"))
        self.btnStockReview.setText(_translate("MainWindow", "今日牛股复盘"))
        self.menu.setTitle(_translate("MainWindow", "设置"))
        self.actReconnect.setText(_translate("MainWindow", "断线重连"))
