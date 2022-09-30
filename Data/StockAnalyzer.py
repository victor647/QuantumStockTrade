import baostock, pandas
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView
from QtDesign.StockAnalyzer_ui import Ui_StockAnalyzer
import Data.TechnicalAnalysis as TA
from Data.HistoryGraph import CandleStickChart, PriceDistributionChart
from Tools import Tools


# 分析个股和大盘在一段时期内的股性
class StockAnalyzer(QMainWindow, Ui_StockAnalyzer):
    stockDatabase = None
    marketDatabase = None

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup_triggers()
        # 默认从6个月前到今天
        today = QDate.currentDate()
        self.dteEndDate.setDate(today)
        self.dteStartDate.setDate(today.addMonths(-6))

    def setup_triggers(self):
        self.btnGetData.clicked.connect(self.get_history_data)
        self.btnStockGraph.clicked.connect(self.show_stock_graph)
        self.btnMarketGraph.clicked.connect(self.show_market_graph)
        self.btnPlotOpenCloseDistribution.clicked.connect(self.plot_open_close_distribution)
        self.btnPlotHighLowDistribution.clicked.connect(self.plot_high_low_distribution)

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
        self.stockDatabase = pandas.DataFrame(result.data, columns=result.fields, dtype=float)
        self.stockDatabase.set_index('date', inplace=True)
        # 确保股票代码有效
        if self.stockDatabase is None:
            Tools.show_error_dialog('股票代码无效或网络无响应！')
            return

        # 获取股票对应的大盘历史数据
        result_market = baostock.query_history_k_data(code=market + '.' + index_code, fields='date,open,high,low,close,preclose,turn',
                                                      start_date=start_date, end_date=end_date, frequency='d', adjustflag='2')
        self.marketDatabase = pandas.DataFrame(result_market.data, columns=result_market.fields, dtype=float)
        self.marketDatabase.set_index('date', inplace=True)
        # 分析大盘表现
        TA.get_percentage_data(self.marketDatabase)
        # 分析股票股性
        TA.get_percentage_data(self.stockDatabase)
        # 计算均线
        TA.get_standard_ma(self.marketDatabase)
        TA.get_standard_ma(self.stockDatabase)
        self.analyze_data()
        self.repaint()

    # 显示股票股性
    def analyze_data(self):
        # 个股表现
        self.lblStockIntervalOpen.setText('区间开盘价格：' + str(TA.interval_open_price(self.stockDatabase)))
        self.lblStockIntervalClose.setText('区间收盘价格：' + str(TA.interval_close_price(self.stockDatabase)))
        self.lblStockIntervalHigh.setText('区间最高价格：' + str(TA.interval_highest_price(self.stockDatabase)))
        self.lblStockIntervalLow.setText('区间最低价格：' + str(TA.interval_lowest_price(self.stockDatabase)))
        self.lblStockIntervalAverage.setText('区间平均价格：' + str(TA.interval_average_price(self.stockDatabase)))
        self.lblStockIntervalTotal.setText('区间累计涨幅：' + str(TA.interval_total_performance(self.stockDatabase)) + '%')
        self.lblStockIntervalAveragePoint.setText('平均每日涨幅：' + str(TA.interval_average_performance(self.stockDatabase)) + '%')
        self.lblStockUpProbability.setText('每日上涨概率：' + str(TA.close_price_up(self.stockDatabase)) + '%')

        # 大盘表现
        self.lblMarketIntervalOpen.setText('区间开盘点位：' + str(TA.interval_open_price(self.marketDatabase)))
        self.lblMarketIntervalClose.setText('区间收盘点位：' + str(TA.interval_close_price(self.marketDatabase)))
        self.lblMarketIntervalHigh.setText('区间最高点位：' + str(TA.interval_highest_price(self.marketDatabase)))
        self.lblMarketIntervalLow.setText('区间最低点位：' + str(TA.interval_lowest_price(self.marketDatabase)))
        self.lblMarketIntervalAverage.setText('区间平均点位：' + str(TA.interval_average_price(self.marketDatabase)))
        self.lblMarketIntervalTotal.setText('区间累计涨幅：' + str(TA.interval_total_performance(self.marketDatabase)) + '%')
        self.lblMarketIntervalAveragePoint.setText('平均每日涨幅：' + str(TA.interval_average_performance(self.marketDatabase)) + '%')
        self.lblMarketUpProbability.setText('每日上涨概率：' + str(TA.close_price_up(self.marketDatabase)) + '%')

        self.lblWinMarket.setText('跑赢大盘日数：' + str(TA.win_market(self.stockDatabase, self.marketDatabase)) + '%')
        self.lblInverseMarketUp.setText('逆市上涨日数：' + str(TA.inverse_market_up(self.stockDatabase, self.marketDatabase)) + '%')
        self.lblInverseMarketDown.setText('逆市下跌日数：' + str(TA.inverse_market_down(self.stockDatabase, self.marketDatabase)) + '%')
        self.lblHighOpenHighClose.setText('高开高走概率：' + str(TA.high_open_high_close(self.stockDatabase)) + '%')
        self.lblHighOpenLowClose.setText('高开低走概率：' + str(TA.high_open_low_close(self.stockDatabase)) + '%')
        self.lblLowOpenLowClose.setText('低开低走概率：' + str(TA.low_open_low_close(self.stockDatabase)) + '%')
        self.lblLowOpenHighClose.setText('低开高走概率：' + str(TA.low_open_high_close(self.stockDatabase)) + '%')
        self.lblReachMaxProbability.setText('涨停触板概率：' + str(TA.reach_max_limit(self.stockDatabase)) + '%')
        self.lblStayMaxProbability.setText('涨停收盘概率：' + str(TA.stay_max_limit(self.stockDatabase)) + '%')
        self.lblReachMinProbability.setText('跌停触板概率：' + str(TA.reach_min_limit(self.stockDatabase)) + '%')
        self.lblStayMinProbability.setText('跌停收盘概率：' + str(TA.stay_min_limit(self.stockDatabase)) + '%')

        # 股性指标
        self.lblAverageTurn.setText('平均换手率：' + str(TA.average_turn(self.stockDatabase)) + '%')
        self.lblAverageAmplitude.setText('每日平均振幅：' + str(TA.average_amplitude(self.stockDatabase)) + '%')
        self.lblAverageCloseUp.setText('阳线平均涨幅：' + str(TA.average_close_when_up(self.stockDatabase)) + '%')
        self.lblAverageHighWhenUp.setText('阳线平均最高：' + str(TA.average_high_when_up(self.stockDatabase)) + '%')
        self.lblAverageLowWhenUp.setText('阳线平均最低：' + str(TA.average_low_when_up(self.stockDatabase)) + '%')
        self.lblAverageFallbackAmp.setText('阳线平均回撤：' + str(TA.average_fallback(self.stockDatabase)) + '%')
        self.lblAverageCloseDown.setText('阴线平均跌幅：' + str(TA.average_close_when_down(self.stockDatabase)) + '%')
        self.lblAverageHighWhenDown.setText('阴线平均最高：' + str(TA.average_high_when_down(self.stockDatabase)) + '%')
        self.lblAverageLowWhenDown.setText('阴线平均最低：' + str(TA.average_low_when_down(self.stockDatabase)) + '%')
        self.lblAverageBounceAmp.setText('阴线平均反弹：' + str(TA.average_bounce(self.stockDatabase)) + '%')

    # 显示开盘收盘涨幅分布图
    def plot_open_close_distribution(self):
        stock_code = Tools.get_stock_code(self.iptStockNumber)
        chart = PriceDistributionChart(stock_code, self.stockDatabase)
        chart.plot_open_close_data()
        chart.exec_()

    # 显示高低涨幅分布图
    def plot_high_low_distribution(self):
        stock_code = Tools.get_stock_code(self.iptStockNumber)
        chart = PriceDistributionChart(stock_code, self.stockDatabase)
        chart.plot_high_low_data()
        chart.exec_()

    # 显示个股K线
    def show_stock_graph(self):
        stock_code = Tools.get_stock_code(self.iptStockNumber)
        chart = CandleStickChart(self.stockDatabase, stock_code)
        chart.plot_all_ma_lines()
        chart.plot_price()
        chart.plot_volume()
        chart.plot_high_low_points(self.highLowPoints)
        chart.exec_()

    # 显示大盘K线
    def show_market_graph(self):
        chart = CandleStickChart(self.marketDatabase, '同期大盘')
        chart.plot_all_ma_lines()
        chart.plot_price()
        chart.plot_volume()
        chart.exec_()
