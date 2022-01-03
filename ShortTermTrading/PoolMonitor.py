from QtDesign.PoolMonitor_ui import Ui_PoolMonitor
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import QDate
from Tools import Tools, FileManager
from Data import TechnicalAnalysis as TA
from Data import HistoryGraph
import pandas, baostock


class PoolMonitor(QDialog, Ui_PoolMonitor):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup_triggers()
        self.tblStockList.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        today = QDate.currentDate()
        self.__startDate = today.addMonths(-13).toString('yyyy-MM-dd')
        self.__endDate = today.toString('yyyy-MM-dd')

    def setup_triggers(self):
        self.btnImportPool.clicked.connect(self.import_stock_list)
        self.btnAddStock.clicked.connect(self.add_stock_code)
        self.btnRemoveStock.clicked.connect(self.remove_stock_code)
        self.btnClearStocks.clicked.connect(self.clear_stock_list)
        self.tblStockList.cellDoubleClicked['int', 'int'].connect(self.stock_detailed_info)

    # 读取股票列表
    def import_stock_list(self):
        FileManager.import_stock_list(self.analyze_stock)

    # 添加股票按钮
    def add_stock_code(self):
        stock_code = Tools.get_stock_code(self.iptStockCode)
        if stock_code == '':
            Tools.show_error_dialog('股票代码或名称无效！')
        else:
            self.analyze_stock(stock_code)

    # 移除一只股票
    def remove_stock_code(self):
        selection = self.tblStockList.selectedIndexes()
        if len(selection) == 0:
            return
        index = selection[0].row()
        self.tblStockList.removeRow(index)

    # 清空股票列表
    def clear_stock_list(self):
        self.tblStockList.setRowCount(0)

    # 读取股票信息并分析
    def analyze_stock(self, stock_code: str):
        row = self.tblStockList.rowCount()
        self.tblStockList.insertRow(row)
        self.tblStockList.setItem(row, 0, QTableWidgetItem(stock_code))
        market, index_code = Tools.get_trade_center_and_index(stock_code)
        full_code = market + '.' + stock_code
        # 股票名称
        result = baostock.query_stock_basic(code=full_code)
        self.tblStockList.setItem(row, 1, QTableWidgetItem(result.data[0][1]))
        result = baostock.query_history_k_data(code=full_code, fields='high,close',
                                               start_date=self.__startDate, end_date=self.__endDate, frequency='d', adjustflag='2')
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
        fallback_percent = TA.get_percent_change_from_price(last_close_price, history_max)
        if fallback_percent < 0:
            fallback_percent *= -1
        column = Tools.add_sortable_item(self.tblStockList, row, column, fallback_percent, str(fallback_percent) + '%')
        # 距离MA
        column = self.get_percent_from_ma(stock_data, last_close_price, 5, row, column)
        column = self.get_percent_from_ma(stock_data, last_close_price, 20, row, column)
        column = self.get_percent_from_ma(stock_data, last_close_price, 60, row, column)
        column = self.get_percent_from_ma(stock_data, last_close_price, 120, row, column)
        column = self.get_percent_from_ma(stock_data, last_close_price, 250, row, column)
        self.tblStockList.repaint()

    # 计算距离均线的百分比
    def get_percent_from_ma(self, stock_data: pandas.DataFrame, last_close_price: float, period: int, row: int, column: int):
        if stock_data.shape[0] > period:
            ma = stock_data[-period:]['close'].mean()
            from_ma = TA.get_percent_change_from_price(last_close_price, ma)
            return Tools.add_colored_item(self.tblStockList, row, column, from_ma, '%')
        return column + 1

    # 显示股票详细数据
    def stock_detailed_info(self, row: int, column: int):
        stock_code = self.tblStockList.item(row, 0).text()
        # 通过网页打开
        if column < 2:
            Tools.open_stock_page(stock_code)
        # 股票K线图
        else:
            HistoryGraph.plot_pooled_stock_graph(stock_code)
