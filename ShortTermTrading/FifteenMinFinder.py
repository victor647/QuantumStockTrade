from QtDesign.FifteenMinFinder_ui import Ui_FifteenMinFinder
from Tools import FileManager, Tools
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from Data.QueryStockData import query_stocks_15min_data
import Data.TechnicalAnalysis as TA
import pandas


# 15分钟K线选股
class FifteenMinFinder(QDialog, Ui_FifteenMinFinder):

    def __init__(self):
        self.__stockPool = []
        super().__init__()
        self.setupUi(self)
        self.setup_triggers()

    def setup_triggers(self):
        self.btnImportStockPool.clicked.connect(self.import_stock_list)

    # 导入自选股列表文件
    def import_stock_list(self):
        self.__stockPool = []
        self.tblStockList.setRowCount(0)
        FileManager.import_stock_list(lambda code: self.__stockPool.append(code))
        query_stocks_15min_data(self.__stockPool, self.analyze_diagram)

    # 分析K线是否符合图形
    def analyze_diagram(self, stock_code: str, stock_data: pandas.DataFrame):
        ma_short = self.spbMAShortPeriod.value()
        ma_long = self.spbMALongPeriod.value()
        ma_key_short = TA.calculate_ma_curve(stock_data, ma_short)
        ma_key_long = TA.calculate_ma_curve(stock_data, ma_long)
        period = self.spbOccurancePeriod.value()

        # 均线金叉
        if self.rbnGoldCross.isChecked() and ma_key_long != '':
            short_before = stock_data[ma_key_short].iloc[-period]
            short_now = stock_data[ma_key_short].iloc[-1]
            long_before = stock_data[ma_key_long].iloc[-period]
            long_now = stock_data[ma_key_long].iloc[-1]
            if short_before < long_before and short_now > long_now:
                self.append_selected_stock(stock_code)

    # 开始筛选符合图形的股票
    def append_selected_stock(self, stock_code: str):
        name = Tools.get_stock_name_from_code(stock_code)
        if name == '':
            return
        row_count = self.tblStockList.rowCount()
        self.tblStockList.insertRow(row_count)
        self.tblStockList.setItem(row_count, 0, QTableWidgetItem(stock_code))
        self.tblStockList.setItem(row_count, 1, QTableWidgetItem(name))
