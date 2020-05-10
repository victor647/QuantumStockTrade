import sys
import traceback
import baostock
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from QtDesign.MainWindow_ui import Ui_MainWindow
from LongTermTrading import StockAnalyzer, ScheduledInvestment, TradeSimulator
from ShortTermTrading import StockFinder, SelectedPerformance
from RealTimeMonitor import LiveTracker
from Data.QueryStockData import query_all_stock_data
from Tools import TradeSettings, FileManager


if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


class MainWindow(QMainWindow, Ui_MainWindow):
    __stockAnalyzer = None
    __tradeSimulator = None
    __stockFinder = None
    __stockTracker = None
    __selectedPerformance = None
    __scheduledInvestment = None

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.reconnect_server()

    @staticmethod
    def reconnect_server():
        baostock.login()

    # 个股股性分析
    def show_stock_analyzer(self):
        self.__stockAnalyzer = StockAnalyzer.StockAnalyzer()
        self.__stockAnalyzer.show()

    # 趋势模拟交易
    def show_trade_simulator(self):
        self.__tradeSimulator = TradeSimulator.TradeSimulator()
        self.__tradeSimulator.show()

    # 量化指标选股
    def show_stock_finder(self):
        self.__stockFinder = StockFinder.StockFinder()
        self.__stockFinder.show()

    # 选股表现回测
    def show_selected_performance(self):
        self.__selectedPerformance = SelectedPerformance.SelectedPerformance()
        self.__selectedPerformance.show()

    # 定投组合表现
    def show_scheduled_investment(self):
        self.__scheduledInvestment = ScheduledInvestment.ScheduledInvestment()
        self.__scheduledInvestment.show()

    # 实时盯盘助手
    def show_live_tracker(self):
        self.__stockTracker = LiveTracker.LiveTracker()
        self.__stockTracker.show()

    # 交易费用设置
    @staticmethod
    def show_trade_settings():
        settings = TradeSettings.TradeSettings()
        settings.show()
        settings.exec_()

    # 获取两市全部股票列表
    def get_all_stocks_list(self):
        FileManager.save_stock_list_file()
        QMessageBox.information(self, '成功', '获取全部股票K线成功！')

    # 获取最新股票K线图
    @staticmethod
    def get_stocks_history_data():
        query_all_stock_data()



sys.excepthook = traceback.print_exception


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
