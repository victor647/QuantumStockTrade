from Windows.StockAnalyzer import *
from PyQt5.QtWidgets import QDialog, QHeaderView, QTableWidgetItem
from PyQt5.QtGui import QColor
from QtDesign.TradeSimulator_ui import Ui_TradeSimulator
from Data.DataManager import DataManager
from Data.TradeStrategy import TradeStrategy


class TradeSimulator(QDialog, Ui_TradeSimulator):
    stockCode = ""
    tradeStrategy = None
    currentShare = 0
    sellableShare = 0
    initialAsset = 0
    totalMoneySpent = 0
    totalMoneyBack = 0
    totalFeePaid = 0
    totalBuyCount = 0
    successfulBuyCount = 0
    totalSellCount = 0
    successfulSellCount = 0
    totalSameDayTradeCount = 0
    successfulSameDayTradeCount = 0

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def get_trade_strategy(self, trade_strategy, stock_code):
        self.tradeStrategy = trade_strategy
        self.stockCode = stock_code
        DataManager.get_average_price(DataManager.stockDatabase, trade_strategy.averagePricePeriod, trade_strategy.averageVolumePeriod)

    def start_trading(self):
        self.trade_first_day()
        self.trade_by_day()
        self.trade_last_day()
        # 为表格自动设置列宽
        self.tblTradeHistory.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def trade_first_day(self):
        # 获取首个交易日数据
        data = DataManager.stockDatabase[0]
        # 底仓买入价为开盘价
        price = data.open
        # 计算底仓资产折现
        self.initialAsset = round(price * self.tradeStrategy.baseShare, 2)
        self.buy_stock(data, "首次买入", str.replace(data.date[2:], "-", "/") + " 09:30", price, self.tradeStrategy.baseShare)
        self.lblOriginalInvestment.setText("初始成本：" + str(self.initialAsset))

    def trade_by_day(self):
        # 遍历每日历史数据
        for i in range(1, len(DataManager.stockDatabase) - 1):
            # 获取当日可卖股份余额
            self.sellableShare = self.currentShare
            daily_data = DataManager.stockDatabase[i]
            minute_database = []
            # 初始化当日交易记录
            daily_buy_history = []
            daily_sell_history = []
            # 获取当日5分钟K线数据
            DataManager.parse_minute_data(StockAnalyzer.get_minute_data(daily_data.date, self.stockCode).data, minute_database)
            # 获取上一交易日日K线数据
            last_day_data = DataManager.stockDatabase[i - 1]
            # 根据长短均线排列获取基础买卖点偏移
            point_bias = TradeStrategy.long_term_bias(last_day_data)
            # 根据前日收盘价与均线排列获取买卖点乘数
            up_index = TradeStrategy.short_term_index(last_day_data)
            # 获取基础买卖点
            base_buy_point = self.tradeStrategy.buyPoint / up_index
            base_sell_point = self.tradeStrategy.sellPoint * up_index
            # 获取初始买卖点涨跌幅
            current_buy_point = base_buy_point
            current_sell_point = base_sell_point
            # 遍历当日5分钟K线数据
            for minute_data in minute_database:
                # 5分钟最高和最低价与昨日收盘相比涨跌幅
                minute_low = minute_data.low_percentage_minute(daily_data.previousClose)
                minute_high = minute_data.high_percentage_minute(daily_data.previousClose)
                # 加入偏移量后的实际买卖点涨跌幅
                actual_buy_point = current_buy_point + point_bias
                actual_sell_point = current_sell_point + point_bias
                # 价格低于买点，执行买入操作
                if minute_low < actual_buy_point:
                    # 计算买入价格
                    trade_price = daily_data.price_at_percentage(actual_buy_point)
                    if self.buy_stock(daily_data, "被动买入", minute_data.time, trade_price, self.tradeStrategy.sharePerTrade, point_bias, up_index):
                        # 计算下一次买点跌幅
                        current_buy_point += base_buy_point
                        # 记录本次买入，为做T卖出参考
                        if self.tradeStrategy.allowSameDayTrade:
                            daily_buy_history.append(actual_buy_point)

                # 价格高于卖点，执行卖出操作
                if minute_high > actual_sell_point:
                    trade_price = daily_data.price_at_percentage(actual_sell_point)
                    if self.sell_stock(daily_data, "被动卖出", minute_data.time, trade_price, self.tradeStrategy.sharePerTrade, point_bias, up_index):
                        # 计算下一次卖点涨幅
                        current_sell_point += base_sell_point
                        # 记录本次卖出，为做T买回参考
                        if self.tradeStrategy.allowSameDayTrade:
                            daily_sell_history.append(actual_sell_point)

                # 允许做T情况下，判断当前价位可否做T
                if self.tradeStrategy.allowSameDayTrade:
                    # 遍历当日买入记录
                    for history in daily_buy_history:
                        # 计算卖出价的涨跌幅
                        t_sell_point = history + self.tradeStrategy.sameDayProfit
                        # 价格高于做T卖出盈利点，执行卖出操作
                        if minute_high > t_sell_point:
                            # 判断是否有可卖余额，避免出现T+0操作
                            if self.sellableShare >= self.tradeStrategy.sharePerTrade:
                                # 计算做T卖出价格
                                trade_price = daily_data.price_at_percentage(t_sell_point)
                                if self.sell_stock(daily_data, "做T卖出", minute_data.time, trade_price, self.tradeStrategy.sharePerTrade, point_bias, up_index):
                                    # 抵消当日买入记录
                                    daily_buy_history.remove(history)
                                    # 回溯再次买入点价格，跌到该买点会再次买入
                                    current_buy_point -= base_buy_point
                                    # 累计做T次数
                                    self.totalSameDayTradeCount += 1
                                    # 收盘价低于做T卖出价，做T成功
                                    if daily_data.close < trade_price:
                                        self.successfulSameDayTradeCount += 1

                    # 遍历当日卖出记录
                    for history in daily_sell_history:
                        # 计算买回价的涨跌幅
                        t_buy_point = history - self.tradeStrategy.sameDayProfit
                        # 价格低于做T买回盈利点，执行买入操作
                        if minute_low < t_buy_point:
                            # 计算做T买回价格
                            trade_price = daily_data.price_at_percentage(t_buy_point)
                            if self.buy_stock(daily_data, "做T买回", minute_data.time, trade_price, self.tradeStrategy.sharePerTrade, point_bias, up_index):
                                # 抵消当日卖出记录
                                daily_sell_history.remove(history)
                                # 回溯再次卖出点价格，涨到该卖点会再次卖出
                                current_sell_point -= base_sell_point
                                # 累计做T次数
                                self.totalSameDayTradeCount += 1
                                # 收盘价高于做T买回价，做T成功
                                if daily_data.close > trade_price:
                                    self.successfulSameDayTradeCount += 1

    def trade_last_day(self):
        # 获取最后一个交易日数据
        data = DataManager.stockDatabase[-1]
        # 获取最后一个交易日需要买回或者卖出的股份数，保持结束底仓
        last_trade_share = self.tradeStrategy.baseShare - self.currentShare
        if last_trade_share > 0:
            self.buy_stock(data, "末日买入", str.replace(data.date[2:], "-", "/") + " 15:00", data.close, last_trade_share)
        if last_trade_share < 0:
            self.sell_stock(data, "末日卖出", str.replace(data.date[2:], "-", "/") + " 15:00", data.close, -last_trade_share)

        # 汇总数据
        self.lblBuyCount.setText("共买入" + str(self.totalBuyCount) + "次，成功" + str(self.successfulBuyCount) + "次")
        self.lblSellCount.setText("共卖出" + str(self.totalSellCount) + "次，成功" + str(self.successfulSellCount) + "次")
        self.lblSameDayPerformance.setText("共做T " + str(self.totalSameDayTradeCount) + "次，成功" + str(self.successfulSameDayTradeCount) + "次")
        self.lblTotalFee.setText("总手续费：" + str(round(self.totalFeePaid, 2)))
        self.lblFinalAsset.setText("最终资产：" + str(self.net_worth(data.close)))
        self.lblTotalProfit.setText("累计收益：" + str(self.net_profit(data.close)))
        self.lblTotalReturn.setText("盈亏比例：" + str(self.profit_percentage(data.close)) + "%")

    def buy_stock(self, data, action, time, trade_price, trade_share, point_bias=0, up_index=1):
        # 最大买入额度已满，放弃买入
        if self.currentShare >= self.tradeStrategy.maxShare:
            return False
        self.currentShare += trade_share
        money = trade_share * trade_price
        fee = TradeSimulator.buy_fee(money)
        self.totalMoneySpent += money + fee
        self.add_trade_log(data, time, action, trade_price, trade_share, self.currentShare, point_bias, up_index)
        # 累加交易手续费
        self.totalFeePaid += fee
        # 累加买入次数记录
        self.totalBuyCount += 1
        # 收盘价高于买入价，买入成功
        if data.close > trade_price:
            self.successfulBuyCount += 1
        return True

    def sell_stock(self, data, action, time, trade_price, trade_share, point_bias=0, up_index=1):
        # 最小持仓额度已到，放弃卖出
        if self.currentShare <= self.tradeStrategy.minShare:
            return False
        self.currentShare -= trade_share
        self.sellableShare -= trade_share
        money = trade_share * trade_price
        fee = TradeSimulator.sell_fee(money)
        self.totalMoneyBack += money - fee
        self.add_trade_log(data, time, action, trade_price, trade_share, self.currentShare, point_bias, up_index)
        # 累加交易手续费
        self.totalFeePaid += fee
        # 累加卖出次数记录
        self.totalSellCount += 1
        # 收盘价低于卖出价，卖出成功
        if data.close < trade_price:
            self.successfulSellCount += 1
        return True

    @staticmethod
    def buy_fee(money):
        fee = money * 0.00025
        if fee < 5:
            fee = 5
        return round(fee, 2)

    @staticmethod
    def sell_fee(money):
        fee = money * 0.00025
        if fee < 5:
            fee = 5
        return round(fee + money * 0.001, 2)

    def add_trade_log(self, data, time, action, trade_price, trade_share, remaining_share, point_bias, up_index):
        # 获取当前表格总行数
        row_count = self.tblTradeHistory.rowCount()
        # 在表格末尾添加一行新纪录
        self.tblTradeHistory.insertRow(row_count)
        column = 0
        # 交易时间
        self.tblTradeHistory.setItem(row_count, column, QTableWidgetItem(DataManager.parse_time(time)))
        column += 1
        # 操作
        self.tblTradeHistory.setItem(row_count, column, QTableWidgetItem(action))
        column += 1
        # 成交价格
        self.add_price_item(data, trade_price, row_count, column)
        column += 1
        # 成交股数
        self.tblTradeHistory.setItem(row_count, column, QTableWidgetItem(str(trade_share)))
        column += 1
        # 持仓股数
        self.tblTradeHistory.setItem(row_count, column, QTableWidgetItem(str(remaining_share)))
        column += 1
        # 开盘
        self.add_price_item(data, data.open, row_count, column)
        column += 1
        # 最高
        self.add_price_item(data, data.high, row_count, column)
        column += 1
        # 最低
        self.add_price_item(data, data.low, row_count, column)
        column += 1
        # 收盘
        self.add_price_item(data, data.close, row_count, column)
        column += 1
        # 五日均线
        self.tblTradeHistory.setItem(row_count, column, QTableWidgetItem(str(data.averagePriceFive)))
        column += 1
        # 换手率
        self.tblTradeHistory.setItem(row_count, column, QTableWidgetItem(str(data.turn) + "%"))
        column += 1
        # 长线偏移
        self.add_colored_item(point_bias, row_count, column, "%")
        column += 1
        # 短线多空
        self.add_colored_item(round((up_index - 1) * 100, 2), row_count, column)
        column += 1
        # 持仓成本
        self.tblTradeHistory.setItem(row_count, column, QTableWidgetItem(str(self.average_cost(data.close))))
        column += 1
        # 累计收益
        self.add_colored_item(self.net_profit(data.close), row_count, column)
        column += 1
        # 盈亏比例
        self.add_colored_item(self.profit_percentage(data.close), row_count, column)

    def add_colored_item(self, text, row_count, column, symbol=""):
        item = QTableWidgetItem(str(text) + symbol)
        item.setForeground(TradeSimulator.get_text_color(text))
        self.tblTradeHistory.setItem(row_count, column, item)

    def add_price_item(self, data, price, row_count, column):
        item = QTableWidgetItem()
        item.setForeground(data.get_text_color(price))
        item.setText(str(price) + " " + str(data.percentage_at_price(price)) + "%")
        self.tblTradeHistory.setItem(row_count, column, item)

    # 将股票涨跌数字转化为红绿颜色
    @staticmethod
    def get_text_color(number):
        if number > 0:
            return QColor(200, 0, 0)
        if number < 0:
            return QColor(0, 128, 0)
        return QColor(0, 0, 0)

    # 累计获利百分比
    def profit_percentage(self, current_price):
        return round(self.net_profit(current_price) / self.initialAsset * 100, 2)

    # 累计获利金额
    def net_profit(self, current_price):
        return round(self.cash_worth() + self.stock_worth(current_price), 2)

    # 股票与现金总资产
    def net_worth(self, current_price):
        return round(self.net_profit(current_price) + self.initialAsset, 2)

    # 现金总资产
    def cash_worth(self):
        return round(self.totalMoneyBack - self.totalMoneySpent, 2)

    # 股票折现总资产
    def stock_worth(self, current_price):
        return round(self.currentShare * current_price, 2)

    # 持仓平均成本
    def average_cost(self, current_price):
        if self.currentShare == 0:
            return 0.00
        return round(current_price - self.net_profit(current_price) / self.currentShare, 2)
