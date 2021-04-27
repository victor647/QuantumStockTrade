import sys
import traceback
import baostock, tushare
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from QtDesign.MainWindow_ui import Ui_MainWindow
from LongTermTrading import StockAnalyzer, ScheduledInvestment, TradeSimulator
from ShortTermTrading import StockFinder, SelectedPerformance, PoolMonitor, FifteenMinTrader
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
    __poolMonitor = None
    __15MinTrader = None

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
        self.btnLiveTracker.clicked.connect(self.show_live_tracker)
        self.btnScheduledInvestment.clicked.connect(self.show_scheduled_investment)
        self.btnPoolMonitor.clicked.connect(self.show_pool_monitor)
        self.btn15MinTrader.clicked.connect(self.show_15_min_trader)

    @staticmethod
    def reconnect_server():
        baostock.login()
        tushare.set_token('eee03f328c31ce7b74e1f0417863e4019723e9bdda3fb0d243cf9a1c')

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

    # 实时盯盘助手
    def show_live_tracker(self):
        self.__stockTracker = LiveTracker.LiveTracker()
        self.__stockTracker.show()

    # 定投组合表现
    def show_scheduled_investment(self):
        self.__scheduledInvestment = ScheduledInvestment.ScheduledInvestment()
        self.__scheduledInvestment.show()

    # 股池每日监测
    def show_pool_monitor(self):
        self.__poolMonitor = PoolMonitor.PoolMonitor()
        self.__poolMonitor.show()

    # 15分钟线掘金
    def show_15_min_trader(self):
        self.__15MinTrader = FifteenMinTrader.FifteenMinTrader()
        self.__15MinTrader.show()

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
