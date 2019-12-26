from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView
from QtDesign.SelectedPerformance_ui import Ui_SelectedPerformance
import StockAnalyzer.TradeSimulator as TradeSimulator
from datetime import date
import baostock, Tools, os.path, pandas, FileManager


class SelectedPerformance(QMainWindow, Ui_SelectedPerformance):
    __startDate = ""
    __endDate = ""

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

    def get_stock_history(self, stock_code: str):
        # 获取交易所信息
        market = Tools.get_trade_center(stock_code)
        result = baostock.query_history_k_data_plus(code=market + "." + stock_code, fields="date,open,high,low,close,preclose,pctChg",
                                                    start_date=self.__startDate, end_date=self.__endDate, frequency="d", adjustflag="2")
        return pandas.DataFrame(result.data, columns=result.fields, dtype=float)

    # 获取列表中股票历史数据
    def start_trade_simulation(self):
        self.__startDate = self.dteSearchDate.date().toString('yyyy-MM-dd')
        self.__endDate = QDate.currentDate().toString('yyyy-MM-dd')
        if self.__startDate == self.__endDate:
            Tools.show_error_dialog("回测开始时间不能为当日！")
            return

        # 初始化所有股票模拟交易数据
        total_investment = total_transaction_fee = 0
        # 遍历选到的每只股票
        for row in range(self.tblStockList.rowCount()):
            # 从表格中获取股票代码
            stock_code = self.tblStockList.item(row, 0).text()
            # 获取股票历史K线数据
            data = self.get_stock_history(stock_code)
            # 选股日收盘价
            initial_price = data['close'].iloc[0]
            self.tblStockList.setItem(row, 2, QTableWidgetItem(str(initial_price)))
            # 次日开盘买入价
            buy_price = round(data['open'].iloc[1], 2)
            column = 3
            column = Tools.add_price_item(self.tblStockList, buy_price, initial_price, row, column)
            # 次日收盘表现
            column = self.get_day_performance(1, column, row, data, buy_price)
            # 3日表现
            column = self.get_day_performance(3, column, row, data, buy_price)
            # 5日表现
            column = self.get_day_performance(5, column, row, data, buy_price)
            # 10日表现
            column = self.get_day_performance(10, column, row, data, buy_price)
            # 至今表现
            column = self.get_day_performance(-1, column, row, data, buy_price)
            # 最高涨幅
            column = Tools.add_price_item(self.tblStockList, data['high'].iloc[1:].max(), buy_price, row, column)
            # 最大回撤
            column = Tools.add_price_item(self.tblStockList, data['low'].iloc[1:].min(), buy_price, row, column)

            # 计算买入股数，至少买入100股
            share = round(self.spbMoneyPerTrade.value() / (buy_price * 100)) * 100
            if share == 0:
                share = 100
            # 计算买入实际市值
            stock_investment = share * buy_price
            total_investment += stock_investment
            # 计算买入手续费
            total_transaction_fee += TradeSimulator.buy_transaction_fee(stock_investment)

            strategy = "选股失败，买入后连续下跌"
            add_log = ""
            best_earning_per_day = -10
            transaction_finished = False
            for day in range(2, self.spbMaxHoldTime.value()):
                # 最大持仓时间超过回测时间
                if data.shape[0] < day:
                    break
                # 计算截止当日总盈亏
                high_performance = (data['high'].iloc[day] - buy_price) / buy_price * 100
                low_performance = (data['low'].iloc[day] - buy_price) / buy_price * 100

                # 在补仓期限之前
                if day < self.spbAddDeadline.value():
                    # 达到补仓点，降低成本
                    if low_performance < self.spbDownAddPoint.value():
                        add_log = "持股第" + str(day) + "日下跌补仓，"
                        additional_investment = share * round(buy_price * (1 + self.spbDownAddPoint.value() / 100), 2)
                        total_transaction_fee += TradeSimulator.buy_transaction_fee(additional_investment)
                        stock_investment += additional_investment
                        total_investment += additional_investment
                        continue

                    # 达到加仓点，强势追涨
                    if high_performance > self.spbUpAddPoint.value():
                        add_log = "持股第" + str(day) + "日上涨加仓，"
                        additional_investment = share * round(buy_price * (1 + self.spbUpAddPoint.value() / 100), 2)
                        total_transaction_fee += TradeSimulator.buy_transaction_fee(additional_investment)
                        stock_investment += additional_investment
                        total_investment += additional_investment
                    continue

                # 达到止损点，割肉离场
                if low_performance < self.spbLoseThreshold.value():
                    strategy = "第" + str(day) + "日触发止损，割肉离场"
                    transaction_finished = True
                    break

                # 达到止盈点，获利了结
                if high_performance > self.spbWinThreshold.value():
                    strategy = "第" + str(day) + "日触发止盈，获利了结"
                    transaction_finished = True
                    break

                # 计算日化单利
                earning_per_day = high_performance / day
                # 发现更优持仓时间
                if earning_per_day > best_earning_per_day:
                    best_earning_per_day = earning_per_day
                    strategy = "共" + str(day - 1) + "日, 日化单利" + str(round(best_earning_per_day, 2)) + "%"

            # 若发生加仓行为，添加记录
            if add_log != "":
                strategy = add_log + strategy
            else:
                strategy = "持股" + strategy
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

