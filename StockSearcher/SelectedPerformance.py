from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView
from QtDesign.SelectedPerformance_ui import Ui_SelectedPerformance
import StockAnalyzer.TradeSimulator as TradeSimulator
import Data.TechnicalAnalysis as TechnicalAnalysis
import Tools, pandas, FileManager


# 选股器回测工具
class SelectedPerformance(QMainWindow, Ui_SelectedPerformance):
    __startDate = ""
    __stockShare = __stockInvestment = __remainingInvestment = __stockReturn = 0

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 初始化日期显示
        self.dteSearchDate.setDate(QDate.currentDate().addMonths(-1))
        self.update_start_date()
        # 为表格自动设置列宽
        self.tblStockList.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    # 读取股票列表（可多选）
    def import_stock_list(self):
        full_data = FileManager.import_multiple_stock_lists()
        for date, codes in full_data.items():
            self.__startDate = date
            for code in codes:
                self.fill_stock_list(code)

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

    # 在东方财富网站打开股票主页
    def open_stock_page(self, row: int, column: int):
        if column > 1:
            return
        code = self.tblStockList.item(row, 0).text()
        Tools.open_stock_page(code)

    # 根据导入的选股列表文件填表
    def fill_stock_list(self, code: str):
        row_count = self.tblStockList.rowCount()
        self.tblStockList.insertRow(row_count)
        # 获取股票名称
        name = Tools.get_stock_name_from_code(code)
        self.tblStockList.setItem(row_count, 0, QTableWidgetItem(code))
        self.tblStockList.setItem(row_count, 1, QTableWidgetItem(name))
        self.tblStockList.setItem(row_count, 2, QTableWidgetItem(self.__startDate))
        self.tblStockList.repaint()

    # 根据日期组件显示更新后台选股日期
    def update_start_date(self):
        self.__startDate = self.dteSearchDate.date().toString('yyyy-MM-dd')

    # 计算X日后的股价表现
    def get_day_performance(self, days: int, column: int, row: int, data: pandas.DataFrame, initial_price: float):
        if data.shape[0] > days or days == -1:
            performance = round(data['close'].iloc[days], 2)
            Tools.add_price_item(self.tblStockList, performance, initial_price, row, column)
        return column + 1

    # 模拟买入股票操作
    def buy_stock(self, trade_price: float, trade_share: int):
        self.__stockShare += trade_share
        investment = trade_price * trade_share
        # 计算买入金额和手续费
        self.__stockInvestment += investment + TradeSimulator.buy_transaction_fee(investment)
        self.__remainingInvestment += investment

    # 模拟卖出股票操作
    def sell_stock(self, trade_price: float, trade_share: int):
        self.__stockShare -= trade_share
        revenue = trade_price * trade_share
        # 计算卖出回报，扣除手续费
        self.__stockReturn += revenue - TradeSimulator.sell_transaction_fee(revenue)
        self.__remainingInvestment -= revenue

    # 开始回测
    def start_trade_simulation(self):
        # 初始化所有股票模拟交易数据
        total_spent = total_profit = win_stocks = 0
        # 遍历选到的每只股票
        for row in range(self.tblStockList.rowCount()):
            # 初始化股票交易记录
            self.__stockInvestment = self.__stockReturn = self.__stockShare = self.__remainingInvestment = 0
            # 从表格中获取股票代码
            stock_code = self.tblStockList.item(row, 0).text()
            # 从表格中读取开始时间
            start_date = self.tblStockList.item(row, 2).text()
            # 获取股票历史K线数据
            data = FileManager.read_stock_history_data(stock_code, True)
            # 截取回测日期内的数据
            data = data.loc[start_date:].head(self.spbMaxHoldTime.value() + 1)
            # 最大持仓时间超过回测时间
            if data.shape[0] <= self.spbMaxHoldTime.value():
                continue
            # 选股日收盘价
            initial_price = round(data['close'].iloc[0], 2)
            column = Tools.add_price_item(self.tblStockList, initial_price, data['preclose'].iloc[0], row, 3)
            # 次日开盘买入价
            buy_price = round(data['open'].iloc[1], 2)
            # 计算买入股数，至少买入100股
            share_per_trade = max(round(self.spbMoneyPerTrade.value() / (buy_price * 100)), 1) * 100
            # 次日开盘买入股票
            self.buy_stock(buy_price, share_per_trade)
            # 次日开盘买入价
            column = Tools.add_price_item(self.tblStockList, buy_price, initial_price, row, column)
            # 次日收盘表现
            column = self.get_day_performance(1, column, row, data, buy_price)
            # 加仓期满表现
            column = self.get_day_performance(self.spbAddDeadline.value(), column, row, data, buy_price)
            # 清仓期满表现
            column = self.get_day_performance(-1, column, row, data, buy_price)
            # 期间最高涨幅
            column = Tools.add_price_item(self.tblStockList, round(data['high'].iloc[1:].max(), 2), buy_price, row, column)
            # 期间最大回撤
            column = Tools.add_price_item(self.tblStockList, round(data['low'].iloc[1:].min(), 2), buy_price, row, column)

            # 初始化策略文本
            best_strategy = "选股失败，无法盈利"
            actual_behaviour = ""
            # 初始化日均盈利
            best_earning_per_day = 0
            # 初始化加仓和卖出日期
            add_day = 0
            # 遍历选股后每个交易日执行操作
            for day in range(1, self.spbMaxHoldTime.value() + 1):
                # 获取当日最高最低涨跌幅
                high_price = round(data['high'].iloc[day], 2)
                high_percentage = TechnicalAnalysis.get_percentage_from_price(high_price, buy_price)
                low_price = round(data['low'].iloc[day], 2)
                low_percentage = TechnicalAnalysis.get_percentage_from_price(low_price, buy_price)
                open_price = round(data['open'].iloc[day], 2)

                # 在加仓期限之前可以进行加仓
                if day < self.spbAddDeadline.value() and add_day == 0:
                    # 达到补仓点，降低成本
                    if self.cbxAddWhenDown.isChecked() and low_percentage < self.spbAddThresholdDown.value():
                        # 若开盘价低于补仓点，则以开盘价补仓
                        add_price = min(TechnicalAnalysis.get_price_from_percentage(buy_price, self.spbAddThresholdDown.value()), open_price)
                        self.buy_stock(add_price, share_per_trade)
                        add_day = day
                        actual_behaviour = "第" + str(day) + "日下跌补仓，"
                    # 达到加仓点，强势追涨
                    elif self.cbxAddWhenUp.isChecked() and high_percentage > self.spbAddThresholdUp.value():
                        # 若开盘价高于加仓点，则以开盘价加仓
                        add_price = max(TechnicalAnalysis.get_price_from_percentage(buy_price, self.spbAddThresholdUp.value()), open_price)
                        self.buy_stock(add_price, share_per_trade)
                        add_day = day
                        actual_behaviour = "第" + str(day) + "日上涨加仓，"

                # 买入首日无法卖出
                if day > 1:
                    # 计算日化单利
                    earning_per_day = high_percentage / day
                    # 发现更优持仓时间
                    if earning_per_day > best_earning_per_day:
                        best_earning_per_day = earning_per_day
                        best_strategy = "持股" + str(day) + "日, 获利" + str(round(high_percentage, 2)) + "%"

                    if self.__stockShare > 0:
                        # 达到止盈点，获利了结
                        if self.__stockShare * high_price > self.__remainingInvestment + self.spbWinThreshold.value():
                            sell_price = max(open_price, round((self.__remainingInvestment + self.spbWinThreshold.value()) / self.__stockShare, 2))
                            # 当日加仓过，只卖出底仓
                            if add_day == day:
                                self.sell_stock(sell_price, share_per_trade)
                                actual_behaviour += "第" + str(day) + "日止盈卖出一半，"
                            else:
                                self.sell_stock(sell_price, self.__stockShare)
                                actual_behaviour += "第" + str(day) + "日止盈，"
                        # 达到止损点，割肉离场
                        elif self.__stockShare * low_price < self.__remainingInvestment + self.spbLoseThreshold.value():
                            sell_price = min(open_price, round((self.__remainingInvestment + self.spbLoseThreshold.value()) / self.__stockShare, 2))
                            if add_day == day:
                                self.sell_stock(sell_price, share_per_trade)
                                actual_behaviour += "第" + str(day) + "日止损卖出一半，"
                            else:
                                self.sell_stock(sell_price, self.__stockShare)
                                actual_behaviour += "第" + str(day) + "日止损，"

                    # 若持股到最后一天，则收盘卖出清算
                    if day == self.spbMaxHoldTime.value() and self.__stockShare > 0:
                        sell_price = round(data['close'].iloc[day], 2)
                        self.sell_stock(sell_price, self.__stockShare)
                        actual_behaviour += "末日卖出，"

            # 计算这只股票的盈利
            final_profit = round(self.__stockReturn - self.__stockInvestment, 2)
            if final_profit > 0:
                win_stocks += 1
            actual_behaviour += ("获利" if final_profit >= 0 else "亏损") + str(final_profit) + "元"
            self.tblStockList.setItem(row, column, QTableWidgetItem(best_strategy))
            column += 1
            self.tblStockList.setItem(row, column, QTableWidgetItem(actual_behaviour))
            # 刷新表格显示
            self.tblStockList.repaint()
            # 计算总和投资与回报
            total_spent += self.__stockInvestment
            total_profit += final_profit
            # 确保有股票被测试，更新底部总获利文字显示
            if total_spent > 0:
                profit_text = ("获利" if total_profit >= 0 else "亏损") + str(round(total_profit, 2))
                self.lblTradeSummary.setText("共买入{}只股票，盈利{}只，成本{}元，{}元，收益率{}%"
                                             .format(row + 1, win_stocks, round(total_spent, 2), profit_text, round(total_profit / total_spent * 100, 2)))

