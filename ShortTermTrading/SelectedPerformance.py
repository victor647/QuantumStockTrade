from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView, QFileDialog
from QtDesign.SelectedPerformance_ui import Ui_SelectedPerformance
import Data.TechnicalAnalysis as TechnicalAnalysis
from Data.InvestmentStatus import StockInvestment
import pandas
from Tools import Tools, FileManager
from Data.HistoryGraph import HistoryGraph


# 选股器回测工具
class SelectedPerformance(QMainWindow, Ui_SelectedPerformance):
    __startDate = ''

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 初始化日期显示
        self.dteSearchDate.setDate(QDate.currentDate().addMonths(-1))
        self.update_start_date()
        # 为表格自动设置列宽
        self.tblStockList.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.__stockInvestments = {}

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
        if stock_code == '':
            Tools.show_error_dialog('股票代码或名称无效！')
        else:
            self.fill_stock_list(stock_code)

    # 移除一只股票
    def remove_stock_code(self):
        selection = self.tblStockList.selectedIndexes()
        if len(selection) == 0:
            return
        index = selection[0].row()
        self.tblStockList.removeRow(index)

    # 股票详细信息
    def show_stock_graph(self, row: int, column: int):
        code = self.tblStockList.item(row, 0).text()
        # 通过网页打开
        if column < 2:
            Tools.open_stock_page(code)
        # 直接画K线图
        else:
            # 从表格中读取开始时间
            start_date = self.tblStockList.item(row, 2).text()
            # 获取股票历史K线数据
            data = FileManager.read_stock_history_data(code, True)
            # 截取回测日期内的数据
            data = pandas.concat([data.loc[:start_date].iloc[-20:-2], data.loc[start_date:].head(20)])
            graph = HistoryGraph(code, data)
            graph.plot_all_ma_lines()
            graph.plot_price()
            graph.plot_volume()
            graph.plot_trade_history(self.__stockInvestments[code])
            graph.exec_()

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
            Tools.add_price_item(self.tblStockList, row, column, performance, initial_price)
        return column + 1

    # 开始回测
    def start_trade_simulation(self):
        # 初始化所有股票模拟交易数据
        total_spent = total_profit = win_stocks = 0
        # 遍历选到的每只股票
        for row in range(self.tblStockList.rowCount()):
            # 从表格中获取股票代码
            stock_code = self.tblStockList.item(row, 0).text()
            # 初始化股票交易记录
            self.__stockInvestments[stock_code] = StockInvestment()
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
            column = Tools.add_price_item(self.tblStockList, row, 3, initial_price, data['preclose'].iloc[0])
            # 次日开盘买入价
            buy_price = round(data['open'].iloc[1], 2)
            # 计算买入股数，至少买入100股
            share_per_trade = max(round(self.spbMoneyPerTrade.value() / (buy_price * 100)), 1) * 100
            # 次日开盘买入股票
            self.__stockInvestments[stock_code].buy_stock(buy_price, share_per_trade, data.index[1][2:])
            self.__stockInvestments[stock_code].initial_invest()
            # 次日开盘买入价
            column = Tools.add_price_item(self.tblStockList, row, column, buy_price, initial_price)
            # 次日收盘表现
            column = self.get_day_performance(1, column, row, data, buy_price)
            # 加仓期满表现
            column = self.get_day_performance(self.spbAddDeadline.value(), column, row, data, buy_price)
            # 清仓期满表现
            column = self.get_day_performance(-1, column, row, data, buy_price)
            # 期间最高涨幅
            column = Tools.add_price_item(self.tblStockList, row, column, round(data['high'].iloc[1:].max(), 2), buy_price)
            # 期间最大回撤
            column = Tools.add_price_item(self.tblStockList, row, column, round(data['low'].iloc[1:].min(), 2), buy_price)

            # 初始化策略文本
            best_strategy = '选股失败，无法盈利'
            actual_behaviour = ''
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
                if day <= self.spbAddDeadline.value() and add_day == 0:
                    # 达到补仓点，降低成本
                    if self.cbxAddWhenDown.isChecked() and low_percentage < self.spbAddThresholdDown.value():
                        # 若开盘价低于补仓点，则以开盘价补仓
                        add_price = min(TechnicalAnalysis.get_price_from_percentage(buy_price, self.spbAddThresholdDown.value()), open_price)
                        self.__stockInvestments[stock_code].buy_stock(add_price, share_per_trade, data.index[day][2:])
                        add_day = day
                        actual_behaviour = '第' + str(day) + '日下跌补仓，'
                    # 达到加仓点，强势追涨
                    elif self.cbxAddWhenUp.isChecked() and high_percentage > self.spbAddThresholdUp.value():
                        # 若开盘价高于加仓点，则以开盘价加仓
                        add_price = max(TechnicalAnalysis.get_price_from_percentage(buy_price, self.spbAddThresholdUp.value()), open_price)
                        self.__stockInvestments[stock_code].buy_stock(add_price, share_per_trade, data.index[day][2:])
                        add_day = day
                        actual_behaviour = '第' + str(day) + '日上涨加仓，'

                # 买入首日无法卖出
                if day > 1:
                    # 计算日化单利
                    earning_per_day = high_percentage / day
                    # 发现更优持仓时间
                    if earning_per_day > best_earning_per_day:
                        best_earning_per_day = earning_per_day
                        best_strategy = '持股' + str(day) + '日, 获利' + str(round(high_percentage, 2)) + '%'

                    if self.__stockInvestments[stock_code].currentShare > 0:
                        # 达到止盈点，获利了结
                        if self.cbxWinThreshold.isChecked() and self.__stockInvestments[stock_code].net_profit(high_price) > self.spbWinThreshold.value():
                            sell_price = max(open_price, self.__stockInvestments[stock_code].threshold_price(self.spbWinThreshold.value()))
                            self.__stockInvestments[stock_code].sell_all(sell_price, data.index[day][2:])
                            # 当日加仓过，只卖出底仓
                            if add_day == day:
                                actual_behaviour += '第' + str(day) + '日止盈卖出一半，'
                            else:
                                actual_behaviour += '第' + str(day) + '日止盈，'
                        # 达到止损点，割肉离场
                        elif self.cbxLoseThreshold.isChecked() and self.__stockInvestments[stock_code].net_profit(low_price) < self.spbLoseThreshold.value():
                            sell_price = min(open_price, self.__stockInvestments[stock_code].threshold_price(self.spbLoseThreshold.value()))
                            self.__stockInvestments[stock_code].sell_all(sell_price, data.index[day][2:])
                            if add_day == day:
                                actual_behaviour += '第' + str(day) + '日止损卖出一半，'
                            else:
                                actual_behaviour += '第' + str(day) + '日止损，'

                    # 若持股到最后一天，则收盘卖出清算
                    if day == self.spbMaxHoldTime.value() and self.__stockInvestments[stock_code].currentShare > 0:
                        sell_price = round(data['close'].iloc[day], 2)
                        self.__stockInvestments[stock_code].sell_all(sell_price, data.index[day][2:])
                        actual_behaviour += '末日卖出，'

            # 计算这只股票的最终盈利
            final_profit = self.__stockInvestments[stock_code].final_profit()
            if final_profit > 0:
                win_stocks += 1
            actual_behaviour += ('获利' if final_profit >= 0 else '亏损') + str(final_profit) + '元'

            # 按照日化单利排序最佳策略
            column = Tools.add_sortable_item(self.tblStockList, row, column, best_earning_per_day, best_strategy)
            # 按照收益额排序实际操作
            Tools.add_sortable_item(self.tblStockList, row, column, final_profit, actual_behaviour)
            # 刷新表格显示
            self.tblStockList.repaint()
            # 计算总和投资与回报
            total_spent += self.__stockInvestments[stock_code].totalInvestment
            total_profit += final_profit
            # 确保有股票被测试，更新底部总获利文字显示
            if total_spent > 0:
                profit_text = ('获利' if total_profit >= 0 else '亏损') + str(round(total_profit, 2))
                self.lblTradeSummary.setText('共买入{}只股票，盈利{}只，成本{}元，{}元，收益率{}%'
                                             .format(row + 1, win_stocks, round(total_spent, 2), profit_text, round(total_profit / total_spent * 100, 2)))

    # 导出股票交易策略
    def export_trade_strategy(self):
        file_path = QFileDialog.getSaveFileName(directory=FileManager.trade_strategy_path(), filter='JSON(*.json)')
        data = {
            'moneyPerTrade': self.spbMoneyPerTrade.value(),
            'winThresholdOn': self.cbxWinThreshold.isChecked(),
            'winThreshold': self.spbWinThreshold.value(),
            'loseThresholdOn': self.cbxLoseThreshold.isChecked(),
            'loseThreshold': self.spbLoseThreshold.value(),
            'addWhenDown': self.cbxAddWhenDown.isChecked(),
            'addThresholdDown': self.spbAddThresholdDown.value(),
            'addWhenUp': self.cbxAddWhenUp.isChecked(),
            'addThresholdUp': self.spbAddThresholdUp.value(),
            'addDeadline': self.spbAddDeadline.value(),
            'maxHoldTime': self.spbMaxHoldTime.value()
        }
        if file_path[0] != '':
            FileManager.export_config_as_json(data, file_path[0])

    # 导入股票交易策略
    def import_trade_strategy(self):
        file_path = QFileDialog.getOpenFileName(directory=FileManager.trade_strategy_path(), filter='JSON(*.json)')
        if file_path[0] != '':
            data = FileManager.import_json_config(file_path[0])
            if 'moneyPerTrade' not in data:
                Tools.show_error_dialog('选取的配置文件格式不对！')
                return
            self.spbMoneyPerTrade.setValue(data['moneyPerTrade'])
            self.cbxWinThreshold.setChecked(data['winThresholdOn'])
            self.spbWinThreshold.setValue(data['winThreshold'])
            self.cbxLoseThreshold.setChecked(data['loseThresholdOn'])
            self.spbLoseThreshold.setValue(data['loseThreshold'])
            self.cbxAddWhenDown.setChecked(data['addWhenDown'])
            self.spbAddThresholdDown.setValue(data['addThresholdDown'])
            self.cbxAddWhenUp.setChecked(data['addWhenUp'])
            self.spbAddThresholdUp.setValue(data['addThresholdUp'])
            self.spbAddDeadline.setValue(data['addDeadline'])
            self.spbMaxHoldTime.setValue(data['maxHoldTime'])
