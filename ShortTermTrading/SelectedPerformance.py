from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView, QFileDialog
from QtDesign.SelectedPerformance_ui import Ui_SelectedPerformance
import Data.TechnicalAnalysis as TA
from Data.InvestmentStatus import StockInvestment
import pandas
from Tools import Tools, FileManager
from Data.HistoryGraph import CandleStickChart


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
        elif column > 2:
            # 从表格中读取开始时间
            start_date = self.tblStockList.item(row, 2).text()
            # 获取股票历史K线数据
            data = FileManager.read_stock_history_data(code, True)
            # 截取回测日期内的数据
            data = pandas.concat([data.loc[:start_date].iloc[-20:-2], data.loc[start_date:].head(20)])
            graph = CandleStickChart(code, data)
            graph.plot_all_ma_lines()
            graph.plot_price()
            graph.plot_volume()
            graph.plot_trade_history(self.__stockInvestments[code], False)
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
            investment = StockInvestment()
            self.__stockInvestments[stock_code] = investment
            # 从表格中读取开始时间
            start_date = self.tblStockList.item(row, 2).text()
            # 获取股票历史K线数据
            data = FileManager.read_stock_history_data(stock_code, True)
            # 计算均线
            if self.rbnAddByMa.isChecked():
                TA.calculate_ma_curve(data, self.spbAddMaPeriod.value())
            if self.cbxClearByMa.isChecked():
                TA.calculate_ma_curve(data, self.spbClearMaPeriod.value())
            # 截取回测日期后的数据
            data = TA.get_stock_data_after_date(data, start_date)
            # 选股日收盘价
            pre_close = round(data.iloc[0]['preclose'], 2)
            column = Tools.add_sortable_item(self.tblStockList, row, 3, pre_close)
            # 次日开盘买入底仓价格
            base_buy_price = round(data['open'].iloc[0], 2)
            # 次日开盘买入股票
            investment.buy_stock_by_money(base_buy_price, self.spbMoneyPerTrade.value(), data.index[0])
            investment.initial_invest()
            # 次日开盘买入价
            column = Tools.add_price_item(self.tblStockList, row, column, base_buy_price, pre_close)

            # 初始化策略文本
            best_strategy = '选股失败，无法盈利'
            actual_behaviour = ''
            # 初始化日均盈利
            best_earning_per_day = 0
            # 初始化加仓和卖出日期
            add_day = hold_days = 0
            # 遍历选股后每个交易日执行操作
            while True:
                # 至今未达到清仓条件，卖出
                if data.shape[0] <= hold_days:
                    sell_price = data['close'].iloc[-1]
                    investment.sell_all(sell_price, data.index[-1])
                    actual_behaviour += '持股至今被动清仓'
                    break
                # 获取当日最高最低涨跌幅
                high_price = round(data['high'].iloc[hold_days], 2)
                high_percentage = TA.get_percentage_from_price(high_price, base_buy_price)
                low_price = round(data['low'].iloc[hold_days], 2)
                low_percentage = TA.get_percentage_from_price(low_price, base_buy_price)
                open_price = round(data['open'].iloc[hold_days], 2)
                close_price = round(data['close'].iloc[hold_days], 2)
                # 允许加仓
                if not self.rbnNeverAdd.isChecked() and add_day == 0:
                    add_price = 0
                    # 根据涨跌幅补仓
                    if self.rbnAddByPercent.isChecked():
                        # 下跌补仓
                        if low_percentage < self.spbAddPercent.value() < 0:
                            # 若开盘价低于补仓点，则以开盘价补仓
                            add_price = min(TA.get_price_from_percentage(base_buy_price, self.spbAddPercent.value()), open_price)
                            actual_behaviour = '第' + str(hold_days) + '日下跌补仓，'
                        # 上涨追仓
                        if high_percentage > self.spbAddPercent.value() > 0:
                            add_price = max(TA.get_price_from_percentage(base_buy_price, self.spbAddPercent.value()), open_price)
                            actual_behaviour = '第' + str(hold_days) + '日上涨加仓，'
                    # 回踩均线补仓
                    if self.rbnAddByMa.isChecked():
                        ma_price = data.iloc[hold_days - self.spbAddMaPeriod.value():hold_days]['close'].mean()
                        if low_price <= ma_price:
                            add_price = min(low_price, open_price)
                            actual_behaviour = '第' + str(hold_days) + '日回踩均线补仓，'
                    # 发生过补仓行为，进行买入
                    if add_price > 0:
                        add_day = hold_days
                        investment.buy_stock_by_money(add_price, self.spbMoneyPerTrade.value(), data.index[hold_days])

                # 第二个交易日开始可以卖出股票
                if hold_days > 0:
                    # 计算日化单利
                    earning_per_day = high_percentage / hold_days
                    # 发现更优持仓时间
                    if earning_per_day > best_earning_per_day:
                        best_earning_per_day = earning_per_day
                        best_strategy = '持股' + str(hold_days) + '日, 获利' + str(round(high_percentage, 2)) + '%'

                    if self.__stockInvestments[stock_code].currentShare > 0:
                        # 达到止盈点，获利了结
                        if self.cbxClearByEarning.isChecked() and investment.net_profit(high_price) > self.spbClearEarning.value():
                            sell_price = max(open_price, investment.threshold_price(self.spbClearEarning.value()))
                            investment.sell_all(sell_price, data.index[hold_days])
                            # 当日加仓过，只卖出底仓
                            if add_day == hold_days:
                                actual_behaviour += '第' + str(hold_days) + '日止盈卖出底仓，'
                            else:
                                actual_behaviour += '第' + str(hold_days) + '日止盈清仓，'
                                break
                        # 达到止损点，割肉离场
                        elif self.cbxClearByLosing.isChecked() and investment.net_profit(low_price) < self.spbClearLosing.value():
                            sell_price = min(open_price, investment.threshold_price(self.spbClearLosing.value()))
                            investment.sell_all(sell_price, data.index[hold_days])
                            if add_day == hold_days:
                                actual_behaviour += '第' + str(hold_days) + '日止损卖出底仓，'
                            else:
                                actual_behaviour += '第' + str(hold_days) + '日止损清仓，'
                                break
                        # 收盘跌破均线，清仓
                        elif self.cbxClearByMa.isChecked():
                            ma_price = data.iloc[hold_days - self.spbClearMaPeriod.value():hold_days]['close'].mean()
                            if close_price < ma_price:
                                investment.sell_all(close_price, data.index[hold_days])
                                if add_day == hold_days:
                                    actual_behaviour += '第' + str(hold_days) + '日破位卖出底仓，'
                                else:
                                    actual_behaviour += '第' + str(hold_days) + '日跌破均线清仓，'
                                    break
                # 从买入开始的天数
                hold_days += 1

            # 计算这只股票的最终盈利
            if investment.final_profit() > 0:
                win_stocks += 1
                actual_behaviour += '获利' + str(investment.final_profit()) + '元'
            else:
                actual_behaviour += '亏损' + str(investment.final_profit()) + '元'

            # 清仓日期
            column = Tools.add_sortable_item(self.tblStockList, row, column, hold_days)
            # 清仓时涨幅
            column = Tools.add_colored_item(self.tblStockList, row, column, investment.final_profit_percentage(), '%')
            # 期间最高涨幅
            column = Tools.add_price_item(self.tblStockList, row, column, round(data['high'].iloc[1:].max(), 2), base_buy_price)
            # 期间最大回撤
            column = Tools.add_price_item(self.tblStockList, row, column, round(data['low'].iloc[1:].min(), 2), base_buy_price)

            # 按照日化单利排序最佳策略
            column = Tools.add_sortable_item(self.tblStockList, row, column, best_earning_per_day, best_strategy)
            # 按照收益额排序实际操作
            Tools.add_sortable_item(self.tblStockList, row, column, investment.final_profit(), actual_behaviour)
            # 刷新表格显示
            self.tblStockList.repaint()
            # 计算总和投资与回报
            total_spent += investment.totalInvestment
            total_profit += investment.final_profit()
            # 确保有股票被测试，更新底部总获利文字显示
            if investment.totalInvestment > 0:
                profit_text = ('获利' if total_profit >= 0 else '亏损') + str(round(total_profit, 2))
                self.lblTradeSummary.setText('共买入{}只股票，盈利{}只，成本{}元，{}元，收益率{}%'
                                             .format(row + 1, win_stocks, round(total_spent, 2), profit_text, TA.get_profit_percentage(total_profit, total_spent)))

    # 导出股票交易策略
    def export_trade_strategy(self):
        file_path = QFileDialog.getSaveFileName(directory=FileManager.trade_strategy_path(), filter='JSON(*.json)')
        data = {
            'moneyPerTrade': self.spbMoneyPerTrade.value(),
            'neverAdd': self.rbnNeverAdd.isChecked(),
            'addByPercent': self.rbnAddByPercent.isChecked(),
            'addPercent': self.spbAddPercent.value(),
            'addByMa': self.rbnAddByMa.isChecked(),
            'addMaPeriod': self.spbAddMaPeriod.value(),
            'clearByEarning': self.cbxClearByEarning.isChecked(),
            'clearEarning': self.spbClearEarning.value(),
            'clearByLosing': self.cbxClearByLosing.isChecked(),
            'clearLosing': self.spbClearLosing.value(),
            'clearByMa': self.cbxClearByMa.isChecked(),
            'clearMaPeriod': self.spbClearMaPeriod.value()
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
            self.rbnNeverAdd.setChecked(data['neverAdd'])
            self.rbnAddByPercent.setChecked(data['addByPercent'])
            self.spbAddPercent.setValue(data['addPercent'])
            self.rbnAddByMa.setChecked(data['addByMa'])
            self.spbAddMaPeriod.setValue(data['addMaPeriod'])
            self.cbxClearByEarning.setChecked(data['clearByEarning'])
            self.spbClearEarning.setValue(data['clearEarning'])
            self.cbxClearByLosing.setChecked(data['clearByLosing'])
            self.spbClearLosing.setValue(data['clearLosing'])
            self.cbxClearByMa.setChecked(data['clearByMa'])
            self.spbClearMaPeriod.setValue(data['clearMaPeriod'])
