from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView
from QtDesign.SelectedPerformance_ui import Ui_SelectedPerformance
import StockAnalyzer.TradeSimulator as TradeSimulator
import Data.TechnicalAnalysis as TechnicalAnalysis
import baostock, Tools, pandas, FileManager


# 选股器回测工具
class SelectedPerformance(QMainWindow, Ui_SelectedPerformance):
    __startDate = ""

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 初始化日期显示
        self.dteSearchDate.setDate(QDate.currentDate().addMonths(-1))
        self.update_start_date()
        # 为表格自动设置列宽
        self.tblStockList.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    # 导入股票信息
    def import_stock_list(self):
        file, start_date = FileManager.import_stock_list_with_date(self.fill_stock_list)
        # 读取股票列表文件中的日期信息
        date = QDate.fromString(start_date, 'yyyy-MM-dd')
        if date.addDays(self.spbMaxHoldTime.value()) > QDate.currentDate():
            date = QDate.currentDate().addDays(-self.spbMaxHoldTime.value())
        self.dteSearchDate.setDate(date)

    # 导出股票列表
    def export_stock_list(self):
        FileManager.export_stock_list(self.tblStockList)

    # 清空股票列表
    def clear_stock_list(self):
        self.tblStockList.setRowCount(0)

    # 添加股票按钮
    def add_stock_code(self):
        stock_code = Tools.get_stock_code(self.iptStockCode)
        if stock_code == "":
            Tools.show_error_dialog("股票代码或名称无效！")
        else:
            self.fill_stock_list(stock_code)

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
        name = Tools.get_stock_name_from_code(code)
        self.tblStockList.setItem(row_count, 0, QTableWidgetItem(code))
        self.tblStockList.setItem(row_count, 1, QTableWidgetItem(name))
        self.tblStockList.setItem(row_count, 2, QTableWidgetItem(self.__startDate))

    # 根据日期组件显示更新后台选股日期
    def update_start_date(self):
        self.__startDate = self.dteSearchDate.date().toString('yyyy-MM-dd')

    # 获取股票历史数据
    def get_stock_history(self, stock_code: str):
        market = Tools.get_trade_center(stock_code)
        result = baostock.query_history_k_data_plus(code=market + "." + stock_code, fields="date,open,high,low,close,preclose,pctChg",
                                                    start_date=self.__startDate, end_date=QDate.currentDate().toString('yyyy-MM-dd'), frequency="d", adjustflag="2")
        return pandas.DataFrame(result.data, columns=result.fields, dtype=float)

    # 读取多个选股列表回测
    def batch_test_performance(self):
        full_data = FileManager.import_multiple_stock_lists()
        for date, codes in full_data.items():
            self.__startDate = date
            for code in codes:
                self.fill_stock_list(code)

    # 获取列表中股票历史数据
    def start_trade_simulation(self):
        # 初始化所有股票模拟交易数据
        total_investment = total_profit = successful_trade_count = 0
        # 遍历选到的每只股票
        for row in range(self.tblStockList.rowCount()):
            # 从表格中获取股票代码
            stock_code = self.tblStockList.item(row, 0).text()
            # 从表格中读取开始时间
            self.__startDate = self.tblStockList.item(row, 2).text()
            # 获取股票历史K线数据
            data = self.get_stock_history(stock_code)
            # 最大持仓时间超过回测时间
            if self.spbMaxHoldTime.value() > data.shape[0]:
                continue
            # 选股日收盘价
            initial_price = data['close'].iloc[0]
            self.tblStockList.setItem(row, 3, QTableWidgetItem(str(initial_price)))
            # 次日开盘买入价
            buy_price = round(data['open'].iloc[1], 2)
            column = 4
            column = Tools.add_price_item(self.tblStockList, buy_price, initial_price, row, column)
            # 次日收盘表现
            column = self.get_day_performance(1, column, row, data, buy_price)
            # 加仓期满表现
            column = self.get_day_performance(self.spbAddDeadline.value() - 1, column, row, data, buy_price)
            # 清仓期满表现
            column = self.get_day_performance(self.spbMaxHoldTime.value() - 1, column, row, data, buy_price)
            # 最高涨幅
            column = Tools.add_price_item(self.tblStockList, data['high'].iloc[1:].max(), buy_price, row, column)
            # 最大回撤
            column = Tools.add_price_item(self.tblStockList, data['low'].iloc[1:].min(), buy_price, row, column)

            # 计算买入股数，至少买入100股
            share_per_trade = max(round(self.spbMoneyPerTrade.value() / (buy_price * 100)), 1) * 100
            # 计算买入实际市值
            stock_investment = share_per_trade * buy_price
            # 初始化卖出时市值
            stock_return = 0
            # 初始化策略文本
            best_strategy = add_log = ""
            actual_behaviour = "末日卖出，"
            # 初始化日均盈利
            best_earning_per_day = -10
            # 是否提前触发止损或止盈
            sell_early = False
            # 遍历选股后每个交易日执行操作
            for day in range(1, self.spbMaxHoldTime.value()):
                # 获取当日最高最低涨跌幅
                high_performance = TechnicalAnalysis.get_percentage_from_price(data['high'].iloc[day], buy_price)
                low_performance = TechnicalAnalysis.get_percentage_from_price(data['low'].iloc[day], buy_price)

                # 在加仓期限之前可以进行加仓
                if day < self.spbAddDeadline.value() and add_log == "":
                    # 达到补仓点，降低成本
                    if self.cbxAddWhenDown.isChecked() and low_performance < self.spbAddThresholdDown.value():
                        add_log = "第" + str(day) + "日下跌补仓，"
                        stock_investment += share_per_trade * TechnicalAnalysis.get_price_from_percentage(buy_price, self.spbAddThresholdDown.value())
                        continue

                    # 达到加仓点，强势追涨
                    if self.cbxAddWhenUp.isChecked() and high_performance > self.spbAddThresholdUp.value():
                        add_log = "第" + str(day) + "日上涨加仓，"
                        stock_investment += share_per_trade * TechnicalAnalysis.get_price_from_percentage(buy_price, self.spbAddThresholdUp.value())
                        continue

                # 买入首日无法卖出
                if day > 1:
                    # 计算日化单利
                    earning_per_day = high_performance / day
                    # 发现更优持仓时间
                    if earning_per_day > best_earning_per_day:
                        best_earning_per_day = earning_per_day
                        best_strategy = "持股" + str(day) + "日, 获利" + str(round(high_performance, 2)) + "%"

                    # 达到止损点，割肉离场
                    if low_performance < self.spbLoseThreshold.value():
                        actual_behaviour = "第" + str(day) + "日触发止损，"
                        stock_return = share_per_trade * TechnicalAnalysis.get_price_from_percentage(buy_price, self.spbLoseThreshold.value())
                        if add_log != "":
                            stock_return *= 2
                        sell_early = True

                    # 达到止盈点，获利了结
                    if high_performance > self.spbWinThreshold.value():
                        actual_behaviour = "第" + str(day) + "日触发止盈，"
                        stock_return = share_per_trade * TechnicalAnalysis.get_price_from_percentage(buy_price, self.spbWinThreshold.value())
                        if add_log != "":
                            stock_return *= 2
                        sell_early = True

                    # 若持股到最后一天，则收盘卖出清算
                    if not sell_early and day == self.spbMaxHoldTime.value() - 1:
                        stock_return = share_per_trade * round(data['close'].iloc[day], 2)
                        if add_log != "":
                            stock_return *= 2

            # 计算扣除手续费后的卖出市值
            stock_return -= TradeSimulator.buy_transaction_fee(stock_investment) + TradeSimulator.sell_transaction_fee(stock_return)
            # 计算这只股票的盈利
            final_profit = round(stock_return - stock_investment, 2)
            if final_profit > 0:
                successful_trade_count += 1
            # 买在高位，无法盈利
            if best_earning_per_day < 0:
                best_strategy = "选股失败，无法盈利"
            self.tblStockList.setItem(row, column, QTableWidgetItem(best_strategy))
            column += 1
            actual_behaviour += ("获利" if final_profit >= 0 else "亏损") + str(final_profit) + "元"
            self.tblStockList.setItem(row, column, QTableWidgetItem(add_log + actual_behaviour))
            # 计算总和投资与回报
            total_investment += stock_investment
            total_profit += final_profit
        profit_text = "获利" if total_profit >= 0 else "亏损"
        # 确保有股票被测试
        if total_investment > 0:
            self.lblTradeSummary.setText("共买入{}只股票，其中{}只盈利，总成本{}元，{}{}元，收益率{}%"
                                        .format(self.tblStockList.rowCount(), successful_trade_count, round(total_investment, 2), profit_text, round(total_profit, 2), round(total_profit / total_investment * 100, 2)))

    # 计算X日后的股价表现
    def get_day_performance(self, days: int, column: int, row: int, data: pandas.DataFrame, initial_price: float):
        if data.shape[0] > days or days == -1:
            performance = round(data['close'].iloc[days], 2)
            Tools.add_price_item(self.tblStockList, performance, initial_price, row, column)
        return column + 1
