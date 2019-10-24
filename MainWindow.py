import sys
import traceback
import baostock
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
from QtDesign.MainWindow_ui import Ui_MainWindow
from Windows import StockReviewer
from StockAnalyzer import StockAnalyzer
from StockFinder import StockFinder
from RealTimeMonitor import LiveTracker


if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


class MainWindow(QMainWindow, Ui_MainWindow):
    __stockAnalyzer = None
    __stockFinder = None
    __stockTracker = None
    __stockReviewer = None

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.reconnect_server()

    @staticmethod
    def reconnect_server():
        baostock.login()

    def show_stock_analyzer(self):
        self.__stockAnalyzer = StockAnalyzer.StockAnalyzer()
        self.__stockAnalyzer.show()

    def show_stock_finder(self):
        self.__stockFinder = StockFinder.StockFinder()
        self.__stockFinder.show()

    def show_live_tracker(self):
        self.__stockTracker = LiveTracker.LiveTracker()
        self.__stockTracker.show()

    def show_stock_reviewer(self):
        self.__stockReviewer = StockReviewer.StockReviewer()
        self.__stockReviewer.show()


sys.excepthook = traceback.print_exception


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
