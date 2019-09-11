import sys
from PyQt5.QtWidgets import QApplication
from QtDesign.MainWindow_ui import Ui_MainWindow
from Windows.StockAnalyzer import *
from Windows.StockFinder import *


class MainWindow(QMainWindow, Ui_MainWindow):
    stockAnalyzer = None
    stockFinder = None

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def show_stock_analyzer(self):
        self.stockAnalyzer = StockAnalyzer()
        self.stockAnalyzer.show()

    def show_stock_finder(self):
        self.stockFinder = StockFinder()
        self.stockFinder.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    baostock.login()
    sys.exit(app.exec_())
