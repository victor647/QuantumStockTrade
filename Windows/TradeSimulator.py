from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QDialog, QHeaderView, QTableWidgetItem
from QtDesign.TradeSimulator_ui import Ui_TradeSimulator
import Windows.StockAnalyzer as StockAnalyzer
import Data.TradeStrategy as TradeStrategy
import Data.DataAnalyzer as DataAnalyzer
import Tools
import baostock
import pandas


# 计算买入费用
def buy_transaction_fee(money):
    # 券商佣金
    broker_fee = money * 0.00025
    if broker_fee < 5:
        broker_fee = 5
    return round(broker_fee, 2)


# 计算卖出费用
def sell_transaction_fee(money):
    # 券商佣金
    broker_fee = money * 0.00025
    if broker_fee < 5:
        broker_fee = 5
    # 印花税
    tax = money * 0.001
    return round(broker_fee + tax, 2)


# 获取交易规则和股票代码
def get_trade_strategy(trade_strategy, stock_code):
    global tradeStrategyInstance
    tradeStrategyInstance = trade_strategy
    global stockCode
    stockCode = stock_code


tradeSimulatorInstance = None
tradeStrategyInstance = None
stockCode = ""


class TradeSimulator(QDialog, Ui_TradeSimulator):
    currentShare = 0
    sellableShare = 0
    __initialAsset = 0
    __totalMoneySpent = 0
    __totalMoneyBack = 0
    __totalFeePaid = 0
    __totalBuyCount = 0
    __successfulBuyCount = 0
    __totalSellCount = 0
    __successfulSellCount = 0
    totalSameDayTradeCount = 0
    successfulSameDayTradeCount = 0

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        global tradeSimulatorInstance
        tradeSimulatorInstance = self
        # 为表格自动设置列宽
        self.tblTradeHistory.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    # 开始模拟交易
    def start_trading(self):
        self.trade_first_day()
        trade_by_day = TradeByDay()
        trade_by_day.start()

    # 首日开盘价买入底仓
    def trade_first_day(self):
        # 获取首个交易日数据
        data = StockAnalyzer.stockDatabase.iloc[0]
        price = round(data['open'], 2)
        # 计算底仓资产折现
        self.__initialAsset = round(price * tradeStrategyInstance.baseShare, 2)
        trade_time = str.replace(data['date'][2:], "-", "/") + " 09:30"
        self.buy_stock(data, "首次买入", trade_time, price, tradeStrategyInstance.baseShare)
        self.lblOriginalInvestment.setText("初始成本：" + str(self.__initialAsset))

    # 末日收盘价计算仓位差补齐
    def trade_last_day(self):
        # 获取最后一个交易日数据
        data = StockAnalyzer.stockDatabase.iloc[-1]
        # 获取需要买回或者卖出的股份数，保持结束底仓
        last_trade_share = tradeStrategyInstance.baseShare - self.currentShare
        if last_trade_share > 0:
            self.buy_stock(data, "末日买入", str.replace(data['date'][2:], "-", "/") + " 15:00", data['close'], last_trade_share)
        if last_trade_share < 0:
            self.sell_stock(data, "末日卖出", str.replace(data['date'][2:], "-", "/") + " 15:00", data['close'], -last_trade_share)

    # 更新交易记录并计算资产变化
    def update_trade_count(self, data):
        self.lblBuyCount.setText("共买入" + str(self.__totalBuyCount) + "次，成功" + str(self.__successfulBuyCount) + "次")
        self.lblSellCount.setText("共卖出" + str(self.__totalSellCount) + "次，成功" + str(self.__successfulSellCount) + "次")
        self.lblSameDayPerformance.setText("共做T " + str(self.totalSameDayTradeCount) + "次，成功" + str(self.successfulSameDayTradeCount) + "次")
        self.lblTotalFee.setText("总手续费：" + str(round(self.__totalFeePaid, 2)))
        self.lblFinalAsset.setText("最终资产：" + str(self.net_worth(data['close'])))
        self.lblTotalProfit.setText("累计收益：" + str(self.net_profit(data['close'])))
        self.lblTotalReturn.setText("盈亏比例：" + str(self.profit_percentage(data['close'])) + "%")

    # 模拟买入股票操作
    def buy_stock(self, data, action, time, trade_price, trade_share, point_bias=0, up_index=1):
        # 最大买入额度已满，放弃买入
        if self.currentShare >= tradeStrategyInstance.maxShare:
            return False
        self.currentShare += trade_share
        money = trade_share * trade_price
        fee = buy_transaction_fee(money)
        self.__totalMoneySpent += money + fee
        self.add_trade_log(data, time, action, trade_price, trade_share, self.currentShare, point_bias, up_index)
        # 累加交易手续费
        self.__totalFeePaid += fee
        # 累加买入次数记录
        self.__totalBuyCount += 1
        # 收盘价高于买入价，买入成功
        if data['close'] > trade_price:
            self.__successfulBuyCount += 1
        # 更新交易记录显示
        self.update_trade_count(data)
        return True

    # # 模拟卖出股票操作
    def sell_stock(self, data, action, time, trade_price, trade_share, point_bias=0, up_index=1):
        # 最小持仓额度已到，放弃卖出
        if self.currentShare <= tradeStrategyInstance.minShare:
            return False
        self.currentShare -= trade_share
        self.sellableShare -= trade_share
        money = trade_share * trade_price
        fee = sell_transaction_fee(money)
        self.__totalMoneyBack += money - fee
        self.add_trade_log(data, time, action, trade_price, trade_share, self.currentShare, point_bias, up_index)
        # 累加交易手续费
        self.__totalFeePaid += fee
        # 累加卖出次数记录
        self.__totalSellCount += 1
        # 收盘价低于卖出价，卖出成功
        if data['close'] < trade_price:
            self.__successfulSellCount += 1
        # 更新交易记录显示
        self.update_trade_count(data)
        return True

    # 在表格中添加交易记录
    def add_trade_log(self, data, time, action, trade_price, trade_share, remaining_share, point_bias, up_index):
        # 获取当前表格总行数
        row_count = self.tblTradeHistory.rowCount()
        # 在表格末尾添加一行新纪录
        self.tblTradeHistory.insertRow(row_count)
        # 缓存昨日收盘价
        pre_close = data['preclose']
        column = 0
        # 交易时间
        self.tblTradeHistory.setItem(row_count, column, QTableWidgetItem(Tools.reformat_time(time)))
        column += 1
        # 操作
        self.tblTradeHistory.setItem(row_count, column, QTableWidgetItem(action))
        column += 1
        # 成交价格
        Tools.add_price_item(self.tblTradeHistory, trade_price, pre_close, row_count, column)
        column += 1
        # 成交股数
        self.tblTradeHistory.setItem(row_count, column, QTableWidgetItem(str(trade_share)))
        column += 1
        # 持仓股数
        self.tblTradeHistory.setItem(row_count, column, QTableWidgetItem(str(remaining_share)))
        column += 1
        # 开盘
        Tools.add_price_item(self.tblTradeHistory, round(data['open'], 2), pre_close, row_count, column)
        column += 1
        # 最高
        Tools.add_price_item(self.tblTradeHistory, round(data['high'], 2), pre_close, row_count, column)
        column += 1
        # 最低
        Tools.add_price_item(self.tblTradeHistory, round(data['low'], 2), pre_close, row_count, column)
        column += 1
        # 收盘
        Tools.add_price_item(self.tblTradeHistory, round(data['close'], 2), pre_close, row_count, column)
        column += 1
        # 五日均线
        self.tblTradeHistory.setItem(row_count, column, QTableWidgetItem(str(data['avg_price_five'])))
        column += 1
        # 换手率
        self.tblTradeHistory.setItem(row_count, column, QTableWidgetItem(str(round(data['turn'], 2)) + "%"))
        column += 1
        # 长线偏移
        Tools.add_colored_item(self.tblTradeHistory, point_bias, row_count, column, "%")
        column += 1
        # 短线多空
        Tools.add_colored_item(self.tblTradeHistory, round((up_index - 1) * 100, 2), row_count, column)
        column += 1
        # 持仓成本
        self.tblTradeHistory.setItem(row_count, column, QTableWidgetItem(str(self.average_cost(data['close']))))
        column += 1
        # 累计收益
        Tools.add_colored_item(self.tblTradeHistory, self.net_profit(data['close']), row_count, column)
        column += 1
        # 盈亏比例
        Tools.add_colored_item(self.tblTradeHistory, self.profit_percentage(data['close']), row_count, column, "%")

    # 累计获利百分比
    def profit_percentage(self, current_price):
        return round(self.net_profit(current_price) / self.__initialAsset * 100, 2)

    # 累计获利金额
    def net_profit(self, current_price):
        return round(self.cash_worth() + self.stock_worth(current_price), 2)

    # 股票与现金总资产
    def net_worth(self, current_price):
        return round(self.net_profit(current_price) + self.__initialAsset, 2)

    # 现金总资产
    def cash_worth(self):
        return round(self.__totalMoneyBack - self.__totalMoneySpent, 2)

    # 股票折现总资产
    def stock_worth(self, current_price):
        return round(self.currentShare * current_price, 2)

    # 持仓平均成本
    def average_cost(self, current_price):
        if self.currentShare == 0:
            return 0.00
        return round(current_price - self.net_profit(current_price) / self.currentShare, 2)


class TradeByDay(QThread):
    def __init__(self):
        super().__init__()

    def __del__(self):
        self.work = False
        self.terminate()

    def run(self):
        # 遍历每日历史数据
        for i, daily_data in StockAnalyzer.stockDatabase.iterrows():
            # 获取当日可卖股份余额
            tradeSimulatorInstance.sellableShare = tradeSimulatorInstance.currentShare
            # 初始化当日交易记录
            daily_buy_history = []
            daily_sell_history = []
            # 缓存昨日收盘价和日期
            pre_close = daily_data['preclose']
            date = daily_data['date']
            # 获取当日5分钟K线数据
            market = Tools.get_trade_center(stockCode)
            result = baostock.query_history_k_data(code=market + "." + stockCode, fields="time,high,low",
                                                   start_date=date, end_date=date, frequency="5", adjustflag="2")
            minute_database = pandas.DataFrame(result.data, columns=result.fields, dtype=float)
            # 获取上一交易日日K线数据
            yesterday_data = StockAnalyzer.stockDatabase.iloc[i - 1]
            # 根据长短均线排列获取基础买卖点偏移
            point_bias = TradeStrategy.long_term_bias(yesterday_data)
            # 根据前日收盘价与均线排列获取买卖点乘数
            up_index = TradeStrategy.short_term_index(yesterday_data)
            # 获取基础买卖点
            base_buy_point = tradeStrategyInstance.buyPoint / up_index
            base_sell_point = tradeStrategyInstance.sellPoint * up_index
            # 获取初始买卖点涨跌幅
            current_buy_point = base_buy_point
            current_sell_point = base_sell_point
            # 遍历当日5分钟K线数据
            for index, minute_data in minute_database.iterrows():
                # 5分钟最高和最低价与昨日收盘相比涨跌幅
                minute_low = DataAnalyzer.get_percentage_from_price(minute_data['high'], pre_close)
                minute_high = DataAnalyzer.get_percentage_from_price(minute_data['low'], pre_close)
                # 加入偏移量后的实际买卖点涨跌幅
                actual_buy_point = current_buy_point + point_bias
                actual_sell_point = current_sell_point + point_bias
                # 价格低于买点，执行买入操作
                if minute_low < actual_buy_point:
                    # 计算买入价格
                    trade_price = DataAnalyzer.get_price_from_percentage(pre_close, actual_buy_point)
                    if tradeSimulatorInstance.buy_stock(daily_data, "被动买入", minute_data['time'], trade_price, tradeStrategyInstance.sharePerTrade, point_bias, up_index):
                        # 计算下一次买点跌幅
                        current_buy_point += base_buy_point
                        # 记录本次买入，为做T卖出参考
                        if tradeStrategyInstance.allowSameDayTrade:
                            daily_buy_history.append(actual_buy_point)

                # 价格高于卖点，执行卖出操作
                if minute_high > actual_sell_point:
                    trade_price = DataAnalyzer.get_price_from_percentage(pre_close, actual_sell_point)
                    if tradeSimulatorInstance.sell_stock(daily_data, "被动卖出", minute_data['time'], trade_price, tradeStrategyInstance.sharePerTrade, point_bias, up_index):
                        # 计算下一次卖点涨幅
                        current_sell_point += base_sell_point
                        # 记录本次卖出，为做T买回参考
                        if tradeStrategyInstance.allowSameDayTrade:
                            daily_sell_history.append(actual_sell_point)

                # 允许做T情况下，判断当前价位可否做T
                if tradeStrategyInstance.allowSameDayTrade:
                    # 遍历当日买入记录
                    for history in daily_buy_history:
                        # 计算卖出价的涨跌幅
                        t_sell_point = history + tradeStrategyInstance.sameDayProfit
                        # 价格高于做T卖出盈利点，执行卖出操作
                        if minute_high > t_sell_point:
                            # 判断是否有可卖余额，避免出现T+0操作
                            if tradeSimulatorInstance.sellableShare >= tradeStrategyInstance.sharePerTrade:
                                # 计算做T卖出价格
                                trade_price = DataAnalyzer.get_price_from_percentage(pre_close, t_sell_point)
                                if tradeSimulatorInstance.sell_stock(daily_data, "做T卖出", minute_data['time'], trade_price, tradeStrategyInstance.sharePerTrade, point_bias, up_index):
                                    # 抵消当日买入记录
                                    daily_buy_history.remove(history)
                                    # 回溯再次买入点价格，跌到该买点会再次买入
                                    current_buy_point -= base_buy_point
                                    # 累计做T次数
                                    tradeSimulatorInstance.totalSameDayTradeCount += 1
                                    # 收盘价低于做T卖出价，做T成功
                                    if daily_data['close'] < trade_price:
                                        tradeSimulatorInstance.successfulSameDayTradeCount += 1

                    # 遍历当日卖出记录
                    for history in daily_sell_history:
                        # 计算买回价的涨跌幅
                        t_buy_point = history - tradeStrategyInstance.sameDayProfit
                        # 价格低于做T买回盈利点，执行买入操作
                        if minute_low < t_buy_point:
                            # 计算做T买回价格
                            trade_price = DataAnalyzer.get_price_from_percentage(pre_close, t_buy_point)
                            if tradeSimulatorInstance.buy_stock(daily_data, "做T买回", minute_data['time'], trade_price, tradeStrategyInstance.sharePerTrade, point_bias, up_index):
                                # 抵消当日卖出记录
                                daily_sell_history.remove(history)
                                # 回溯再次卖出点价格，涨到该卖点会再次卖出
                                current_sell_point -= base_sell_point
                                # 累计做T次数
                                tradeSimulatorInstance.totalSameDayTradeCount += 1
                                # 收盘价高于做T买回价，做T成功
                                if daily_data['close'] > trade_price:
                                    tradeSimulatorInstance.successfulSameDayTradeCount += 1
        tradeSimulatorInstance.trade_last_day()
