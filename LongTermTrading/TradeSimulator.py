from PyQt5.QtWidgets import QDialog, QHeaderView, QTableWidgetItem
from QtDesign.TradeSimulator_ui import Ui_TradeSimulator
import LongTermTrading.StockAnalyzer as StockAnalyzer
import LongTermTrading.TradeStrategy as TradeStrategy
import Data.TechnicalAnalysis as TechnicalAnalysis
from Data.HistoryGraph import HistoryGraph
from Data.InvestmentStatus import StockInvestment
import baostock, pandas
from Tools import Tools


# 长线模拟交易回测
class TradeSimulator(QDialog, Ui_TradeSimulator):
    __successfulBuyCount = __successfulSellCount = 0
    totalSameDayTradeCount = successfulSameDayTradeCount = 0
    __crossShort = __crossLong = ""
    __trend = "无"

    def __init__(self, stock_code: str, trade_strategy: TradeStrategy):
        super().__init__()
        self.setupUi(self)
        self.__tradeStrategy = trade_strategy
        self.__stockInvestment = StockInvestment()
        # 设置窗口标题
        self.setWindowTitle(stock_code + "模拟交易")
        # 为表格自动设置列宽
        self.tblTradeHistory.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.__stockCode = stock_code

    # 获取多空趋势转变信号
    def get_trend_type(self):
        # MACD交叉
        if StockAnalyzer.instance.rbnMacd.isChecked():
            self.__crossShort = "macd_white"
            self.__crossLong = "macd_yellow"
        # TRIX交叉
        elif StockAnalyzer.instance.rbnTrix.isChecked():
            self.__crossShort = "trix_white"
            self.__crossLong = "trix_yellow"
        # EXPMA交叉
        elif StockAnalyzer.instance.rbnExpma.isChecked():
            self.__crossShort = "expma_white"
            self.__crossLong = "expma_yellow"
        # 均线交叉
        else:
            self.__crossShort = 'ma_' + StockAnalyzer.instance.cbbMaShort.currentText()
            self.__crossLong = 'ma_' + StockAnalyzer.instance.cbbMaLong.currentText()

        stock_initial = StockAnalyzer.stockDatabase.iloc[0]
        if stock_initial[self.__crossShort] > stock_initial[self.__crossLong]:
            self.__trend = "上升"
        if stock_initial[self.__crossShort] < stock_initial[self.__crossLong]:
            self.__trend = "下降"

    # 开始模拟交易
    def start_trading(self):
        self.trade_first_day()
        if self.__tradeStrategy.enableTrend:
            self.get_trend_type()
        # 遍历每日历史数据
        for day_index in range(1, StockAnalyzer.stockDatabase.shape[0] - 1):
            # 获取当日数据
            stock_today = StockAnalyzer.stockDatabase.iloc[day_index]
            # 计算目前股价运行趋势
            if self.__tradeStrategy.enableTrend:
                self.update_trend_status(day_index, stock_today)
            # 获取当日可卖股份余额
            self.normal_trade(stock_today)
            self.trade_by_signal(day_index, stock_today)
            # 更新表格显示
            self.tblTradeHistory.repaint()
        self.trade_last_day()

    # 首日开盘价买入底仓
    def trade_first_day(self):
        # 获取首个交易日数据
        data = StockAnalyzer.stockDatabase.iloc[0]
        price = round(data['open'], 2)
        trade_time = str.replace(data['date'][2:], "-", "/") + " 09:30"
        self.buy_stock(data, "首次买入", trade_time, price, self.__tradeStrategy.initialShare)
        # 得到初始成本
        self.__stockInvestment.initial_invest()
        self.lblOriginalInvestment.setText("初始成本：" + str(self.__stockInvestment.initialAsset))

    # 末日收盘价计算仓位差补齐
    def trade_last_day(self):
        # 获取最后一个交易日数据
        data = StockAnalyzer.stockDatabase.iloc[-1]
        # 获取需要买回或者卖出的股份数，保持结束底仓
        last_trade_share = self.__tradeStrategy.initialShare - self.__stockInvestment.currentShare
        if last_trade_share > 0:
            self.buy_stock(data, "末日买入", str.replace(data['date'][2:], "-", "/") + " 15:00", data['close'], last_trade_share)
        if last_trade_share < 0:
            self.sell_stock(data, "末日卖出", str.replace(data['date'][2:], "-", "/") + " 15:00", data['close'], -last_trade_share)

    # 更新多空趋势情况
    def update_trend_status(self, index: int, stock_today: pandas.DataFrame):
        # 前两天数据不足不改变趋势
        if index < 2:
            return
        # 获得开盘时间
        start_time = str.replace(stock_today['date'][2:], "-", "/") + " 09:30"

        # 根据前两日指标变化计算多空趋势
        stock_after = StockAnalyzer.stockDatabase.iloc[index - 1]
        stock_before = StockAnalyzer.stockDatabase.iloc[index - 2]
        if stock_before[self.__crossShort] < stock_before[self.__crossLong] and stock_after[self.__crossShort] > stock_after[self.__crossLong]:
            self.__trend = "上升"
            # 立刻买入
            if self.__tradeStrategy.trendChangeTradeShare > 0:
                self.buy_stock(stock_today, "抄底买入", start_time, stock_today['open'], self.__tradeStrategy.trendChangeTradeShare, "转为上升趋势")
        if stock_before[self.__crossShort] > stock_before[self.__crossLong] and stock_after[self.__crossShort] < stock_after[self.__crossLong]:
            self.__trend = "下降"
            # 立刻卖出
            if self.__tradeStrategy.trendChangeTradeShare > 0:
                self.sell_stock(stock_today, "见顶卖出", start_time, stock_today['open'], self.__tradeStrategy.trendChangeTradeShare, "转为下降趋势")

    # 普通交易策略
    def normal_trade(self, daily_data: pandas.DataFrame):
        # 初始化当日交易记录
        daily_buy_history = []
        daily_sell_history = []
        # 缓存昨日收盘价和日期
        pre_close = daily_data['preclose']
        date = daily_data['date']
        # 获取当日5分钟K线数据
        market = Tools.get_trade_center(self.__stockCode)
        result = baostock.query_history_k_data(code=market + "." + self.__stockCode, fields="time,high,low",
                                               start_date=date, end_date=date, frequency="5", adjustflag="2")
        minute_database = pandas.DataFrame(result.data, columns=result.fields, dtype=float)

        # 获取基础买卖点涨跌幅
        current_buy_point = self.__tradeStrategy.buyPointBase
        current_sell_point = self.__tradeStrategy.sellPointBase
        # 根据股票运行趋势调整买卖点
        if self.__tradeStrategy.enableTrend:
            if self.__trend == "上升":
                current_buy_point += self.__tradeStrategy.buyPointTrendBias
                current_sell_point += self.__tradeStrategy.sellPointTrendBias
            elif self.__trend == "下降":
                current_buy_point -= self.__tradeStrategy.buyPointTrendBias
                current_sell_point -= self.__tradeStrategy.sellPointTrendBias

        # 遍历当日5分钟K线数据
        for index, minute_data in minute_database.iterrows():
            # 5分钟最高和最低价与昨日收盘相比涨跌幅
            minute_low = TechnicalAnalysis.get_percentage_from_price(minute_data['high'], pre_close)
            minute_high = TechnicalAnalysis.get_percentage_from_price(minute_data['low'], pre_close)
            # 价格低于买点，执行买入操作
            if minute_low < current_buy_point:
                # 确保买入价格高于5分钟最低价
                current_buy_point = min(minute_high, current_buy_point)
                # 计算买入价格
                trade_price = TechnicalAnalysis.get_price_from_percentage(pre_close, current_buy_point)
                if self.buy_stock(daily_data, "被动买入", minute_data['time'], trade_price, self.__tradeStrategy.sharePerTrade, self.__trend):
                    # 记录本次买入，为做T卖出参考
                    if self.__tradeStrategy.allowSameDayTrade:
                        daily_buy_history.append(current_buy_point)
                    # 计算下一次买点跌幅
                    current_buy_point -= self.__tradeStrategy.buyPointStep

            # 价格高于卖点，执行卖出操作
            if minute_high > current_sell_point:
                # 确保卖出价格高于5分钟最高价
                current_sell_point = max(minute_low, current_sell_point)
                trade_price = TechnicalAnalysis.get_price_from_percentage(pre_close, current_sell_point)
                if self.sell_stock(daily_data, "被动卖出", minute_data['time'], trade_price, self.__tradeStrategy.sharePerTrade, self.__trend):
                    # 记录本次卖出，为做T买回参考
                    if self.__tradeStrategy.allowSameDayTrade:
                        daily_sell_history.append(current_sell_point)
                    # 计算下一次卖点涨幅
                    current_sell_point += self.__tradeStrategy.sellPointStep

            # 允许做T情况下，判断当前价位可否做T
            if self.__tradeStrategy.allowSameDayTrade:
                # 遍历当日买入记录
                for history in daily_buy_history:
                    # 计算卖出价的涨跌幅
                    t_sell_point = history + self.__tradeStrategy.sameDayProfit
                    # 价格高于做T卖出盈利点，执行卖出操作
                    if minute_high > t_sell_point:
                        # 计算做T卖出价格
                        trade_price = TechnicalAnalysis.get_price_from_percentage(pre_close, t_sell_point)
                        if self.sell_stock(daily_data, "做T卖出", minute_data['time'], trade_price, self.__tradeStrategy.sharePerTrade):
                            # 抵消当日买入记录
                            daily_buy_history.remove(history)
                            # 回溯再次买入点价格，跌到该买点会再次买入
                            current_buy_point += self.__tradeStrategy.buyPointStep
                            # 累计做T次数
                            self.totalSameDayTradeCount += 1
                            # 收盘价低于做T卖出价，做T成功
                            if daily_data['close'] < trade_price:
                                self.successfulSameDayTradeCount += 1

                # 遍历当日卖出记录
                for history in daily_sell_history:
                    # 计算买回价的涨跌幅
                    t_buy_point = history - self.__tradeStrategy.sameDayProfit
                    # 价格低于做T买回盈利点，执行买入操作
                    if minute_low < t_buy_point:
                        # 计算做T买回价格
                        trade_price = TechnicalAnalysis.get_price_from_percentage(pre_close, t_buy_point)
                        if self.buy_stock(daily_data, "做T买回", minute_data['time'], trade_price, self.__tradeStrategy.sharePerTrade):
                            # 抵消当日卖出记录
                            daily_sell_history.remove(history)
                            # 回溯再次卖出点价格，涨到该卖点会再次卖出
                            current_sell_point -= self.__tradeStrategy.sellPointStep
                            # 累计做T次数
                            self.totalSameDayTradeCount += 1
                            # 收盘价高于做T买回价，做T成功
                            if daily_data['close'] > trade_price:
                                self.successfulSameDayTradeCount += 1

    # 多空信号交易策略
    def trade_by_signal(self, index: int, stock_today: pandas.DataFrame):
        # 获得收盘时间
        end_time = str.replace(stock_today['date'][2:], "-", "/") + " 15:00"
        # 根据前两日指标变化计算多空趋势
        stock_today = StockAnalyzer.stockDatabase.iloc[index]
        net_buy_share = 0
        message = ""
        # KDJ极值信号
        if StockAnalyzer.instance.cbxKdjEnabled.isChecked():
            if stock_today['kdj_j'] < 0:
                net_buy_share += self.__tradeStrategy.signalTradeShare
                message += "KDJ中J<0 "
            if stock_today['kdj_j'] > 100:
                net_buy_share -= self.__tradeStrategy.signalTradeShare
                message += "KDJ中J>100 "
        # BOLL轨道信号
        if StockAnalyzer.instance.cbxBollEnabled.isChecked():
            if stock_today['low'] < stock_today['boll_lower']:
                net_buy_share += self.__tradeStrategy.signalTradeShare
                message += "BOLL下穿下轨 "
            if stock_today['high'] > stock_today['boll_upper']:
                net_buy_share -= self.__tradeStrategy.signalTradeShare
                message += "BOLL上穿上轨 "
        # BIAS极值信号
        if StockAnalyzer.instance.cbxBiasEnabled.isChecked():
            if stock_today['bias_24'] < -self.__tradeStrategy.biasThreshold:
                net_buy_share += self.__tradeStrategy.signalTradeShare
                message += "BIAS < -" + str(self.__tradeStrategy.biasThreshold)
            if stock_today['bias_24'] > self.__tradeStrategy.biasThreshold:
                net_buy_share -= self.__tradeStrategy.signalTradeShare
                message += "BIAS > " + str(self.__tradeStrategy.biasThreshold)

        # 计算当天收盘净买入额执行操作
        if net_buy_share > 0:
            self.buy_stock(stock_today, "超跌买入", end_time, stock_today['close'], net_buy_share, message)
        if net_buy_share < 0:
            self.sell_stock(stock_today, "冲高卖出", end_time, stock_today['close'], -net_buy_share, message)

    # 更新交易记录并计算资产变化
    def update_trade_count(self, data: pandas.DataFrame):
        self.lblBuyCount.setText("共买入" + str(len(self.__stockInvestment.buyTransactions)) + "次，成功" + str(self.__successfulBuyCount) + "次")
        self.lblSellCount.setText("共卖出" + str(len(self.__stockInvestment.sellTransactions)) + "次，成功" + str(self.__successfulSellCount) + "次")
        self.lblSameDayPerformance.setText("共做T " + str(self.totalSameDayTradeCount) + "次，成功" + str(self.successfulSameDayTradeCount) + "次")
        self.lblTotalFee.setText("总手续费：" + str(self.__stockInvestment.totalFee))
        self.lblFinalAsset.setText("最终资产：" + str(self.__stockInvestment.net_worth(data['close'])))
        self.lblTotalProfit.setText("累计收益：" + str(self.__stockInvestment.net_profit(data['close'])))
        self.lblTotalReturn.setText("盈亏比例：" + str(self.__stockInvestment.profit_percentage(data['close'])) + "%")

    # 模拟买入股票操作
    def buy_stock(self, data: pandas.DataFrame, action: str, time: str, price: float, share: int, signal="无"):
        # 最大买入额度已满，放弃买入
        if self.__stockInvestment.currentShare >= self.__tradeStrategy.maxShare:
            return False
        # 准备买入额度超过最大可持仓额度，减少买入额度
        if self.__tradeStrategy.maxShare - self.__stockInvestment.currentShare < share:
            share = self.__tradeStrategy.maxShare - self.__stockInvestment.currentShare
        # 修复日期格式
        time = Tools.reformat_time(time)
        # 进行实际买入操作
        self.__stockInvestment.buy_stock(price, share, time[:8])
        # 添加交易记录
        self.add_trade_log(data, time, action, price, share, signal)
        # 收盘价高于买入价，买入成功
        if data['close'] > price:
            self.__successfulBuyCount += 1
        # 更新交易记录显示
        self.update_trade_count(data)
        return True

    # 模拟卖出股票操作
    def sell_stock(self, data: pandas.DataFrame, action: str, time: str, price: float, share: int, signal="无"):
        # 最小持仓额度已到，放弃卖出
        if self.__stockInvestment.currentShare <= self.__tradeStrategy.minShare:
            return False
        # 准备卖出额度超过最小可持仓额度，减少卖出额度
        if self.__stockInvestment.currentShare - self.__tradeStrategy.minShare < share:
            share = self.__stockInvestment.currentShare - self.__tradeStrategy.minShare
        # 修复日期格式
        time = Tools.reformat_time(time)
        # 进行实际卖出操作
        self.__stockInvestment.sell_stock(price, share, time[:8])
        # 添加交易记录
        self.add_trade_log(data, time, action, price, share, signal)
        # 收盘价低于卖出价，卖出成功
        if data['close'] < price:
            self.__successfulSellCount += 1
        # 更新交易记录显示
        self.update_trade_count(data)
        return True

    # 在表格中添加交易记录
    def add_trade_log(self, data: pandas.DataFrame, time: str, action: str, trade_price: float, trade_share: int, signal: str):
        # 获取当前表格总行数
        row = self.tblTradeHistory.rowCount()
        # 在表格末尾添加一行新纪录
        self.tblTradeHistory.insertRow(row)
        # 缓存昨日收盘价
        pre_close = data['preclose']
        column = 0
        # 交易时间
        self.tblTradeHistory.setItem(row, column, QTableWidgetItem(time))
        column += 1
        # 操作
        self.tblTradeHistory.setItem(row, column, QTableWidgetItem(action))
        column += 1
        # 成交价格
        column = Tools.add_price_item(self.tblTradeHistory, row, column, trade_price, pre_close)
        # 成交股数
        self.tblTradeHistory.setItem(row, column, QTableWidgetItem(str(trade_share)))
        column += 1
        # 持仓股数
        self.tblTradeHistory.setItem(row, column, QTableWidgetItem(str(self.__stockInvestment.currentShare)))
        column += 1
        # 开盘
        column = Tools.add_price_item(self.tblTradeHistory, row, column, round(data['open'], 2), pre_close)
        # 最高
        column = Tools.add_price_item(self.tblTradeHistory, row, column, round(data['high'], 2), pre_close)
        # 最低
        column = Tools.add_price_item(self.tblTradeHistory, row, column, round(data['low'], 2), pre_close)
        # 收盘
        column = Tools.add_price_item(self.tblTradeHistory, row, column, round(data['close'], 2), pre_close)
        # 换手率
        self.tblTradeHistory.setItem(row, column, QTableWidgetItem(str(round(data['turn'], 2)) + "%"))
        column += 1
        # 多空信号
        self.tblTradeHistory.setItem(row, column, QTableWidgetItem(str(signal)))
        column += 1
        # 持仓成本
        self.tblTradeHistory.setItem(row, column, QTableWidgetItem(str(self.__stockInvestment.average_cost(data['close']))))
        column += 1
        # 累计收益
        column = Tools.add_colored_item(self.tblTradeHistory, row, column, self.__stockInvestment.net_profit(data['close']))
        # 盈亏比例
        column = Tools.add_colored_item(self.tblTradeHistory, row, column, self.__stockInvestment.profit_percentage(data['close']), "%")

    # 显示交易记录K线图
    def show_history_diagram(self):
        if self.__tradeStrategy.enableTrend:
            self.get_trend_type()
        # 复制一份以日期作为key的数据
        stock_data = pandas.DataFrame.copy(StockAnalyzer.stockDatabase)
        stock_data.set_index('date', inplace=True)
        graph = HistoryGraph(self.__stockCode, stock_data)
        # 画成交量
        graph.plot_volume()
        # 画布林轨道
        if StockAnalyzer.instance.cbxBollEnabled.isChecked():
            graph.plot_boll()
        # 画趋势线
        if self.__tradeStrategy.enableTrend:
            # 画MACD线
            if StockAnalyzer.instance.rbnMacd.isChecked():
                graph.plot_macd()
            # 画其他趋势线
            else:
                graph.plot_ma_pair(self.__crossShort, self.__crossLong, StockAnalyzer.instance.rbnTrix.isChecked())
        graph.plot_price()
        graph.plot_trade_history(self.__stockInvestment)
        graph.exec_()

