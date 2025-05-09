from PyQt6.QtWidgets import QDialog, QHeaderView, QTableWidgetItem
from QtDesign.TradeSimulator_ui import Ui_TradeSimulator
from PyQt6.QtCore import Qt, QDate
import Data.TechnicalAnalysis as TA
from Data.HistoryGraph import CandleStickChart
from Data.InvestmentStatus import StockInvestment
import baostock, pandas
from Libraries import Tools


# 长线模拟交易回测
class TradeSimulator(QDialog, Ui_TradeSimulator):
    # 当前是否持有股票
    tradeStartDayIndex = 0
    market = ''
    stockCode = ''
    stockData = None
    stockInvestment = None
    successfulBuyCount = __successfulSellCount = 0
    totalSameDayTradeCount = successfulSameDayTradeCount = 0
    # 当前趋势
    currentTrend = '震荡'
    trends = []
    # 持仓份数
    currentShare = 0

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup_triggers()
        # 为表格自动设置列宽
        self.tblTradeHistory.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        today = QDate.currentDate()
        self.dteEnd.setDate(today)
        self.dteStart.setDate(today.addMonths(-6))

    def setup_triggers(self):
        self.btnStartTrading.clicked.connect(self.start_trading)
        self.btnShowDiagram.clicked.connect(self.show_history_diagram)

    # 开始模拟交易
    def start_trading(self):
        self.reset_data()
        self.get_stock_data()
        TA.get_percentage_data(self.stockData)
        self.analyze_by_day()

    def reset_data(self):
        self.stockInvestment = StockInvestment()
        self.tradeStartDayIndex = 0
        self.stockData = None
        self.currentTrend = '震荡'
        self.trends = []
        self.currentShare = 0
        self.successfulBuyCount = self.__successfulSellCount = 0
        self.totalSameDayTradeCount = self.successfulSameDayTradeCount = 0
        self.tblTradeHistory.setRowCount(0)

    # 获取股票历史K线
    def get_stock_data(self):
        self.stockCode = Tools.get_stock_code(self.iptStockNumber)
        # 获取交易所信息
        self.market, index_code = Tools.get_trade_center_and_index(self.stockCode)
        start_date = self.dteStart.date().addMonths(-6).toString('yyyy-MM-dd')
        end_date = self.dteEnd.date().toString('yyyy-MM-dd')
        # 获取股票历史数据
        bs_result = baostock.query_history_k_data(code=self.market + '.' + self.stockCode, fields='date,open,high,low,close,preclose,pctChg,turn',
                                                  start_date=start_date, end_date=end_date, frequency='d', adjustflag='2')
        self.stockData = pandas.DataFrame(bs_result.data, columns=bs_result.fields, dtype=float)
        # 计算均线
        TA.calculate_ma_curve(self.stockData, self.spbMAPeriodShort.value())
        TA.calculate_ma_curve(self.stockData, self.spbMAPeriodLong.value())
        TA.get_technical_index(self.stockData)

    # 分析每日情况
    def analyze_by_day(self):
        start_date = self.dteStart.date().toString('yyyy-MM-dd')
        total_days = self.stockData.shape[0]
        for day_index in range(total_days):
            # 前期计算均线数据，不进行交易
            if self.stockData.iloc[day_index]['date'] < start_date:
                continue

            # 买入底仓
            if self.tradeStartDayIndex == 0:
                self.start_trade(day_index)
            else:
                # 最后一日清仓
                if day_index == total_days - 1:
                    self.end_trade(day_index)
                else:
                    # 进行每日交易
                    self.daily_trade(day_index)
                    # 根据收盘情况计算趋势
                    if self.currentTrend == '上升':
                        self.check_if_up_trend_end(day_index)
                        self.check_if_down_trend_start(day_index)
                    elif self.currentTrend == '下降':
                        self.check_if_down_trend_end(day_index)
                        self.check_if_up_trend_start(day_index)
                    else:
                        self.check_if_up_trend_start(day_index)
                        self.check_if_down_trend_start(day_index)


            # 更新表格显示
            self.tblTradeHistory.repaint()

    # 判断是否进入上升趋势
    def check_if_up_trend_start(self, day_index: int):
        ma_short_column = 'ma_' + str(self.spbMAPeriodShort.value())
        ma_long_column = 'ma_' + str(self.spbMAPeriodLong.value())
        day_data = self.stockData.iloc[day_index]
        # MACD红柱
        if self.cbxUpTrendStartByMACD.isChecked():
            if day_data['macd_column'] < 0:
                return
        # 连续X日突破长期均线
        if self.cbxUpTrendStartByMAStay.isChecked():
            for i in range(day_index - self.spbUpTrendStartMAStayDays.value() + 1, day_index + 1):
                # 任何一日收盘低于均线，则趋势不成立
                if self.stockData['close'].iloc[i] < self.stockData[ma_long_column].iloc[i]:
                    return
        # 短期均线位于长期均线上方
        if self.cbxUpTrendStartByMACross.isChecked():
            if day_data[ma_short_column] < day_data[ma_long_column]:
                return
        # 短期均线斜率高于阈值
        if self.cbxUpTrendStartByMAShortDiff.isChecked():
            diff = TA.get_percent_change_from_price(day_data[ma_short_column], self.stockData.iloc[day_index - 1][ma_short_column])
            if diff < self.spbUpTrendMAShortDiffRate.value():
                return
        # 长期均线斜率高于阈值
        if self.cbxUpTrendStartByMALongDiff.isChecked():
            diff = TA.get_percent_change_from_price(day_data[ma_long_column], self.stockData.iloc[day_index - 1][ma_long_column])
            if diff < self.spbUpTrendMALongDiffRate.value():
                return
        self.currentTrend = '上升'
        self.trends.append(('上升', day_index - self.tradeStartDayIndex, day_data['close']))

    # 判断是否结束上升趋势
    def check_if_up_trend_end(self, day_index: int):
        day_data = self.stockData.iloc[day_index]
        # 是否结束趋势
        will_end = False
        # 是否符合某个单一条件
        match = True
        # 连续X日MACD缩短
        if self.cbxUpTrendEndByMacd.isChecked():
            macd_data = self.stockData['macd_column']
            for i in range(day_index - self.spbUpTrendEndMACDFallDays.value() + 1, day_index + 1):
                if macd_data.iloc[i - 1] > macd_data.iloc[i]:
                    match = False
                    break
            will_end = match
        match = True
        # 连续X日失守短期均线
        ma_short_column = 'ma_' + str(self.spbMAPeriodShort.value())
        if not will_end and self.cbxUpTrendEndByMaBreak.isChecked():
            for i in range(day_index - self.spbUpTrendEndMABreakDays.value() + 1, day_index + 1):
                if self.stockData['close'].iloc[i] > self.stockData[ma_short_column].iloc[i]:
                    match = False
                    break
            will_end = match
        match = True
        # 连续X日下跌
        if not will_end and self.cbxUpTrendEndByConsecutiveDown.isChecked():
            for i in range(day_index - self.spbUpTrendEndConsecutiveDownDays.value() + 1, day_index + 1):
                if self.stockData['close'].iloc[i - 1] < self.stockData['close'].iloc[i]:
                    match = False
                    break
            will_end = match
        match = True
        # 连续X日不再创新高
        if not will_end and self.cbxUpTrendEndByNoHighAgain.isChecked():
            x_days_ago_high = self.stockData['high'].iloc[day_index - self.spbUpTrendEndNoHighDays.value() + 1]
            after_x_days_ago_high = self.stockData['high'].iloc[day_index - self.spbUpTrendEndNoHighDays.value() + 2:day_index + 1].max()
            if after_x_days_ago_high > x_days_ago_high:
                match = False
            will_end = match
        # 短期均线斜率转负
        if not will_end and self.cbxUpTrendEndByMAShortDiff.isChecked():
            diff = TA.get_percent_change_from_price(day_data[ma_short_column], self.stockData.iloc[day_index - 1][ma_short_column])
            if diff > 0:
                will_end = False
        # 任一条件满足，结束趋势
        if will_end:
            self.currentTrend = '震荡'
            self.trends.append(('震荡', day_index - self.tradeStartDayIndex, day_data['close']))

    # 判断是否进入下降趋势
    def check_if_down_trend_start(self, day_index: int):
        ma_short_column = 'ma_' + str(self.spbMAPeriodShort.value())
        ma_long_column = 'ma_' + str(self.spbMAPeriodLong.value())
        day_data = self.stockData.iloc[day_index]
        # MACD绿柱
        if self.cbxDownTrendStartByMACD.isChecked():
            if day_data['macd_column'] > 0:
                return
        # 连续X日跌破长期均线
        if self.cbxDownTrendStartByMABreak.isChecked():
            for i in range(day_index - self.spbDownTrendStartMABreakDays.value() + 1, day_index + 1):
                # 任何一日收盘高于均线，则趋势不成立
                if self.stockData['close'].iloc[i] > self.stockData[ma_long_column].iloc[i]:
                    return
        # 短期均线位于长期均线下方
        if self.cbxDownTrendStartByMACross.isChecked():
            if day_data[ma_short_column] > day_data[ma_long_column]:
                return
        # 短期均线斜率低于阈值
        if self.cbxDownTrendStartByMAShortDiff.isChecked():
            diff = TA.get_percent_change_from_price(day_data[ma_short_column], self.stockData.iloc[day_index - 1][ma_short_column])
            if diff > self.spbDownTrendMAShortDiffRate.value():
                return
        # 长期均线斜率低于阈值
        if self.cbxDownTrendStartByMALongDiff.isChecked():
            diff = TA.get_percent_change_from_price(day_data[ma_long_column], self.stockData.iloc[day_index - 1][ma_long_column])
            if diff > self.spbDownTrendMALongDiffRate.value():
                return
        self.currentTrend = '下降'
        self.trends.append(('下降', day_index - self.tradeStartDayIndex, day_data['close']))

    # 判断是否结束下降趋势
    def check_if_down_trend_end(self, day_index: int):
        day_data = self.stockData.iloc[day_index]
        # 是否结束趋势
        will_end = False
        # 是否符合某个单一条件
        match = True
        # 连续X日MACD缩短
        if self.cbxDownTrendEndByMacd.isChecked():
            macd_data = self.stockData['macd_column']
            for i in range(day_index - self.spbDownTrendEndMAStayDays.value() + 1, day_index + 1):
                if macd_data.iloc[i - 1] < macd_data.iloc[i]:
                    match = False
                    break
            will_end = match
        match = True
        # 连续X日突破短期均线
        ma_short_column = 'ma_' + str(self.spbMAPeriodShort.value())
        if not will_end and self.cbxDownTrendEndByMAStay.isChecked():
            for i in range(day_index - self.spbDownTrendEndMAStayDays.value() + 1, day_index + 1):
                if self.stockData['close'].iloc[i] < self.stockData[ma_short_column].iloc[i]:
                    match = False
                    break
            will_end = match
        match = True
        # 连续X日上涨
        if not will_end and self.cbxDownTrendEndByConsecutiveUp.isChecked():
            for i in range(day_index - self.spbDownTrendEndConsecutiveUpDays.value() + 1, day_index + 1):
                if self.stockData['close'].iloc[i - 1] > self.stockData['close'].iloc[i]:
                    match = False
                    break
            will_end = match
        match = True
        # 连续X日不再创新低
        if not will_end and self.cbxDownTrendEndByNoLowAgain.isChecked():
            x_days_ago_low = self.stockData['low'].iloc[day_index - self.spbDownTrendEndNoLowDays.value() + 1]
            after_x_days_ago_low = self.stockData['low'].iloc[day_index - self.spbDownTrendEndNoLowDays.value() + 2:day_index + 1].min()
            if after_x_days_ago_low < x_days_ago_low:
                match = False
            will_end = match
        # 短期均线斜率转正
        if not will_end and self.cbxDownTrendEndByMAShortDiff.isChecked():
            diff = TA.get_percent_change_from_price(day_data[ma_short_column], self.stockData.iloc[day_index - 1][ma_short_column])
            if diff < 0:
                will_end = False
        # 任一条件满足，结束趋势
        if will_end:
            self.currentTrend = '震荡'
            self.trends.append(('震荡', day_index - self.tradeStartDayIndex, day_data['close']))

    # 买入底仓
    def start_trade(self, day_index: int):
        # 获取当日数据
        daily_data = self.stockData.iloc[day_index]
        # 开始持股
        self.tradeStartDayIndex = day_index
        # 出现信号当日收盘价买入
        price = round(daily_data['open'], 2)
        trade_time = daily_data['date'] + ' 09:30'
        self.buy_stock(daily_data, '建仓买入', trade_time, price, self.spbMoneyPerTrade.value())

    # 卖出所有仓位
    def end_trade(self, day_index: int):
        daily_data = self.stockData.iloc[day_index]
        self.tradeStartDayIndex = 0
        # 收盘价卖出
        price = round(daily_data['close'], 2)
        time = Tools.reformat_time(daily_data['date'] + ' 15:00')
        current_share = self.stockInvestment.currentShare
        self.stockInvestment.sell_all(price, time[:10])
        self.add_trade_log(daily_data, time, '清仓卖出', price, current_share)

    # 进行每日交易
    def daily_trade(self, day_index: int):
        day_data = self.stockData.iloc[day_index]
        # 初始化当日交易记录
        daily_buy_history = []
        daily_sell_history = []
        # 缓存昨日收盘价和日期
        pre_close = day_data['preclose']
        date = day_data['date']
        # 缓存每次交易的金额
        money = self.spbMoneyPerTrade.value()
        # 获取当日5分钟K线数据
        result = baostock.query_history_k_data(code=self.market + '.' + self.stockCode, fields='time,high,low',
                                               start_date=date, end_date=date, frequency='5', adjustflag='2')
        minute_database = pandas.DataFrame(result.data, columns=result.fields, dtype=float)
        # 计算各个趋势下的买卖点
        if self.currentTrend == '上升':
            buy_point = self.spbUpTrendBuyPoint.value()
            sell_point = self.spbUpTrendSellPoint.value()
            buy_by_percent = self.cbxUpTrendBuyByPercent.isChecked()
            sell_by_percent = self.cbxUpTrendSellByPercent.isChecked()
            same_day_trade = self.cbxUpTrendSameDayTrade.isChecked()
            same_day_profit = self.spbUpTrendSameDayProfit.value()
        elif self.currentTrend == '下降':
            buy_point = self.spbDownTrendBuyPoint.value()
            sell_point = self.spbDownTrendSellPoint.value()
            buy_by_percent = self.cbxDownTrendBuyByPercent.isChecked()
            sell_by_percent = self.cbxDownTrendSellByPercent.isChecked()
            same_day_trade = self.cbxDownTrendSameDayTrade.isChecked()
            same_day_profit = self.spbDownTrendSameDayProfit.value()
        else:
            buy_point = self.spbFlatTrendBuyPoint.value()
            sell_point = self.spbFlatTrendSellPoint.value()
            buy_by_percent = self.cbxFlatTrendBuyByPercent.isChecked()
            sell_by_percent = self.cbxFlatTrendSellByPercent.isChecked()
            same_day_trade = self.cbxFlatTrendSameDayTrade.isChecked()
            same_day_profit = self.spbFlatTrendSameDayProfit.value()
        # 百分比买卖点模式，获取基础买卖价格
        percent_buy_price = TA.get_price_from_percent_change(pre_close, buy_point)
        percent_sell_price = TA.get_price_from_percent_change(pre_close, sell_point)

        # 五日均线买卖点模式，计算前四日收盘均价
        last_four_day_total = self.stockData.iloc[day_index - 5:day_index - 1]['close'].sum()
        # 初始化当日是否交易的数据
        bought = sold = False
        # 遍历当日5分钟K线数据
        for index, minute_data in minute_database.iterrows():
            time = minute_data['time']
            minute_low = minute_data['low']
            minute_high = minute_data['high']
            # 当日还未买过
            if not bought:
                five_day_mean = round((last_four_day_total + minute_low) / 5, 2)
                # 回调五日均线买入
                if self.currentTrend == '上升' and self.cbxUpTrendBuyByMA5.isChecked():
                    if minute_low < five_day_mean:
                        if self.buy_stock(day_data, '回调买入', time, five_day_mean, money):
                            bought = True
                # 超跌偏离五日均线买入
                if self.currentTrend == '下降' and self.cbxDownTrendBuyByMA5.isChecked():
                    buy_price = TA.get_price_from_percent_change(five_day_mean, self.spbDownTrendMA5BuyThreshold.value())
                    if minute_low < buy_price:
                        if self.buy_stock(day_data, '超跌买入', time, buy_price, money):
                            bought = True
                # 穿过布林线下轨买入
                if self.currentTrend == '震荡' and self.cbxFlatTrendBuyByBOLL.isChecked():
                    buy_price = round(day_data['boll_lower'], 2)
                    if minute_low < buy_price:
                        if self.buy_stock(day_data, '探底买入', time, buy_price, money):
                            bought = True

            # 达到跌幅买入
            if not bought and buy_by_percent:
                if minute_low < percent_buy_price:
                    if self.buy_stock(day_data, '回调买入', time, percent_buy_price, money):
                        daily_buy_history.append(percent_buy_price)
                        bought = True

            # 当日还未卖过
            if not sold:
                five_day_mean = round((last_four_day_total + minute_high) / 5, 2)
                # 冲高五日均线卖出
                if self.currentTrend == '下降' and self.cbxDownTrendSellByMA5.isChecked():
                    if minute_high > five_day_mean:
                        if self.sell_stock(day_data, '冲高卖出', time, five_day_mean, money):
                            sold = True
                # 超买偏离五日均线卖出
                if self.currentTrend == '上升' and self.cbxUpTrendSellByMA5.isChecked():
                    sell_price = TA.get_price_from_percent_change(five_day_mean, self.spbUpTrendMA5SellThreshold.value())
                    if minute_high > sell_price:
                        if self.sell_stock(day_data, '超买卖出', time, sell_price, money):
                            sold = True
                # 穿过布林线上轨卖出
                if self.currentTrend == '震荡' and self.cbxFlatTrendBuyByBOLL.isChecked():
                    sell_price = round(day_data['boll_upper'], 2)
                    if minute_high > sell_price:
                        if self.sell_stock(day_data, '触顶卖出', time, sell_price, money):
                            sold = True

            # 达到涨幅卖出
            if not sold and sell_by_percent:
                if minute_high > percent_sell_price:
                    if self.sell_stock(day_data, '冲高卖出', time, percent_sell_price, money):
                        daily_sell_history.append(percent_sell_price)
                        sold = True

            # 允许做T情况下，判断当前价位可否做T
            if same_day_trade:
                # 持仓大于底仓才可做T卖出
                if self.currentShare >= self.spbBaseHolding.value():
                    # 遍历当日买入记录
                    for buy_price in daily_buy_history:
                        # 计算卖出价的涨跌幅
                        sell_price = round(buy_price + same_day_profit / 100 * pre_close, 2)
                        # 价格高于做T卖出盈利点，执行卖出操作
                        if minute_high >= sell_price:
                            if self.sell_stock(day_data, '做T卖出', time, sell_price, money):
                                # 抵消当日买入记录
                                daily_buy_history.remove(buy_price)
                                daily_sell_history.append(sell_price)
                                # 累计做T次数
                                self.totalSameDayTradeCount += 1
                                # 收盘价低于做T卖出价，做T成功
                                if day_data['close'] < sell_price:
                                    self.successfulSameDayTradeCount += 1
                # 持仓小于底仓才可做T买回
                if self.currentShare <= self.spbBaseHolding.value():
                    # 遍历当日卖出记录
                    for sell_price in daily_sell_history:
                        # 计算买回价的涨跌幅
                        buy_price = round(sell_price - same_day_profit / 100 * pre_close, 2)
                        # 价格低于做T买回盈利点，执行买入操作
                        if minute_low < buy_price:
                            if self.buy_stock(day_data, '做T买回', time, buy_price, money):
                                # 抵消当日卖出记录
                                daily_sell_history.remove(sell_price)
                                daily_buy_history.append(buy_price)
                                # 累计做T次数
                                self.totalSameDayTradeCount += 1
                                # 收盘价高于做T买回价，做T成功
                                if day_data['close'] > buy_price:
                                    self.successfulSameDayTradeCount += 1

    # 模拟买入股票操作
    def buy_stock(self, data: pandas.DataFrame, action: str, time: str, price: float, money: int):
        price = round(price, 2)
        available_money = self.spbMaxHolding.value() * self.spbMoneyPerTrade.value() - self.stockInvestment.stock_value(price)
        # 最大买入额度已满，放弃买入
        if available_money < 10000:
            return False
        # 可买入额度小于单次交易额度
        if available_money < self.spbMoneyPerTrade.value():
            money = available_money

        # 修复日期格式
        time = Tools.reformat_time(time)
        # 进行实际买入操作
        share = self.stockInvestment.buy_stock_by_money(price, money, time[:10])
        # 添加交易记录
        self.add_trade_log(data, time, action, price, share)
        # 收盘价高于买入价，买入成功
        if data['close'] > price:
            self.successfulBuyCount += 1
        self.currentShare += 1
        return True

    # 模拟卖出股票操作
    def sell_stock(self, data: pandas.DataFrame, action: str, time: str, price: float, money: int):
        price = round(price, 2)
        available_money = self.stockInvestment.stock_value(price) - self.spbMinHolding.value() * self.spbMoneyPerTrade.value()
        # 最小持仓额度已到，放弃卖出
        if available_money < 10000:
            return False
        # 可卖出额度小于单次交易额度
        if available_money < self.spbMoneyPerTrade.value():
            money = available_money

        # 修复日期格式
        time = Tools.reformat_time(time)
        # 进行实际卖出操作
        share = self.stockInvestment.sell_stock_by_money(price, money, time[:10])
        # 添加交易记录
        self.add_trade_log(data, time, action, price, share)
        # 收盘价低于卖出价，卖出成功
        if data['close'] < price:
            self.__successfulSellCount += 1
        self.currentShare -= 1
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
        self.tblTradeHistory.setItem(row, column, QTableWidgetItem(str(self.stockInvestment.currentShare)))
        column += 1
        # 开盘
        column = Tools.add_price_item(self.tblTradeHistory, row, column, round(data['open'], 2), pre_close)
        # 最高
        column = Tools.add_price_item(self.tblTradeHistory, row, column, round(data['high'], 2), pre_close)
        # 最低
        column = Tools.add_price_item(self.tblTradeHistory, row, column, round(data['low'], 2), pre_close)
        # 收盘
        column = Tools.add_price_item(self.tblTradeHistory, row, column, round(data['close'], 2), pre_close)
        # 股价趋势
        self.tblTradeHistory.setItem(row, column, QTableWidgetItem(self.currentTrend))
        column += 1
        # 平均成本
        self.tblTradeHistory.setItem(row, column, QTableWidgetItem(str(self.stockInvestment.average_cost(data['close']))))
        column += 1
        # 持仓市值
        self.tblTradeHistory.setItem(row, column, QTableWidgetItem(str(self.stockInvestment.stock_value(data['close']))))
        column += 1
        # 累计收益
        column = Tools.add_colored_item(self.tblTradeHistory, row, column, self.stockInvestment.net_profit(data['close']))
        # 盈亏比例
        Tools.add_colored_item(self.tblTradeHistory, row, column, self.stockInvestment.profit_percentage(data['close']), '%')

    # 显示交易记录K线图
    def show_history_diagram(self):
        if self.stockData is None:
            self.get_stock_data()
        # 复制一份以日期作为key的数据
        stock_data = pandas.DataFrame.copy(self.stockData)
        stock_data.set_index('date', inplace=True)
        # 截取开始交易的日期
        start_date = self.dteStart.date().toString('yyyy-MM-dd')
        stock_data = stock_data.loc[start_date:]
        graph = CandleStickChart(stock_data, self.stockCode)
        # 画成交量
        graph.plot_volume()
        # 画MACD和均线
        graph.plot_ma(self.spbMAPeriodLong.value(), Qt.yellow)
        graph.plot_ma(self.spbMAPeriodShort.value(), Qt.white)
        graph.plot_price()
        graph.plot_macd()
        graph.plot_trends(self.trends)
        graph.plot_trade_history(self.stockInvestment)
        graph.exec_()

