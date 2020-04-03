import baostock, pandas
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMainWindow
from QtDesign.StockAnalyzer_ui import Ui_StockAnalyzer
import Data.TechnicalAnalysis as TechnicalAnalysis
from Data.HistoryGraph import PriceDistributionChart
from Tools import Tools
    

# 分析个股和大盘在一段时期内的股性
class StockAnalyzer(QMainWindow, Ui_StockAnalyzer):
    __stockDatabase = None
    __marketDatabase = None
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 默认从6个月前到今天
        today = QDate.currentDate()
        self.dteEndDate.setDate(today)
        self.dteStartDate.setDate(today.addMonths(-6))

    # 获取股票历史数据
    def get_history_data(self):
        # 获取股票代码
        stock_code = Tools.get_stock_code(self.iptStockNumber)
        # 无效的输入
        if stock_code == '':
            Tools.show_error_dialog('股票代码或名称无效！')
            return

        # 获取交易所信息和大盘指数代码
        market, index_code = Tools.get_trade_center_and_index(stock_code)
        # 获取分析日期范围
        start_date = self.dteStartDate.date().toString('yyyy-MM-dd')
        end_date = self.dteEndDate.date().toString('yyyy-MM-dd')

        # 获取股票历史数据
        result = baostock.query_history_k_data(code=market + '.' + stock_code, fields='date,open,high,low,close,preclose,pctChg,turn,tradestatus,isST',
                                               start_date=start_date, end_date=end_date, frequency='d', adjustflag='2')
        self.__stockDatabase = pandas.DataFrame(result.data, columns=result.fields, dtype=float)
        # 确保股票代码有效
        if self.__stockDatabase is None:
            Tools.show_error_dialog('股票代码无效或网络无响应！')
            return

        # 获取股票对应的大盘历史数据
        result_market = baostock.query_history_k_data(code=market + '.' + index_code, fields='date,open,high,low,close,preclose,turn',
                                                      start_date=start_date, end_date=end_date, frequency='d', adjustflag='2')
        self.__marketDatabase = pandas.DataFrame(result_market.data, columns=result_market.fields, dtype=float)
        # 分析大盘表现
        TechnicalAnalysis.get_percentage_data(self.__marketDatabase)
        # 裁剪股票数据
        # self.__stockDatabase = self.__stockDatabase.tail(self.__marketDatabase.shape[0]).reset_index(drop=True)
        # 分析股票股性
        TechnicalAnalysis.get_percentage_data(self.__stockDatabase)
        self.analyze_data()
        self.repaint()

    # 显示股票股性
    def analyze_data(self):
        # 个股表现
        self.lblStockIntervalOpen.setText('区间开盘价格：' + str(TechnicalAnalysis.interval_open_price(self.__stockDatabase)))
        self.lblStockIntervalClose.setText('区间收盘价格：' + str(TechnicalAnalysis.interval_close_price(self.__stockDatabase)))
        self.lblStockIntervalHigh.setText('区间最高价格：' + str(TechnicalAnalysis.interval_highest_price(self.__stockDatabase)))
        self.lblStockIntervalLow.setText('区间最低价格：' + str(TechnicalAnalysis.interval_lowest_price(self.__stockDatabase)))
        self.lblStockIntervalAverage.setText('区间平均价格：' + str(TechnicalAnalysis.interval_average_price(self.__stockDatabase)))
        self.lblStockIntervalTotal.setText('区间累计涨幅：' + str(TechnicalAnalysis.interval_total_performance(self.__stockDatabase)) + '%')
        self.lblStockIntervalAveragePoint.setText('平均每日涨幅：' + str(TechnicalAnalysis.interval_average_performance(self.__stockDatabase)) + '%')
        self.lblStockUpProbability.setText('每日上涨概率：' + str(TechnicalAnalysis.close_price_up(self.__stockDatabase)) + '%')

        # 大盘表现
        self.lblMarketIntervalOpen.setText('区间开盘点位：' + str(TechnicalAnalysis.interval_open_price(self.__marketDatabase)))
        self.lblMarketIntervalClose.setText('区间收盘点位：' + str(TechnicalAnalysis.interval_close_price(self.__marketDatabase)))
        self.lblMarketIntervalHigh.setText('区间最高点位：' + str(TechnicalAnalysis.interval_highest_price(self.__marketDatabase)))
        self.lblMarketIntervalLow.setText('区间最低点位：' + str(TechnicalAnalysis.interval_lowest_price(self.__marketDatabase)))
        self.lblMarketIntervalAverage.setText('区间平均点位：' + str(TechnicalAnalysis.interval_average_price(self.__marketDatabase)))
        self.lblMarketIntervalTotal.setText('区间累计涨幅：' + str(TechnicalAnalysis.interval_total_performance(self.__marketDatabase)) + '%')
        self.lblMarketIntervalAveragePoint.setText('平均每日涨幅：' + str(TechnicalAnalysis.interval_average_performance(self.__marketDatabase)) + '%')
        self.lblMarketUpProbability.setText('每日上涨概率：' + str(TechnicalAnalysis.close_price_up(self.__marketDatabase)) + '%')

        self.lblWinMarket.setText('跑赢大盘日数：' + str(TechnicalAnalysis.win_market(self.__stockDatabase, self.__marketDatabase)) + '%')
        self.lblInverseMarketUp.setText('逆市上涨日数：' + str(TechnicalAnalysis.inverse_market_up(self.__stockDatabase, self.__marketDatabase)) + '%')
        self.lblInverseMarketDown.setText('逆市下跌日数：' + str(TechnicalAnalysis.inverse_market_down(self.__stockDatabase, self.__marketDatabase)) + '%')
        self.lblHighOpenHighClose.setText('高开高走概率：' + str(TechnicalAnalysis.high_open_high_close(self.__stockDatabase)) + '%')
        self.lblHighOpenLowClose.setText('高开低走概率：' + str(TechnicalAnalysis.high_open_low_close(self.__stockDatabase)) + '%')
        self.lblLowOpenLowClose.setText('低开低走概率：' + str(TechnicalAnalysis.low_open_low_close(self.__stockDatabase)) + '%')
        self.lblLowOpenHighClose.setText('低开高走概率：' + str(TechnicalAnalysis.low_open_high_close(self.__stockDatabase)) + '%')
        self.lblReachMaxProbability.setText('涨停触板概率：' + str(TechnicalAnalysis.reach_max_limit(self.__stockDatabase)) + '%')
        self.lblStayMaxProbability.setText('涨停收盘概率：' + str(TechnicalAnalysis.stay_max_limit(self.__stockDatabase)) + '%')
        self.lblReachMinProbability.setText('跌停触板概率：' + str(TechnicalAnalysis.reach_min_limit(self.__stockDatabase)) + '%')
        self.lblStayMinProbability.setText('跌停收盘概率：' + str(TechnicalAnalysis.stay_min_limit(self.__stockDatabase)) + '%')

        # 股性指标
        self.lblAverageTurn.setText('平均换手率：' + str(TechnicalAnalysis.average_turn(self.__stockDatabase)) + '%')
        self.lblAverageAmplitude.setText('每日平均振幅：' + str(TechnicalAnalysis.average_amplitude(self.__stockDatabase)) + '%')
        self.lblAverageCloseUp.setText('阳线平均涨幅：' + str(TechnicalAnalysis.average_close_when_up(self.__stockDatabase)) + '%')
        self.lblAverageHighWhenUp.setText('阳线平均最高：' + str(TechnicalAnalysis.average_high_when_up(self.__stockDatabase)) + '%')
        self.lblAverageLowWhenUp.setText('阳线平均最低：' + str(TechnicalAnalysis.average_low_when_up(self.__stockDatabase)) + '%')
        self.lblAverageFallbackAmp.setText('阳线平均回撤：' + str(TechnicalAnalysis.average_fallback(self.__stockDatabase)) + '%')
        self.lblAverageCloseDown.setText('阴线平均跌幅：' + str(TechnicalAnalysis.average_close_when_down(self.__stockDatabase)) + '%')
        self.lblAverageHighWhenDown.setText('阴线平均最高：' + str(TechnicalAnalysis.average_low_when_down(self.__stockDatabase)) + '%')
        self.lblAverageLowWhenDown.setText('阴线平均最低：' + str(TechnicalAnalysis.average_low_when_down(self.__stockDatabase)) + '%')
        self.lblAverageBounceAmp.setText('阴线平均反弹：' + str(TechnicalAnalysis.average_bounce(self.__stockDatabase)) + '%')

    # 显示开盘收盘涨幅分布图
    def plot_open_close_distribution(self):
        stock_code = Tools.get_stock_code(self.iptStockNumber)
        chart = PriceDistributionChart(stock_code, self.__stockDatabase)
        chart.plot_open_close_data()
        chart.exec_()

    # 显示高低涨幅分布图
    def plot_high_low_distribution(self):
        stock_code = Tools.get_stock_code(self.iptStockNumber)
        chart = PriceDistributionChart(stock_code, self.__stockDatabase)
        chart.plot_high_low_data()
        chart.exec_()
