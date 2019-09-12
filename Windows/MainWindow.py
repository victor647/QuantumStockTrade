import sys
import baostock
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
from QtDesign.MainWindow_ui import Ui_MainWindow
import Windows.StockAnalyzer as StockAnalyzer
import Windows.StockFinder as StockFinder

if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


class MainWindow(QMainWindow, Ui_MainWindow):
    stockAnalyzer = None
    stockFinder = None

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def show_stock_analyzer(self):
        self.stockAnalyzer = StockAnalyzer.StockAnalyzer()
        self.stockAnalyzer.show()

    def show_stock_finder(self):
        self.stockFinder = StockFinder.StockFinder()
        self.stockFinder.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    baostock.login()
    sys.exit(app.exec_())
