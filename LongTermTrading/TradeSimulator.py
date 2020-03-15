from PyQt5.QtWidgets import QDialog, QHeaderView, QTableWidgetItem
from QtDesign.TradeSimulator_ui import Ui_TradeSimulator
from PyQt5.QtCore import Qt
import Data.TechnicalAnalysis as TechnicalAnalysis
from Data.HistoryGraph import CandleStickChart
from Data.InvestmentStatus import StockInvestment
import baostock, pandas
from Tools import Tools


# 长线模拟交易回测
class TradeSimulator(QDialog, Ui_TradeSimulator):
    # 当前是否持有股票
    __isHolding = False
    __stockCode = ''
    __stockData = None
    __successfulBuyCount = __successfulSellCount = 0
    totalSameDayTradeCount = successfulSameDayTradeCount = 0
    __crossShort = __crossLong = ""
    __trend = "无"

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 为表格自动设置列宽
        self.tblTradeHistory.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.__stockInvestment = StockInvestment()

    # 开始模拟交易
    def start_trading(self):
        self.__stockCode = Tools.get_stock_code(self.iptStockNumber)
        # 获取交易所信息
        market = Tools.get_trade_center(self.__stockCode)
        start_date = self.dteStart.date().toString()
        end_date = self.dteStart.date().toString()
        # 获取股票历史数据
        bs_result = baostock.query_history_k_data(code=market + "." + self.__stockCode, fields="date,open,high,low,close,preclose,pctChg,turn",
                                                  start_date=start_date, end_date=end_date, frequency="d", adjustflag="2")
        self.__stockData = pandas.DataFrame(bs_result.data, columns=bs_result.fields, dtype=float)
        TechnicalAnalysis.get_technical_index(self.__stockData)
        self.analyze_by_day()

    # 分析每日情况
    def analyze_by_day(self):
        self.__isHolding = False
        for day_index in range(self.__stockData.shape[0]):
            # 当前有持仓
            if self.__isHolding:
                self.daily_trade(day_index)
                if self.end_signal_appears(day_index):
                    self.end_trade(day_index)
            elif self.start_signal_appears(day_index):
                self.start_trade(day_index)
            # 更新表格显示
            self.tblTradeHistory.repaint()

    # 出现建仓信号
    def start_signal_appears(self, day_index: int):
        # MACD信号
        if self.rbnStartByMacd.isChecked():
            macd_data = self.__stockData['macd_column']
            for i in range(self.spbMacdStartDays.value()):
                # 任何一日为红色或继续下降，则趋势不成立
                if macd_data.iloc[day_index - i - 1] > macd_data.iloc[day_index - i] or macd_data.iloc[day_index - i - 1] > 0:
                    return False
        else:
            close_data = self.__stockData['close']
            # 均线交叉信号
            if self.rbnStartByMaCross.isChecked():
                ma_long_yesterday = close_data.iloc[day_index - 1 - self.spbMaBuyPeriodLong.value():day_index - 1].mean()
                ma_long_today = close_data.iloc[day_index - self.spbMaBuyPeriodLong.value():day_index].mean()
                ma_short_yesterday = close_data.iloc[day_index - 1 - self.spbMaBuyPeriodShort.value():day_index - 1].mean()
                ma_short_today = close_data.iloc[day_index - 1 - self.spbMaBuyPeriodShort.value():day_index - 1].mean()
                # 未出现金叉，趋势不成立
                if ma_short_today < ma_long_today or ma_short_yesterday > ma_long_yesterday:
                    return False
            # 均线突破信号
            else:
                for i in range(self.spbMaStartStayDays.value()):
                    ma_long = close_data.iloc[day_index - i - self.spbMaBuyPeriodLong.value():day_index - i].mean()
                    # 任何一日收盘低于均线，则趋势不成立
                    if close_data[day_index - i] < ma_long:
                        return False
        return True

    # 出现清仓信号
    def end_signal_appears(self, day_index: int):
        return False

    # 出现建仓信号，买入
    def start_trade(self, day_index: int):
        # 获取当日数据
        daily_data = self.__stockData.iloc[day_index]
        # 开始持股
        self.__isHolding = True
        # 出现信号当日收盘价买入
        price = round(daily_data['close'], 2)
        trade_time = daily_data['date'] + " 15:00"
        self.buy_stock(daily_data, "建仓买入", trade_time, price, self.spbInitialInvestment.value())
        # 得到初始成本
        self.__stockInvestment.initial_invest()
        self.lblOriginalInvestment.setText("初始成本：" + str(self.__stockInvestment.initialAsset))

    # 出现清仓信号，卖出
    def end_trade(self, day_index: int):
        daily_data = self.__stockData.iloc[day_index]
        self.__isHolding = False
        # 收盘价卖出
        price = round(daily_data['close'], 2)
        time = Tools.reformat_time(daily_data['date'] + " 15:00")
        self.add_trade_log(daily_data, time, '清仓卖出', price, self.__stockInvestment.currentShare)
        self.__stockInvestment.sell_all(price, time[:10])

    # 普通交易策略
    def daily_trade(self, day_index: int):
        daily_data = self.__stockData.iloc[day_index]
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

        # 百分比买卖点模式，获取基础买卖价格
        buy_price = TechnicalAnalysis.get_price_from_percentage(pre_close, self.spbBuyPoint.value())
        sell_price = TechnicalAnalysis.get_price_from_percentage(pre_close, self.spbSellPoint.value())
        # 五日均线买卖点模式，计算前四日收盘均价
        last_four_day_total = self.__stockData.iloc[day_index - 5 : day_index - 1]['close'].sum()

        # 遍历当日5分钟K线数据
        for index, minute_data in minute_database.iterrows():
            # 五日均线买点模式计算挂单价,确保今日没交易过
            five_day_mean = (last_four_day_total + minute_data['low']) / 5
            if self.rbnBuyByMa5.isChecked() and buy_price != 0:
                buy_price = TechnicalAnalysis.get_price_from_percentage(five_day_mean, self.spbMa5BuyThreshold.value())
            if self.rbnSellByMa5.isChecked() and sell_price != 9999:
                sell_price = TechnicalAnalysis.get_price_from_percentage(five_day_mean, self.spbMa5SellThreshold.value())

            # 价格达到买点，执行买入操作
            if minute_data['low'] <= buy_price:
                # 确保买入价格高于5分钟最低价
                buy_price = min(minute_data['high'], buy_price)
                if self.buy_stock(daily_data, "回调买入", minute_data['time'], buy_price, self.spbMoneyPerTrade.value()):
                    # 记录本次买入，为做T卖出参考
                    if self.cbxAllowSameDayTradeBuy.isChecked():
                        daily_buy_history.append(buy_price)
                    # 计算下一次买点价格
                    if self.cbxSameDayBuyAgain:
                        buy_price += pre_close * self.spbBuyPoint.value()
                    else:
                        buy_price = 0

            # 价格高于卖点，执行卖出操作
            if minute_data['high'] >= sell_price:
                # 确保卖出价格高于5分钟最高价
                sell_price = max(minute_data['low'], sell_price)
                if self.sell_stock(daily_data, "冲高卖出", minute_data['time'], sell_price, self.spbMoneyPerTrade.value()):
                    # 记录本次卖出，为做T买回参考
                    if self.cbxAllowSameDayTradeSell.isChecked():
                        daily_sell_history.append(sell_price)
                    # 计算下一次卖点
                    if self.cbxSameDayBuyAgain:
                        sell_price += pre_close * self.spbSellPoint.value()
                    else:
                        sell_price = 9999

            # 允许做T情况下，判断当前价位可否做T
            if self.cbxAllowSameDayTradeBuy:
                # 遍历当日买入记录
                for history in daily_buy_history:
                    # 计算卖出价的涨跌幅
                    t_sell_price = history + self.spbSameDayProfitBuy.value() * pre_close
                    # 价格高于做T卖出盈利点，执行卖出操作
                    if minute_data['high'] >= t_sell_price:
                        if self.sell_stock(daily_data, "做T卖出", minute_data['time'], t_sell_price, self.spbMoneyPerTrade.value()):
                            # 抵消当日买入记录
                            daily_buy_history.remove(history)
                            # 回溯再次买入点价格，跌到该买点会再次买入
                            buy_price -= pre_close * self.spbBuyPoint.value()
                            # 累计做T次数
                            self.totalSameDayTradeCount += 1
                            # 收盘价低于做T卖出价，做T成功
                            if daily_data['close'] < t_sell_price:
                                self.successfulSameDayTradeCount += 1
            # 允许做T情况下，判断当前价位可否做T
            if self.cbxAllowSameDayTradeSell:
                # 遍历当日卖出记录
                for history in daily_sell_history:
                    # 计算买回价的涨跌幅
                    t_buy_price = history - self.spbSameDayProfitBuy.value() * pre_close
                    # 价格低于做T买回盈利点，执行买入操作
                    if minute_data['low'] < t_buy_price:
                        if self.buy_stock(daily_data, "做T买回", minute_data['time'], t_buy_price, self.spbMoneyPerTrade.value()):
                            # 抵消当日卖出记录
                            daily_sell_history.remove(history)
                            # 回溯再次卖出点价格，涨到该卖点会再次卖出
                            sell_price -= pre_close * self.spbSellPoint.value()
                            # 累计做T次数
                            self.totalSameDayTradeCount += 1
                            # 收盘价高于做T买回价，做T成功
                            if daily_data['close'] > t_buy_price:
                                self.successfulSameDayTradeCount += 1

    # 更新交易记录并计算资产变化
    def update_trade_count(self, data: pandas.DataFrame):
        self.lblBuyCount.setText("共买入" + str(len(self.__stockInvestment.buyTransactions)) + "次，成功" + str(self.__successfulBuyCount) + "次")
        self.lblSellCount.setText("共卖出" + str(len(self.__stockInvestment.sellTransactions)) + "次，成功" + str(self.__successfulSellCount) + "次")
        self.lblSameDayPerformance.setText("共做T " + str(self.totalSameDayTradeCount) + "次，成功" + str(self.successfulSameDayTradeCount) + "次")
        self.lblTotalFee.setText("总手续费：" + str(self.__stockInvestment.totalFee))
        self.lblFinalAsset.setText("最终资产：" + str(self.__stockInvestment.net_worth(data['close'])))
        self.lblTotalProfit.setText("累计收益：" + str(self.__stockInvestment.net_profit(data['close'])))
        self.lblTotalReturn.setText("盈亏比例：" + str(self.__stockInvestment.profit_percentage_from_init(data['close'])) + "%")

    # 模拟买入股票操作
    def buy_stock(self, data: pandas.DataFrame, action: str, time: str, price: float, money: int):
        available_money = self.spbMaxHolding.value() - self.__stockInvestment.stock_value(price)
        # 最大买入额度已满，放弃买入
        if available_money < 5000:
            return False
        # 可买入额度小于单次交易额度
        if available_money < self.spbMoneyPerTrade.value():
            money = available_money

        # 修复日期格式
        time = Tools.reformat_time(time)
        # 进行实际买入操作
        share = self.__stockInvestment.buy_stock_by_money(price, money, time[:10])
        # 添加交易记录
        self.add_trade_log(data, time, action, price, share)
        # 收盘价高于买入价，买入成功
        if data['close'] > price:
            self.__successfulBuyCount += 1
        # 更新交易记录显示
        self.update_trade_count(data)
        return True

    # 模拟卖出股票操作
    def sell_stock(self, data: pandas.DataFrame, action: str, time: str, price: float, money: int):
        available_money = self.__stockInvestment.stock_value(price) - self.spbMinHolding.value()
        # 最小持仓额度已到，放弃卖出
        if available_money < 5000:
            return False
        # 可卖出额度小于单次交易额度
        if available_money < self.spbMoneyPerTrade.value():
            money = available_money

        # 修复日期格式
        time = Tools.reformat_time(time)
        # 进行实际卖出操作
        share = self.__stockInvestment.sell_stock_by_money(price, money, time[:10])
        # 添加交易记录
        self.add_trade_log(data, time, action, price, share)
        # 收盘价低于卖出价，卖出成功
        if data['close'] < price:
            self.__successfulSellCount += 1
        # 更新交易记录显示
        self.update_trade_count(data)
        return True

    # 在表格中添加交易记录
    def add_trade_log(self, data: pandas.DataFrame, time: str, action: str, trade_price: float, trade_share: int):
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
        # 持仓成本
        self.tblTradeHistory.setItem(row, column, QTableWidgetItem(str(self.__stockInvestment.average_cost(data['close']))))
        column += 1
        # 累计收益
        column = Tools.add_colored_item(self.tblTradeHistory, row, column, self.__stockInvestment.net_profit(data['close']))
        # 盈亏比例
        column = Tools.add_colored_item(self.tblTradeHistory, row, column, self.__stockInvestment.profit_percentage(data['close']), "%")

    # 显示交易记录K线图
    def show_history_diagram(self):
        # 复制一份以日期作为key的数据
        stock_data = pandas.DataFrame.copy(self.__stockData)
        stock_data.set_index('date', inplace=True)
        graph = CandleStickChart(self.__stockCode, stock_data)
        # 画成交量
        graph.plot_volume()      

        # 画趋势线
        if self.rbnStartByMacd.isChecked() or self.rbnEndByMacd.isChecked():
            graph.plot_macd()

        ma5_plotted = False
        if self.rbnBuyByMa5.isChecked() or self.rbnSellByMa5.isChecked():
            graph.plot_ma(5, Qt.white)
            ma5_plotted = True

        if self.rbnStartByMaBreak.isChecked():
            graph.plot_ma(self.spbMaBuyPeriodLong.value(), Qt.magenta)
        elif self.rbnStartByMaCross.isChecked():
            graph.plot_ma(self.spbMaBuyPeriodLong.value(), Qt.magenta)
            if not ma5_plotted or self.spbMaBuyPeriodShort.value() != 5:
                graph.plot_ma(self.spbMaBuyPeriodShort.value(), Qt.yellow)

        if self.rbnEndByMaBreak.isChecked():
            graph.plot_ma(self.spbMaSellPeriodLong.value(), Qt.green)
        elif self.rbnEndByMaCross.isChecked():
            graph.plot_ma(self.spbMaSellPeriodLong.value(), Qt.green)
            if not ma5_plotted or self.spbMaSellPeriodShort.value() != 5:
                graph.plot_ma(self.spbMaSellPeriodShort.value(), Qt.white)

        graph.plot_price()
        graph.plot_trade_history(self.__stockInvestment)
        graph.exec_()

