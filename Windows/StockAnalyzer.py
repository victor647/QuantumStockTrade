import baostock
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMainWindow, QErrorMessage
from QtDesign.StockAnalyzer_ui import Ui_StockAnalyzer
import Windows.TradeSimulator as TradeSimulator
from Data.TradeStrategy import TradeStrategy
import Data.DataAnalyzer as DataAnalyzer
import Tools
import pandas


stockDatabase = None
marketDatabase = None
    

class StockAnalyzer(QMainWindow, Ui_StockAnalyzer):
    __tradeStrategy = TradeStrategy()
    __analysisData = DataAnalyzer.AnalysisData()
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        now = QDate.currentDate()
        start = now.addMonths(-6)
        self.dteStartDate.setDate(start)
        self.dteEndDate.setDate(now)

    def get_history_data(self):
        stock_code = self.iptStockNumber.text()
        market = Tools.get_trade_center(stock_code)

        start_date = self.dteStartDate.text()
        end_date = self.dteEndDate.text()

        result_stock = baostock.query_history_k_data(code=market + "." + stock_code, fields="date,open,high,low,close,preclose,turn",
                                                     start_date=start_date, end_date=end_date, frequency="d", adjustflag="2")
        if len(result_stock.data) == 0:
            error_dialog = QErrorMessage()
            error_dialog.setWindowTitle("错误")
            error_dialog.showMessage("股票代码无效！")
            error_dialog.exec_()
            return

        global stockDatabase
        stockDatabase = pandas.DataFrame(result_stock.data, columns=result_stock.fields, dtype=float)
        DataAnalyzer.analyze_database(stockDatabase)
        DataAnalyzer.get_average_price(stockDatabase, self.spbAveragePeriodPriceLong.value(), self.spbAveragePeriodVolume.value())

        market_code = "000001" if market == "sh" else "399001"
        result_market = baostock.query_history_k_data(code=market + "." + market_code, fields="date,open,high,low,close,preclose,turn",
                                                      start_date=start_date, end_date=end_date, frequency="d", adjustflag="2")
        
        global marketDatabase
        marketDatabase = pandas.DataFrame(result_market.data, columns=result_market.fields, dtype=float)
        DataAnalyzer.analyze_database(marketDatabase)
        self.analyze_data()

    def analyze_data(self):
        self.__analysisData.averageTurn = DataAnalyzer.average_turn(stockDatabase)
        self.__analysisData.averageCloseUp = DataAnalyzer.average_close_when_up(stockDatabase)
        self.__analysisData.averageCloseDown = DataAnalyzer.average_close_when_down(stockDatabase)
        self.__analysisData.averageHigh = DataAnalyzer.average_high(stockDatabase)
        self.__analysisData.averageLow = DataAnalyzer.average_low(stockDatabase)
        self.__analysisData.averageHighWhenUp = DataAnalyzer.average_high_when_up(stockDatabase)
        self.__analysisData.averageLowWhenDown = DataAnalyzer.average_low_when_down(stockDatabase)
        self.__analysisData.averageFullAmp = DataAnalyzer.average_amplitude(stockDatabase)
        self.__analysisData.averageFallback = DataAnalyzer.average_fallback(stockDatabase)
        self.__analysisData.averageBounce = DataAnalyzer.average_bounce(stockDatabase)

        # 个股表现
        self.lblStockIntervalOpen.setText("区间开盘价格：" + str(DataAnalyzer.interval_open_price(stockDatabase)))
        self.lblStockIntervalClose.setText("区间收盘价格：" + str(DataAnalyzer.interval_close_price(stockDatabase)))
        self.lblStockIntervalHigh.setText("区间最高价格：" + str(DataAnalyzer.interval_highest_price(stockDatabase)))
        self.lblStockIntervalLow.setText("区间最低价格：" + str(DataAnalyzer.interval_lowest_price(stockDatabase)))
        self.lblStockIntervalAverage.setText("区间平均价格：" + str(DataAnalyzer.interval_average_price(stockDatabase)))
        self.lblStockIntervalTotal.setText("区间累计涨幅：" + str(DataAnalyzer.interval_total_performance(stockDatabase)) + "%")
        self.lblStockIntervalAveragePoint.setText("平均每日涨幅：" + str(DataAnalyzer.interval_average_performance(stockDatabase)) + "%")
        self.lblStockUpProbability.setText("每日上涨概率：" + str(DataAnalyzer.close_price_up(stockDatabase)) + "%")
        self.lblWinMarket.setText("跑赢大盘日数：" + str(DataAnalyzer.win_market(stockDatabase, marketDatabase)) + "%")
        self.lblInverseMarketUp.setText("逆市上涨日数：" + str(DataAnalyzer.inverse_market_up(stockDatabase, marketDatabase)) + "%")
        self.lblInverseMarketDown.setText("逆市下跌日数：" + str(DataAnalyzer.inverse_market_down(stockDatabase, marketDatabase)) + "%")
        self.lblAverageHigh.setText("平均日内最高：" + str(self.__analysisData.averageHigh) + "%")
        self.lblAverageLow.setText("平均日内最低：" + str(self.__analysisData.averageLow) + "%")
        self.lblAverageCloseUp.setText("阳线平均涨幅：" + str(self.__analysisData.averageCloseUp) + "%")
        self.lblAverageCloseDown.setText("阴线平均跌幅：" + str(self.__analysisData.averageCloseDown) + "%")
        self.lblReachMaxProbability.setText("涨停触板概率：" + str(DataAnalyzer.reach_max_limit(stockDatabase)) + "%")
        self.lblStayMaxProbability.setText("涨停收盘概率：" + str(DataAnalyzer.stay_max_limit(stockDatabase)) + "%")
        self.lblReachMinProbability.setText("跌停触板概率：" + str(DataAnalyzer.reach_min_limit(stockDatabase)) + "%")
        self.lblStayMinProbability.setText("跌停收盘概率：" + str(DataAnalyzer.stay_min_limit(stockDatabase)) + "%")

        # 股性指标
        self.lblAverageTurn.setText("平均换手率：" + str(self.__analysisData.averageTurn) + "%")
        self.lblAverageAmplitude.setText("每日平均振幅：" + str(self.__analysisData.averageFullAmp) + "%")
        self.lblHighOpenHighClose.setText("高开高走概率：" + str(DataAnalyzer.high_open_high_close(stockDatabase)) + "%")
        self.lblHighOpenLowClose.setText("高开低走概率：" + str(DataAnalyzer.high_open_low_close(stockDatabase)) + "%")
        self.lblLowOpenLowClose.setText("低开低走概率：" + str(DataAnalyzer.low_open_low_close(stockDatabase)) + "%")
        self.lblLowOpenHighClose.setText("低开高走概率：" + str(DataAnalyzer.low_open_high_close(stockDatabase)) + "%")
        self.lblAverageHighWhenUp.setText("阳线平均最高：" + str(self.__analysisData.averageHighWhenUp) + "%")
        self.lblAverageFallbackAmp.setText("阳线平均回撤：" + str(self.__analysisData.averageFallback) + "%")
        self.lblAverageLowWhenDown.setText("阴线平均最低：" + str(self.__analysisData.averageLowWhenDown) + "%")
        self.lblAverageBounceAmp.setText("阴线平均反弹：" + str(self.__analysisData.averageBounce) + "%")

        # 大盘表现
        self.lblMarketIntervalOpen.setText("区间开盘点位：" + str(DataAnalyzer.interval_open_price(marketDatabase)))
        self.lblMarketIntervalClose.setText("区间收盘点位：" + str(DataAnalyzer.interval_close_price(marketDatabase)))
        self.lblMarketIntervalHigh.setText("区间最高点位：" + str(DataAnalyzer.interval_highest_price(marketDatabase)))
        self.lblMarketIntervalLow.setText("区间最低点位：" + str(DataAnalyzer.interval_lowest_price(marketDatabase)))
        self.lblMarketIntervalAverage.setText("区间平均点位：" + str(DataAnalyzer.interval_average_price(marketDatabase)))
        self.lblMarketIntervalTotal.setText("区间累计涨幅：" + str(DataAnalyzer.interval_total_performance(marketDatabase)) + "%")
        self.lblMarketIntervalAveragePoint.setText("平均每日涨幅：" + str(DataAnalyzer.interval_average_performance(marketDatabase)) + "%")
        self.lblMarketUpProbability.setText("每日上涨概率：" + str(DataAnalyzer.close_price_up(marketDatabase)) + "%")

    def auto_get_strategy(self):
        if not self.check_stock_data_exist():
            return
        self.__tradeStrategy.auto_get_strategy(self.__analysisData)
        self.spbBuyPoint.setValue(self.__tradeStrategy.buyPoint)
        self.spbSellPoint.setValue(self.__tradeStrategy.sellPoint)
        self.cbxAllowSameDayTrade.setChecked(self.__tradeStrategy.allowSameDayTrade)
        self.spbSameDayProfit.setValue(self.__tradeStrategy.sameDayProfit)

    def start_trade(self):
        if not self.check_stock_data_exist():
            return
        self.__tradeStrategy.buyPoint = self.spbBuyPoint.value()
        self.__tradeStrategy.sellPoint = self.spbSellPoint.value()
        self.__tradeStrategy.allowSameDayTrade = self.cbxAllowSameDayTrade.isChecked()
        self.__tradeStrategy.sameDayProfit = self.spbSameDayProfit.value()
        self.__tradeStrategy.baseShare = self.spbBaseShare.value()
        self.__tradeStrategy.sharePerTrade = self.spbSharePerTrade.value()
        self.__tradeStrategy.maxShare = self.spbMaxShare.value()
        self.__tradeStrategy.minShare = self.spbMinShare.value()
        self.__tradeStrategy.averagePricePeriod = self.spbAveragePeriodPriceLong.value()
        self.__tradeStrategy.averageVolumePeriod = self.spbAveragePeriodVolume.value()
        self.__tradeStrategy.volumeWeight = self.spbVolumeMultiplier.value()
        stock_code = self.iptStockNumber.text()

        trade_window = TradeSimulator.TradeSimulator()
        trade_window.setWindowTitle(stock_code + "模拟交易")
        TradeSimulator.get_trade_strategy(self.__tradeStrategy, stock_code)
        trade_window.show()
        trade_window.start_trading()
        trade_window.exec_()
        return

    def check_stock_data_exist(self):
        if self.__analysisData.averageTurn == 0:
            error_dialog = QErrorMessage()
            error_dialog.setWindowTitle("错误")
            error_dialog.showMessage("请先获取股票历史数据！")
            error_dialog.exec_()
            return False
        return True
