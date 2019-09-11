import baostock
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMainWindow, QErrorMessage
from QtDesign.StockAnalyzer_ui import Ui_StockAnalyzer
from Data.AnalysisData import AnalysisData
from Windows.TradeSimulator import *
from Data.TradeStrategy import TradeStrategy
from Data.DataManager import DataManager


class StockAnalyzer(QMainWindow, Ui_StockAnalyzer):
    tradeStrategy = TradeStrategy()
    analysisData = AnalysisData()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        now = QDate.currentDate()
        start = now.addMonths(-6)
        self.dteStartDate.setDate(start)
        self.dteEndDate.setDate(now)

    def get_history_data(self):
        DataManager.init()
        stock_code = self.iptStockNumber.text()
        market = StockAnalyzer.get_trade_center(stock_code)

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
        DataManager.parse_daily_data(result_stock.data, DataManager.stockDatabase)

        market_code = "000001" if market == "sh" else "399001"
        result_market = baostock.query_history_k_data(code=market + "." + market_code, fields="date,open,high,low,close,preclose,turn",
                                                      start_date=start_date, end_date=end_date, frequency="d", adjustflag="2")
        DataManager.parse_daily_data(result_market.data, DataManager.marketDatabase)
        self.show_data()

    @staticmethod
    def get_trade_center(stock_code):
        code = int(stock_code)
        market = ""
        # 深圳主板
        if 0 < code < 100000:
            market = "sz"
        # 创业板
        elif 300000 < code < 400000:
            market = "sz"
        # 上海主板
        elif 600000 < code < 700000:
            market = "sh"
        # 深圳可转债
        elif 128000 <= code <= 129000:
            market = "sz"
        # 上海可转债
        elif 113500 <= code <= 113600:
            market = "sh"
        return market

    @staticmethod
    def get_minute_data(date, code):
        market = StockAnalyzer.get_trade_center(code)
        return baostock.query_history_k_data(code=market + "." + code, fields="time,high,low",
                                             start_date=date, end_date=date, frequency="5", adjustflag="2")

    def show_data(self):        
        self.analysisData.upProbability = DataManager.interval_up_probability(DataManager.stockDatabase)
        self.analysisData.averageTurn = DataManager.average_turn()
        self.analysisData.averageCloseUp = DataManager.average_close_up()
        self.analysisData.averageCloseDown = DataManager.average_close_down()
        self.analysisData.averageHigh = DataManager.average_high()
        self.analysisData.averageLow = DataManager.average_low()
        self.analysisData.averageHighWhenUp = DataManager.average_high_when_up()
        self.analysisData.averageLowWhenDown = DataManager.average_low_when_down()
        self.analysisData.averageFullAmp = DataManager.average_full_amplitude()
        self.analysisData.averageFallback = DataManager.average_fallback()
        self.analysisData.averageBounce = DataManager.average_bounce()

        # 个股表现
        self.lblStockIntervalOpen.setText("区间开盘价格：" + str(DataManager.interval_open_price(DataManager.stockDatabase)))
        self.lblStockIntervalClose.setText("区间收盘价格：" + str(DataManager.interval_close_price(DataManager.stockDatabase)))
        self.lblStockIntervalHigh.setText("区间最高价格：" + str(DataManager.interval_highest_price(DataManager.stockDatabase)))
        self.lblStockIntervalLow.setText("区间最低价格：" + str(DataManager.interval_lowest_price(DataManager.stockDatabase)))
        self.lblStockIntervalAverage.setText("区间平均价格：" + str(DataManager.interval_average_price(DataManager.stockDatabase)))
        self.lblStockIntervalTotal.setText("区间累计涨幅：" + str(DataManager.interval_total_performance(DataManager.stockDatabase)) + "%")
        self.lblStockIntervalAveragePoint.setText("平均每日涨幅：" + str(DataManager.interval_average_performance(DataManager.stockDatabase)) + "%")
        self.lblStockUpProbability.setText("每日上涨概率：" + str(self.analysisData.upProbability) + "%")
        self.lblWinMarket.setText("跑赢大盘日数：" + str(DataManager.win_market_probability()) + "%")
        self.lblOffMarketPoint.setText("日均偏离大盘：" + str(DataManager.off_market_point()) + "%")
        self.lblInverseMarketUp.setText("逆市上涨日数：：" + str(DataManager.inverse_market_up_probability()) + "%")
        self.lblInverseMarketDown.setText("逆市下跌日数：：" + str(DataManager.inverse_market_down_probability()) + "%")
        self.lblAverageHigh.setText("平均最高涨幅：" + str(self.analysisData.averageHigh) + "%")
        self.lblAverageLow.setText("平均最低涨幅：" + str(self.analysisData.averageLow) + "%")
        self.lblReachMaxProbability.setText("涨停触板概率：" + str(DataManager.reach_max_probability()) + "%")
        self.lblStayMaxProbability.setText("涨停收盘概率：" + str(DataManager.stay_max_probability()) + "%")
        self.lblReachMinProbability.setText("跌停触板概率：" + str(DataManager.reach_min_probability()) + "%")
        self.lblStayMinProbability.setText("跌停收盘概率：" + str(DataManager.stay_min_probability()) + "%")

        # 股性指标
        self.lblAverageTurn.setText("平均换手率：" + str(self.analysisData.averageTurn) + "%")
        self.lblAverageAmplitude.setText("每日平均振幅：" + str(self.analysisData.averageFullAmp) + "%")
        self.lblAverageCloseUp.setText("阳线平均涨幅：" + str(self.analysisData.averageCloseUp) + "%")
        self.lblAverageHighWhenUp.setText("阳线平均最高：" + str(self.analysisData.averageHighWhenUp) + "%")
        self.lblAverageFallbackAmp.setText("阳线平均回撤：" + str(self.analysisData.averageFallback) + "%")
        self.lblAverageCloseDown.setText("阴线平均跌幅：" + str(self.analysisData.averageCloseDown) + "%")
        self.lblAverageLowWhenDown.setText("阴线平均最低：" + str(self.analysisData.averageLowWhenDown) + "%")
        self.lblAverageBounceAmp.setText("阴线平均反弹：" + str(self.analysisData.averageBounce) + "%")

        # 大盘表现
        self.lblMarketIntervalOpen.setText("区间开盘点位：" + str(DataManager.interval_open_price(DataManager.marketDatabase)))
        self.lblMarketIntervalClose.setText("区间收盘点位：" + str(DataManager.interval_close_price(DataManager.marketDatabase)))
        self.lblMarketIntervalHigh.setText("区间最高点位：" + str(DataManager.interval_highest_price(DataManager.marketDatabase)))
        self.lblMarketIntervalLow.setText("区间最低点位：" + str(DataManager.interval_lowest_price(DataManager.marketDatabase)))
        self.lblMarketIntervalAverage.setText("区间平均点位：" + str(DataManager.interval_average_price(DataManager.marketDatabase)) + "%")
        self.lblMarketIntervalTotal.setText("区间累计涨幅：" + str(DataManager.interval_total_performance(DataManager.marketDatabase)) + "%")
        self.lblMarketIntervalAveragePoint.setText("平均每日涨幅：" + str(DataManager.interval_average_performance(DataManager.marketDatabase)) + "%")
        self.lblMarketUpProbability.setText("每日上涨概率：" + str(DataManager.interval_up_probability(DataManager.marketDatabase)) + "%")

    def auto_get_strategy(self):
        if not self.check_stock_data_exist():
            return
        self.tradeStrategy.auto_get_strategy(self.analysisData)
        self.spbBuyPoint.setValue(self.tradeStrategy.buyPoint)
        self.spbSellPoint.setValue(self.tradeStrategy.sellPoint)
        self.cbxAllowSameDayTrade.setChecked(self.tradeStrategy.allowSameDayTrade)
        self.spbSameDayProfit.setValue(self.tradeStrategy.sameDayProfit)

    def start_trade(self):
        if not self.check_stock_data_exist():
            return
        self.tradeStrategy.buyPoint = self.spbBuyPoint.value()
        self.tradeStrategy.sellPoint = self.spbSellPoint.value()
        self.tradeStrategy.allowSameDayTrade = self.cbxAllowSameDayTrade.isChecked()
        self.tradeStrategy.sameDayProfit = self.spbSameDayProfit.value()
        self.tradeStrategy.baseShare = self.spbBaseShare.value()
        self.tradeStrategy.sharePerTrade = self.spbSharePerTrade.value()
        self.tradeStrategy.maxShare = self.spbMaxShare.value()
        self.tradeStrategy.minShare = self.spbMinShare.value()
        self.tradeStrategy.averagePricePeriod = self.spbAveragePeriodPriceLong.value()
        self.tradeStrategy.averageVolumePeriod = self.spbAveragePeriodVolume.value()
        self.tradeStrategy.volumeWeight = self.spbVolumeMultiplier.value()
        stock_code = self.iptStockNumber.text()

        trade_window = TradeSimulator()
        trade_window.setWindowTitle(stock_code + "模拟交易")
        trade_window.get_trade_strategy(self.tradeStrategy, stock_code)
        trade_window.show()
        trade_window.start_trading()
        trade_window.exec_()
        return

    def check_stock_data_exist(self):
        if self.analysisData.upProbability < 0:
            error_dialog = QErrorMessage()
            error_dialog.setWindowTitle("错误")
            error_dialog.showMessage("请先获取股票历史数据！")
            error_dialog.exec_()
            return False
        return True



