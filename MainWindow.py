import sys
import traceback
import baostock
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from QtDesign.MainWindow_ui import Ui_MainWindow
from LongTermTrading import StockAnalyzer, ScheduledInvestment, TradeSimulator
from ShortTermTrading import StockFinder, SelectedPerformance, PoolMonitor, FifteenMinTrader, FifteenMinFinder
from RealTimeMonitor import LiveTracker
from Data.QueryStockData import query_all_stock_daily_data
from Tools import TradeSettings, FileManager


if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


class MainWindow(QMainWindow, Ui_MainWindow):
    __secondaryWindow = None

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup_triggers()
        self.reconnect_server()

    def setup_triggers(self):
        self.btnStockAnalyzer.clicked.connect(self.show_stock_analyzer)
        self.btnTradeSimulator.clicked.connect(self.show_trade_simulator)
        self.btnStockFinder.clicked.connect(self.show_stock_finder)
        self.btnSelectedPerformance.clicked.connect(self.show_selected_performance)
        self.btnScheduledInvestment.clicked.connect(self.show_scheduled_investment)
        self.btnPoolMonitor.clicked.connect(self.show_pool_monitor)
        self.btn15MinFinder.clicked.connect(self.show_15_min_finder)
        self.btn15MinTrader.clicked.connect(self.show_15_min_trader)

        self.actGetStockList.triggered.connect(self.get_all_stocks_list)
        self.actGetStockData.triggered.connect(self.get_stocks_history_data)
        self.actReconnect.triggered.connect(self.reconnect_server)
        self.actTradeSettings.triggered.connect(self.show_trade_settings)

    @staticmethod
    def reconnect_server():
        baostock.login()

    # 个股股性分析
    def show_stock_analyzer(self):
        self.__secondaryWindow = StockAnalyzer.StockAnalyzer()
        self.__secondaryWindow.show()

    # 趋势模拟交易
    def show_trade_simulator(self):
        self.__secondaryWindow = TradeSimulator.TradeSimulator()
        self.__secondaryWindow.show()

    # 量化指标选股
    def show_stock_finder(self):
        self.__secondaryWindow = StockFinder.StockFinder()
        self.__secondaryWindow.show()

    # 选股表现回测
    def show_selected_performance(self):
        self.__secondaryWindow = SelectedPerformance.SelectedPerformance()
        self.__secondaryWindow.show()

    # 实时盯盘助手
    def show_live_tracker(self):
        self.__secondaryWindow = LiveTracker.LiveTracker()
        self.__secondaryWindow.show()

    # 定投组合表现
    def show_scheduled_investment(self):
        self.__secondaryWindow = ScheduledInvestment.ScheduledInvestment()
        self.__secondaryWindow.show()

    # 股池每日监测
    def show_pool_monitor(self):
        self.__secondaryWindow = PoolMonitor.PoolMonitor()
        self.__secondaryWindow.show()

    # 15分钟线回测
    def show_15_min_finder(self):
        self.__secondaryWindow = FifteenMinFinder.FifteenMinFinder()
        self.__secondaryWindow.show()

    # 15分钟线回测
    def show_15_min_trader(self):
        self.__secondaryWindow = FifteenMinTrader.FifteenMinTrader()
        self.__secondaryWindow.show()

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
        query_all_stock_daily_data()



sys.excepthook = traceback.print_exception


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    # 自动更新股票数据
    if sys.argv[1] == '-auto':
        FileManager.save_stock_list_file()
        query_all_stock_daily_data()
    sys.exit(app.exec_())
