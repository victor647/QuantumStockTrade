import baostock, pandas
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QDialog
from QtDesign.TradeStrategy_ui import Ui_TradeStrategy
import LongTermTrading.TradeSimulator as TradeSimulator
import Data.TechnicalAnalysis as TechnicalAnalysis
from Data.HistoryGraph import PriceDistributionChart
from Tools import Tools, FileManager


class TradeSimulator(QDialog, Ui_TradeStrategy):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    # 开始模拟交易
    def start_trading(self):
        stock_code = Tools.get_stock_code(self.iptStockNumber)
        start_date = self.dteStart.date().toString()
        end_date = self.dteStart.date().toString()
        trade_window = TradeSimulator.TradeSimulator(self, stock_code, start_date, end_date)
        trade_window.show()
        trade_window.exec_()





