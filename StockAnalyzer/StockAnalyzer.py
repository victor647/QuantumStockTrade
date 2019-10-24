import baostock, pandas
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMainWindow
from QtDesign.StockAnalyzer_ui import Ui_StockAnalyzer
import StockAnalyzer.TradeSimulator as TradeSimulator
from StockAnalyzer.TradeStrategy import TradeStrategy
import Data.DataAnalyzer as DataAnalyzer
import Tools, FileManager


stockDatabase = pandas.DataFrame()
marketDatabase = pandas.DataFrame()
stockAnalyzerInstance = None
    

class StockAnalyzer(QMainWindow, Ui_StockAnalyzer):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.__tradeStrategy = TradeStrategy()
        self.__analysisData = DataAnalyzer.AnalysisData()
        # 初始化单例
        global stockAnalyzerInstance
        stockAnalyzerInstance = self

    def get_history_data(self):
        # 获取股票代码
        stock_code = self.iptStockNumber.text()
        # 获取交易所信息
        market = Tools.get_trade_center(stock_code)
        now = QDate.currentDate()
        start_date = now.addYears(-1).toString('yyyy-MM-dd')
        end_date = now.toString('yyyy-MM-dd')

        # 获取股票历史数据
        result = baostock.query_history_k_data_plus(code=market + "." + stock_code, fields="date,open,high,low,close,preclose,pctChg,turn,tradestatus,isST",
                                                    start_date=start_date, end_date=end_date, frequency="d", adjustflag="2")
        FileManager.save_stock_history_data(result, stock_code)
        global stockDatabase
        stockDatabase = FileManager.read_stock_history_data(stock_code)
        # 确保股票代码有效
        if stockDatabase is None:
            Tools.show_error_dialog("股票代码无效或网络无响应！")
            return

        # 获取股票对应的大盘历史数据
        market_code = "000001" if market == "sh" else "399001"
        start_date = now.addMonths(self.spbAnalyzeMonths.value() * -1).toString('yyyy-MM-dd')
        result_market = baostock.query_history_k_data(code=market + "." + market_code, fields="date,open,high,low,close,preclose,turn",
                                                      start_date=start_date, end_date=end_date, frequency="d", adjustflag="2")
        # 初始化大盘历史数据
        global marketDatabase
        marketDatabase = pandas.DataFrame(result_market.data, columns=result_market.fields, dtype=float)
        # 分析大盘表现
        DataAnalyzer.analyze_database(marketDatabase)
        # 裁剪股票数据
        stockDatabase = stockDatabase.tail(marketDatabase.shape[0]).reset_index(drop=True)
        # 分析股票股性
        DataAnalyzer.analyze_database(stockDatabase)

        self.analyze_data()

    # 显示股票股性
    def analyze_data(self):
        self.__analysisData.averageTurn = DataAnalyzer.average_turn(stockDatabase)
        self.__analysisData.averageCloseUp = DataAnalyzer.average_close_when_up(stockDatabase)
        self.__analysisData.averageCloseDown = DataAnalyzer.average_close_when_down(stockDatabase)
        self.__analysisData.averageHighWhenUp = DataAnalyzer.average_high_when_up(stockDatabase)
        self.__analysisData.averageHighWhenDown = DataAnalyzer.average_high_when_down(stockDatabase)
        self.__analysisData.averageLowWhenDown = DataAnalyzer.average_low_when_down(stockDatabase)
        self.__analysisData.averageLowWhenUp = DataAnalyzer.average_low_when_up(stockDatabase)
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

        # 大盘表现
        self.lblMarketIntervalOpen.setText("区间开盘点位：" + str(DataAnalyzer.interval_open_price(marketDatabase)))
        self.lblMarketIntervalClose.setText("区间收盘点位：" + str(DataAnalyzer.interval_close_price(marketDatabase)))
        self.lblMarketIntervalHigh.setText("区间最高点位：" + str(DataAnalyzer.interval_highest_price(marketDatabase)))
        self.lblMarketIntervalLow.setText("区间最低点位：" + str(DataAnalyzer.interval_lowest_price(marketDatabase)))
        self.lblMarketIntervalAverage.setText("区间平均点位：" + str(DataAnalyzer.interval_average_price(marketDatabase)))
        self.lblMarketIntervalTotal.setText("区间累计涨幅：" + str(DataAnalyzer.interval_total_performance(marketDatabase)) + "%")
        self.lblMarketIntervalAveragePoint.setText("平均每日涨幅：" + str(DataAnalyzer.interval_average_performance(marketDatabase)) + "%")
        self.lblMarketUpProbability.setText("每日上涨概率：" + str(DataAnalyzer.close_price_up(marketDatabase)) + "%")

        self.lblWinMarket.setText("跑赢大盘日数：" + str(DataAnalyzer.win_market(stockDatabase, marketDatabase)) + "%")
        self.lblInverseMarketUp.setText("逆市上涨日数：" + str(DataAnalyzer.inverse_market_up(stockDatabase, marketDatabase)) + "%")
        self.lblInverseMarketDown.setText("逆市下跌日数：" + str(DataAnalyzer.inverse_market_down(stockDatabase, marketDatabase)) + "%")
        self.lblHighOpenHighClose.setText("高开高走概率：" + str(DataAnalyzer.high_open_high_close(stockDatabase)) + "%")
        self.lblHighOpenLowClose.setText("高开低走概率：" + str(DataAnalyzer.high_open_low_close(stockDatabase)) + "%")
        self.lblLowOpenLowClose.setText("低开低走概率：" + str(DataAnalyzer.low_open_low_close(stockDatabase)) + "%")
        self.lblLowOpenHighClose.setText("低开高走概率：" + str(DataAnalyzer.low_open_high_close(stockDatabase)) + "%")
        self.lblReachMaxProbability.setText("涨停触板概率：" + str(DataAnalyzer.reach_max_limit(stockDatabase)) + "%")
        self.lblStayMaxProbability.setText("涨停收盘概率：" + str(DataAnalyzer.stay_max_limit(stockDatabase)) + "%")
        self.lblReachMinProbability.setText("跌停触板概率：" + str(DataAnalyzer.reach_min_limit(stockDatabase)) + "%")
        self.lblStayMinProbability.setText("跌停收盘概率：" + str(DataAnalyzer.stay_min_limit(stockDatabase)) + "%")

        # 股性指标
        self.lblAverageTurn.setText("平均换手率：" + str(self.__analysisData.averageTurn) + "%")
        self.lblAverageAmplitude.setText("每日平均振幅：" + str(self.__analysisData.averageFullAmp) + "%")
        self.lblAverageCloseUp.setText("阳线平均涨幅：" + str(self.__analysisData.averageCloseUp) + "%")
        self.lblAverageHighWhenUp.setText("阳线平均最高：" + str(self.__analysisData.averageHighWhenUp) + "%")
        self.lblAverageLowWhenUp.setText("阳线平均最低：" + str(self.__analysisData.averageHighWhenDown) + "%")
        self.lblAverageFallbackAmp.setText("阳线平均回撤：" + str(self.__analysisData.averageFallback) + "%")
        self.lblAverageCloseDown.setText("阴线平均跌幅：" + str(self.__analysisData.averageCloseDown) + "%")
        self.lblAverageHighWhenDown.setText("阴线平均最高：" + str(self.__analysisData.averageHighWhenDown) + "%")
        self.lblAverageLowWhenDown.setText("阴线平均最低：" + str(self.__analysisData.averageLowWhenDown) + "%")
        self.lblAverageBounceAmp.setText("阴线平均反弹：" + str(self.__analysisData.averageBounce) + "%")

    def auto_get_strategy(self):
        if not self.check_stock_data_exist():
            return
        self.__tradeStrategy.auto_get_strategy(self.__analysisData)
        self.spbBuyPointBase.setValue(self.__tradeStrategy.buyPointBase)
        self.spbBuyPointTrendBias.setValue(self.__tradeStrategy.buyPointTrendBias)
        self.spbSellPointBase.setValue(self.__tradeStrategy.sellPointBase)
        self.spbSellPointTrendBias.setValue(self.__tradeStrategy.sellPointTrendBias)
        self.cbxAllowSameDayTrade.setChecked(self.__tradeStrategy.allowSameDayTrade)
        self.spbSameDayProfit.setValue(self.__tradeStrategy.sameDayProfit)

    def start_trade(self):
        if not self.check_stock_data_exist():
            return
        self.__tradeStrategy.buyPointBase = self.spbBuyPointBase.value()
        self.__tradeStrategy.sellPointBase = self.spbSellPointBase.value()
        self.__tradeStrategy.buyPointTrendBias = self.spbBuyPointTrendBias.value()
        self.__tradeStrategy.sellPointTrendBias = self.spbSellPointTrendBias.value()
        self.__tradeStrategy.buyPointStep = self.spbBuyPointStep.value()
        self.__tradeStrategy.sellPointStep = self.spbSellPointStep.value()
        self.__tradeStrategy.allowSameDayTrade = self.cbxAllowSameDayTrade.isChecked()
        self.__tradeStrategy.sameDayProfit = self.spbSameDayProfit.value()
        self.__tradeStrategy.initialShare = self.spbInitialShare.value() * 100
        self.__tradeStrategy.sharePerTrade = self.spbSharePerTrade.value() * 100
        self.__tradeStrategy.maxShare = self.spbMaxShare.value() * 100
        self.__tradeStrategy.minShare = self.spbMinShare.value() * 100
        self.__tradeStrategy.signalTradeShare = self.__tradeStrategy.sharePerTrade * self.spbSignalTradeUnit.value()
        self.__tradeStrategy.trendChangeTradeShare = self.__tradeStrategy.sharePerTrade * self.spbTrendChangeTradeUnit.value()
        self.__tradeStrategy.biasThreshold = self.spbBiasThreshold.value()
        stock_code = self.iptStockNumber.text()

        trade_window = TradeSimulator.TradeSimulator()
        trade_window.setWindowTitle(stock_code + "模拟交易")
        TradeSimulator.init_trade_strategy(self.__tradeStrategy, stock_code)
        trade_window.show()
        trade_window.start_trading()
        trade_window.exec_()
        return

    def check_stock_data_exist(self):
        if self.__analysisData.averageTurn == 0:
            Tools.show_error_dialog("请先获取股票历史数据！")
            return False
        return True
