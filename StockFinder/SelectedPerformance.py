from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView
from QtDesign.SelectedPerformance_ui import Ui_SelectedPerformance
import Data.TechnicalAnalysis as TechnicalAnalysis
from datetime import date
import baostock, Tools, os.path, pandas, FileManager


class SelectedPerformance(QMainWindow, Ui_SelectedPerformance):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 初始化日期显示
        self.dteSearchDate.setDate(QDate.currentDate().addMonths(-1))
        # 为表格自动设置列宽
        self.tblStockList.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    # 导入股票信息
    def import_stock_list(self):
        file = FileManager.import_stock_list(self.fill_stock_list)
        # 通过文件创建时间获取选股日期
        creation_date = date.fromtimestamp(os.path.getctime(file))
        self.dteSearchDate.setDate(creation_date)

    # 导出股票列表
    def export_stock_list(self):
        FileManager.export_stock_list(self.tblStockList)

    # 清空股票列表
    def clear_stock_list(self):
        self.tblStockList.setRowCount(0)

    # 添加股票按钮
    def add_stock_code(self):
        code = self.iptStockCode.text()
        self.fill_stock_list(code)

    # 移除一只股票
    def remove_stock_code(self):
        selection = self.tblStockList.selectedIndexes()
        if len(selection) == 0:
            return
        index = selection[0].row()
        self.tblStockList.removeRow(index)

    # 根据导入的选股列表文件填表
    def fill_stock_list(self, code: str):
        row_count = self.tblStockList.rowCount()
        self.tblStockList.insertRow(row_count)
        # 获取股票名称
        name = Tools.get_stock_name(code)
        self.tblStockList.setItem(row_count, 0, QTableWidgetItem(code))
        self.tblStockList.setItem(row_count, 1, QTableWidgetItem(name))

    # 获取列表中股票历史数据
    def get_stock_data(self):
        start_date = self.dteSearchDate.date().toString('yyyy-MM-dd')
        end_date = QDate.currentDate().toString('yyyy-MM-dd')
        if start_date == end_date:
            Tools.show_error_dialog("回测开始时间不能为当日！")
            return
        for row in range(self.tblStockList.rowCount()):
            # 从表格中获取股票代码
            stock_code = self.tblStockList.item(row, 0).text()
            # 获取交易所信息
            market = Tools.get_trade_center(stock_code)
            result = baostock.query_history_k_data_plus(code=market + "." + stock_code, fields="date,open,high,low,close,preclose,pctChg",
                                                        start_date=start_date, end_date=end_date, frequency="d", adjustflag="2")
            data = pandas.DataFrame(result.data, columns=result.fields, dtype=float)
            column = 2
            initial_price = data['close'].iloc[0]
            self.tblStockList.setItem(row, column, QTableWidgetItem(str(initial_price)))
            buy_price = data['open'].iloc[1]
            column += 1
            column = Tools.add_price_item(self.tblStockList, buy_price, initial_price, row, column)
            column = self.get_day_performance(1, column, row, data, buy_price)
            column = self.get_day_performance(3, column, row, data, buy_price)
            column = self.get_day_performance(5, column, row, data, buy_price)
            column = self.get_day_performance(10, column, row, data, buy_price)
            column = self.get_day_performance(-1, column, row, data, buy_price)
            column = Tools.add_price_item(self.tblStockList, data['high'].iloc[1:].max(), buy_price, row, column)
            column = Tools.add_price_item(self.tblStockList, data['low'].iloc[1:].min(), buy_price, row, column)

            strategy = "选股失败，买入后连续下跌"
            best_earning_per_day = -10
            transaction_finished = False
            for day in range(2, self.spbMaxHoldTime.value()):
                # 最大持仓时间超过回测时间
                if data.shape[0] < day:
                    break
                # 计算截止当日总盈亏
                high_performance = (data['high'].iloc[day] - buy_price) / buy_price * 100
                low_performance = (data['low'].iloc[day] - buy_price) / buy_price * 100
                # 触发止损割肉
                if low_performance < -self.spbLoseThreshold.value():
                    strategy = "持股" + str(day) + "日触发止损，割肉离场"
                    transaction_finished = True
                    break

                # 达到止盈点，获利了结
                if high_performance > self.spbWinThreshold.value():
                    strategy = "持股" + str(day) + "日触发止盈，获利了结"
                    transaction_finished = True
                    break

                # 计算日化单利
                earning_per_day = high_performance / day
                # 发现更优持仓时间
                if earning_per_day > best_earning_per_day:
                    best_earning_per_day = earning_per_day
                    strategy = "持股" + str(day - 1) + "日, 日化单利" + str(round(best_earning_per_day, 2)) + "%"
            # 若日化单利过低
            if not transaction_finished and 0 < best_earning_per_day < 0.5:
                strategy = "选股失败，长期横盘获利太少"
            self.tblStockList.setItem(row, column, QTableWidgetItem(strategy))

    # 计算X日后的股价表现
    def get_day_performance(self, days: int, column: int, row: int, data: pandas.DataFrame, initial_price: float):
        if data.shape[0] >= days or days == -1:
            performance = round(data['close'].iloc[days], 2)
            Tools.add_price_item(self.tblStockList, performance, initial_price, row, column)
        return column + 1

