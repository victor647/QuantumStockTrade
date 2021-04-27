from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView, QFileDialog
from QtDesign.FifteenMinTrader_ui import Ui_FifteenMinTrader
import Data.TechnicalAnalysis as TA
from Data.InvestmentStatus import StockInvestment
import pandas
from Tools import Tools, FileManager
import Data.HistoryGraph as HistoryGraph


# 15分钟k线选股交易
class FifteenMinTrader(QMainWindow, Ui_FifteenMinTrader):
    __startDate = ''

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup_triggers()
        # 为表格自动设置列宽
        self.tblStockList.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.__stockInvestments = {}

    def setup_triggers(self):
        self.btnImportStockList.clicked.connect(self.import_stock_list)
        self.btnStartTrading.clicked.connect(self.start_trade_simulation)

    # 读取股票列表（可多选）
    def import_stock_list(self):
        full_data = FileManager.import_multiple_stock_lists()
        for date, codes in full_data.items():
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
        self.update_start_date()
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
        # 编辑选股日期
        if column == 2:
            return
        stock_code = self.tblStockList.item(row, 0).text()
        # 通过网页打开股票资料
        if column < 2:
            Tools.open_stock_page(stock_code)

        # 从表格中读取选股时间
        search_date = self.tblStockList.item(row, 2).text()
        # 大盘K线图
        if column == 10:
            market, index_code = Tools.get_trade_center_and_index(stock_code)
            HistoryGraph.plot_stock_search_and_trade(market + index_code, search_date)
        # 股票K线图
        else:
            HistoryGraph.plot_stock_search_and_trade(stock_code, search_date, 50, 50, self.__stockInvestments[stock_code])

    # 根据导入的选股列表文件填表
    def fill_stock_list(self, code: str):
        name = Tools.get_stock_name_from_code(code)
        if name == '':
            return
        row_count = self.tblStockList.rowCount()
        self.tblStockList.insertRow(row_count)
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
        total_spent = total_profit = win_stocks = total_fee = transaction_count = 0
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
            if self.cbxAddByMa.isChecked():
                TA.calculate_ma_curve(data, self.spbAddMaPeriod.value())
            if self.cbxClearByMa.isChecked():
                TA.calculate_ma_curve(data, self.spbClearMaPeriod.value())
            # 截取回测日期后的数据
            data = TA.get_stock_data_after_date(data, start_date)
            # 选股日收盘价
            pre_close = round(data['preclose'].iloc[0], 2)
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
            hold_days = 0
            add_day = -1
            # 遍历选股后每个交易日执行操作
            while True:
                # 至今未达到清仓条件，卖出
                if data.shape[0] <= hold_days:
                    # 重置日期增加
                    hold_days -= 1
                    sell_price = data['close'].iloc[-1]
                    if investment.sell_all(sell_price, data.index[-1]):
                        actual_behaviour += '被动清仓'
                    else:
                        actual_behaviour += '持有底仓'
                    break
                # 获取当日最高最低涨跌幅
                high_price = round(data['high'].iloc[hold_days], 2)
                low_price = round(data['low'].iloc[hold_days], 2)
                open_price = round(data['open'].iloc[hold_days], 2)
                close_price = round(data['close'].iloc[hold_days], 2)
                # 尚未加仓过，可以进行加仓
                if add_day == -1:
                    add_price = 0
                    # 根据涨跌幅补仓
                    if self.cbxAddByPercent.isChecked():
                        trigger_price = TA.get_price_from_percent_change(base_buy_price, self.spbAddPercent.value())
                        # 下跌补仓
                        if self.spbAddPercent.value() < 0 and low_price <= trigger_price:
                            # 若开盘价低于补仓点，则以开盘价补仓
                            add_price = min(trigger_price, open_price)
                            actual_behaviour = 'D' + str(hold_days + 1) + '下跌补仓，'
                        # 上涨追仓
                        if self.spbAddPercent.value() > 0 and high_price >= trigger_price:
                            add_price = max(trigger_price, open_price)
                            actual_behaviour = 'D' + str(hold_days + 1) + '上涨加仓，'
                    # 回踩均线补仓
                    if self.cbxAddByMa.isChecked():
                        ma_add_period = self.spbAddMaPeriod.value()
                        ma_price = data['ma_' + str(ma_add_period)].iloc[hold_days]
                        # 根据日内涨跌幅调整买入时的均线值
                        ma_price += (ma_price - close_price) / ma_add_period
                        ma_price_from_base = TA.get_percent_change_from_price(ma_price, base_buy_price)
                        # 回踩补仓价格需低于补仓价格上限
                        if low_price <= ma_price and ma_price_from_base < self.spbAddPriceLimit.value():
                            add_price = min(ma_price, open_price)
                            actual_behaviour = 'D' + str(hold_days + 1) + '回踩补仓，'
                    # 发生过补仓行为，进行买入
                    if add_price > 0:
                        add_day = hold_days
                        investment.buy_stock_by_money(add_price, self.spbMoneyPerTrade.value(), data.index[hold_days])

                # 第二个交易日开始可以卖出股票
                if hold_days > 0:
                    # 当日最高价折算收益
                    high_percentage = TA.get_percent_change_from_price(high_price, base_buy_price)
                    # 计算日化单利
                    earning_per_day = high_percentage / hold_days
                    # 发现更优持仓时间
                    if earning_per_day > best_earning_per_day:
                        best_earning_per_day = earning_per_day
                        best_strategy = 'D' + str(hold_days + 1) + '冲高卖出, 获利' + str(round(high_percentage, 2)) + '%'

                    if self.__stockInvestments[stock_code].currentShare > 0:
                        # 达到止盈点，获利了结
                        if self.cbxClearByEarning.isChecked() and investment.net_profit(high_price) > self.spbClearEarning.value():
                            sell_price = max(open_price, investment.threshold_price(self.spbClearEarning.value()))
                            investment.sell_all(sell_price, data.index[hold_days])
                            # 当日加仓过，只卖出底仓
                            if add_day == hold_days:
                                actual_behaviour += 'D' + str(hold_days + 1) + '止盈卖出，'
                            else:
                                actual_behaviour += 'D' + str(hold_days + 1) + '止盈清仓'
                                break
                        # 达到止损点，割肉离场
                        elif self.cbxClearByLosing.isChecked() and investment.net_profit(low_price) < self.spbClearLosing.value():
                            sell_price = min(open_price, investment.threshold_price(self.spbClearLosing.value()))
                            investment.sell_all(sell_price, data.index[hold_days])
                            if add_day == hold_days:
                                actual_behaviour += 'D' + str(hold_days + 1) + '止损卖出，'
                            else:
                                actual_behaviour += 'D' + str(hold_days + 1) + '止损清仓'
                                break
                        # 收盘跌破均线，清仓
                        elif self.cbxClearByMa.isChecked():
                            ma_price = data['ma_' + str(self.spbClearMaPeriod.value())].iloc[hold_days]
                            if close_price < ma_price:
                                investment.sell_all(close_price, data.index[hold_days])
                                if add_day == hold_days:
                                    actual_behaviour += 'D' + str(hold_days + 1) + '破位卖出，'
                                else:
                                    actual_behaviour += 'D' + str(hold_days + 1) + '破位清仓'
                                    break
                # 从买入开始的天数
                hold_days += 1

            # 若获得盈利则记录
            if investment.final_profit() > 0:
                win_stocks += 1
            # 清仓时价格
            final_price = round(data['close'].iloc[hold_days], 2)
            # 持股日数
            hold_days += 1
            column = Tools.add_sortable_item(self.tblStockList, row, column, hold_days, str(hold_days) + '日')
            # 持仓收益
            final_profit = investment.net_profit(final_price)
            column = Tools.add_colored_item(self.tblStockList, row, column, final_profit)
            # 收益率
            column = Tools.add_colored_item(self.tblStockList, row, column, investment.profit_percentage(final_price), '%')
            # 期间最高涨幅
            column = Tools.add_price_item(self.tblStockList, row, column, round(data['high'].iloc[1:hold_days].max(), 2), base_buy_price)
            # 期间最大回撤
            column = Tools.add_price_item(self.tblStockList, row, column, round(data['low'].iloc[1:hold_days].min(), 2), base_buy_price)
            # 获取指数表现
            market, index_code = Tools.get_trade_center_and_index(stock_code)
            if index_code == '000001':
                index_performance = TA.market_performance_by_days('sh000001', start_date, hold_days)
            elif index_code == '399001':
                index_performance = TA.market_performance_by_days('sz399001', start_date, hold_days)
            else:
                index_performance = TA.market_performance_by_days('sz399006', start_date, hold_days)
            stock_total_performance = TA.get_percent_change_from_price(data['close'].iloc[hold_days - 1], data['preclose'].iloc[0])
            # 收盘涨跌幅
            column = Tools.add_colored_item(self.tblStockList, row, column, stock_total_performance, '%')
            # 同期指数表现
            column = Tools.add_colored_item(self.tblStockList, row, column, index_performance, '%')
            # 期间跑赢指数
            market_difference = round(stock_total_performance - index_performance, 2)
            column = Tools.add_colored_item(self.tblStockList, row, column, market_difference, '%')
            # 按照日化单利排序最佳策略
            column = Tools.add_sortable_item(self.tblStockList, row, column, best_earning_per_day, best_strategy)
            # 按照收益额排序实际操作
            Tools.add_sortable_item(self.tblStockList, row, column, investment.final_profit(), actual_behaviour)
            # 刷新表格显示
            self.tblStockList.repaint()
            # 计算总和投资与回报
            transaction_count += investment.transaction_count()
            total_spent += investment.totalInvestment
            total_profit += final_profit
            total_fee += investment.totalFee
            # 确保有股票被测试，更新底部总获利文字显示
            if investment.totalInvestment > 0:
                profit_text = ('获利' if total_profit >= 0 else '亏损') + str(round(total_profit, 2))
                self.lblTradeSummary.setText('共{}只股票盈利，操作{}次，成本{}元，{}元，手续费{}元，收益率{}%'
                                             .format(win_stocks, transaction_count, round(total_spent, 2), profit_text, round(total_fee, 2), TA.get_profit_percentage(total_profit, total_spent)))

    # 导出股票交易策略
    def export_trade_strategy(self):
        file_path = QFileDialog.getSaveFileName(directory=FileManager.trade_strategy_path(), filter='JSON(*.json)')
        data = {
            'moneyPerTrade': self.spbMoneyPerTrade.value(),
            'addByPercent': self.cbxAddByPercent.isChecked(),
            'addPercent': self.spbAddPercent.value(),
            'addByMa': self.cbxAddByMa.isChecked(),
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
            self.cbxAddByPercent.setChecked(data['addByPercent'])
            self.spbAddPercent.setValue(data['addPercent'])
            self.cbxAddByMa.setChecked(data['addByMa'])
            self.spbAddMaPeriod.setValue(data['addMaPeriod'])
            self.cbxClearByEarning.setChecked(data['clearByEarning'])
            self.spbClearEarning.setValue(data['clearEarning'])
            self.cbxClearByLosing.setChecked(data['clearByLosing'])
            self.spbClearLosing.setValue(data['clearLosing'])
            self.cbxClearByMa.setChecked(data['clearByMa'])
            self.spbClearMaPeriod.setValue(data['clearMaPeriod'])
