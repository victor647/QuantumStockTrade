from QtDesign.PoolMonitor_ui import Ui_PoolMonitor
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import QDate
from Tools import Tools, FileManager
from Data import TechnicalAnalysis as TA
import pandas, baostock


class PoolMonitor(QDialog, Ui_PoolMonitor):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup_triggers()
        self.tblStockList.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def setup_triggers(self):
        self.btnImportStockList.clicked.connect(self.import_stock_list)
        self.btnStartAnalyze.clicked.connect(self.start_analyze)

    # 读取股票列表
    def import_stock_list(self):
        FileManager.import_stock_list(self.fill_stock_list)

    # 根据导入的选股列表文件填表
    def fill_stock_list(self, code: str):
        name = Tools.get_stock_name_from_code(code)
        if name == '':
            return
        row_count = self.tblStockList.rowCount()
        self.tblStockList.insertRow(row_count)
        self.tblStockList.setItem(row_count, 0, QTableWidgetItem(code))
        self.tblStockList.setItem(row_count, 1, QTableWidgetItem(name))
        self.tblStockList.repaint()

    # 开始计算分析
    def start_analyze(self):
        today = QDate.currentDate()
        start_date = today.addMonths(-13).toString('yyyy-MM-dd')
        end_date = today.toString('yyyy-MM-dd')
        for row in range(self.tblStockList.rowCount()):
            stock_code = self.tblStockList.item(row, 0).text()
            market, index_code = Tools.get_trade_center_and_index(stock_code)
            result = baostock.query_history_k_data(code=market + '.' + stock_code, fields='high,close',
                                                   start_date=start_date, end_date=end_date, frequency='d', adjustflag='2')
            stock_data = pandas.DataFrame(result.data, columns=result.fields, dtype=float)
            last_close_price = stock_data.iloc[-1]['close']
            # 最新价格
            column = Tools.add_price_item(self.tblStockList, row, 2, last_close_price, stock_data.iloc[-2]['close'])
            # 3日涨跌幅
            three_day_change = TA.get_percent_change_from_price(last_close_price, stock_data.iloc[-4]['close'])
            column = Tools.add_colored_item(self.tblStockList, row, column, three_day_change, '%')
            # 历史最高
            history_max = stock_data['high'].max()
            column = Tools.add_sortable_item(self.tblStockList, row, column, history_max)
            # 回撤幅度
            fallback_percent = -TA.get_percent_change_from_price(last_close_price, history_max)
            column = Tools.add_sortable_item(self.tblStockList, row, column, fallback_percent, str(fallback_percent) + '%')
            # 距离MA
            column = self.get_percent_from_ma(stock_data, last_close_price, 5, row, column)
            column = self.get_percent_from_ma(stock_data, last_close_price, 20, row, column)
            column = self.get_percent_from_ma(stock_data, last_close_price, 60, row, column)
            column = self.get_percent_from_ma(stock_data, last_close_price, 120, row, column)
            column = self.get_percent_from_ma(stock_data, last_close_price, 250, row, column)

    # 计算距离均线的百分比
    def get_percent_from_ma(self, stock_data: pandas.DataFrame, last_close_price: float, period: int, row: int, column: int):
        if stock_data.shape[0] > period:
            ma = stock_data[-period:]['close'].mean()
            from_ma = TA.get_percent_change_from_price(last_close_price, ma)
            return Tools.add_colored_item(self.tblStockList, row, column, from_ma, '%')
        return column + 1
