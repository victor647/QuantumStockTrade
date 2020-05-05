from PyQt5.QtWidgets import QDialog
from PyQt5.QtChart import *
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QColor, QFont
from QtDesign.HistoryGraph_ui import Ui_HistoryGraph
from Data.InvestmentStatus import StockInvestment
import Data.TechnicalAnalysis as TA
from Tools import FileManager
import pandas, math


# 美化散点图
def decorate_scatter_series(series: QScatterSeries, text: str, color: QColor, label_size=12):
    series.setPointLabelsVisible(True)
    series.setPointLabelsFormat(text)
    series.setPointLabelsFont(QFont('Helvetica', label_size, QFont.Bold))
    series.setPointLabelsColor(color)
    series.setMarkerSize(5)
    series.setColor(color)
    series.setBorderColor(Qt.gray)


# 美化柱状图
def decorate_bar_series(bar_set: QBarSet, color: QColor, transparent=False):
    # 设置颜色
    bar_set.setColor(Qt.transparent if transparent else color)
    bar_set.setBorderColor(color)


# 画选股日期附近的K线
def plot_stock_search_and_trade(stock_code: str, search_date: str, days_after=20, days_before=100, trade_history=None):
    stock_data = FileManager.read_stock_history_data(stock_code, True)
    # 计算均线数据
    TA.calculate_all_ma_curves(stock_data)
    # 选股日期后的数据
    data_after = TA.get_stock_data_after_date(stock_data, search_date, days_after)
    # 选股日期前的数据
    data_before = TA.get_stock_data_before_date(stock_data, search_date, days_before)
    graph = CandleStickChart(pandas.concat([data_before, data_after]), stock_code)
    graph.plot_all_ma_lines()
    graph.plot_price()
    graph.plot_volume()
    graph.plot_search_date(data_before.index[-1])
    # 画交易记录
    if trade_history is not None:
        graph.plot_trade_history(trade_history, False)
    graph.exec_()


# K线图
class CandleStickChart(QDialog, Ui_HistoryGraph):
    __volumeSeries = None

    def __init__(self, stock_data: pandas.DataFrame, title='', show_year=False):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(title + '走势：' + stock_data.index[0] + ' ~ ' + stock_data.index[-1])
        self.__stockData = stock_data
        # 创建图表
        self.__chart = QChart()
        self.__chart.setBackgroundBrush(Qt.black)
        # 隐藏图例
        self.__chart.legend().hide()
        # 初始化日期显示
        self.__dates = []
        for index, day_data in self.__stockData.iterrows():
            self.__dates.append(index)
        # 创建日期x轴
        self.__axis_x = QBarCategoryAxis()
        self.__axis_x.setCategories(self.__dates)
        self.__chart.addAxis(self.__axis_x, Qt.AlignBottom)
        # 创建专门的日期显示X轴
        self.resize(len(self.__dates) * 15 + 100, 550)
        self.setMinimumSize(len(self.__dates) * 7 + 200, 400)
        self.__axis_x.hide()
        date_axis = QDateTimeAxis()
        date_axis.setTickCount(max(31, round(len(self.__dates) / 5) + 1))
        date_axis.setFormat('yy/MM/dd' if show_year else 'MM/dd')
        date_axis.setGridLineColor(Qt.black)
        date_axis.setLabelsColor(Qt.lightGray)
        date_axis.setMin(QDateTime.fromString(self.__stockData.index[0], 'yyyy-MM-dd'))
        date_axis.setMax(QDateTime.fromString(self.__stockData.index[-1], 'yyyy-MM-dd'))
        self.__chart.addAxis(date_axis, Qt.AlignBottom)

        # 添加股价Y轴
        self.__axis_price = QValueAxis()
        self.__axis_price.setTickCount(9)
        self.__axis_price.setGridLineColor(Qt.darkGray)
        self.__axis_price.setLabelsColor(Qt.lightGray)
        self.__chart.addAxis(self.__axis_price, Qt.AlignRight)
        # 显示图表
        self.crtGraph.setChart(self.__chart)
        self.show()

    # 画股价蜡烛图
    def plot_price(self):
        price_series = QCandlestickSeries()
        # 设置蜡烛图颜色
        price_series.setDecreasingColor(Qt.cyan)
        price_series.setIncreasingColor(Qt.transparent)
        # 添加数据
        for index, day_data in self.__stockData.iterrows():
            candlestick_set = QCandlestickSet(day_data['open'], day_data['high'], day_data['low'], day_data['close'])
            # 给线条上色，默认为白色
            candlestick_set.setPen(Qt.white)
            if day_data['close'] > day_data['open']:
                candlestick_set.setPen(Qt.red)
            elif day_data['close'] < day_data['open']:
                candlestick_set.setPen(Qt.cyan)
            elif 'preclose' in day_data:
                if day_data['close'] > day_data['preclose']:
                    candlestick_set.setPen(Qt.red)
                elif day_data['close'] < day_data['preclose']:
                    candlestick_set.setPen(Qt.cyan)
            price_series.append(candlestick_set)
        # 创建图表
        self.__chart.addSeries(price_series)
        # 计算价格轴范围
        max_price = self.__stockData['high'].max()
        min_price = self.__stockData['low'].min()
        # 若振幅过小，压缩绘图区域
        stretch_ratio = 1.5 / (max_price / min_price)
        if stretch_ratio > 1:
            max_price *= (stretch_ratio - 1) * 0.25 + 1
            min_price /= (stretch_ratio - 1) * 0.75 + 1
        # 避开成交量图形区域
        min_price -= (max_price - min_price) / 3
        self.__axis_price.setRange(min_price, max_price)
        price_series.attachAxis(self.__axis_x)
        price_series.attachAxis(self.__axis_price)

    # 画成交量柱状图
    def plot_volume(self):
        self.__volumeSeries = QStackedBarSeries()
        self.__volumeSeries.setBarWidth(0.7)
        volume_bar_up = QBarSet('up')
        volume_bar_down = QBarSet('down')
        decorate_bar_series(volume_bar_up, Qt.red, True)
        decorate_bar_series(volume_bar_down, Qt.cyan)
        self.__volumeSeries.append(volume_bar_up)
        self.__volumeSeries.append(volume_bar_down)
        # 添加数据
        for index, day_data in self.__stockData.iterrows():
            # 给成交量柱子上色
            if 'preclose' in day_data:
                if day_data['close'] >= day_data['preclose']:
                    volume_bar_up.append(day_data['turn'])
                    volume_bar_down.append(0)
                else:
                    volume_bar_down.append(day_data['turn'])
                    volume_bar_up.append(0)
            # 若没有昨日收盘信息，则根据当日表现填色
            else:
                if day_data['close'] >= day_data['open']:
                    volume_bar_up.append(day_data['turn'])
                    volume_bar_down.append(0)
                else:
                    volume_bar_down.append(day_data['turn'])
                    volume_bar_up.append(0)
        self.__chart.addSeries(self.__volumeSeries)
        # 创建成交量Y轴在右侧
        volume_axis = QValueAxis()
        volume_axis.setGridLineColor(Qt.darkGray)
        volume_axis.setLabelsColor(Qt.lightGray)
        volume_axis.setTickCount(9)
        # 将成交量图形置于最下方
        volume_axis.setMax(self.__stockData['turn'].max() * 4)
        self.__chart.addAxis(volume_axis, Qt.AlignLeft)
        self.__volumeSeries.attachAxis(volume_axis)
        self.__volumeSeries.attachAxis(self.__axis_x)

    # 画布林线轨道
    def plot_boll(self):
        boll_upper = QLineSeries()
        boll_middle = QLineSeries()
        boll_lower = QLineSeries()
        # 设置轨道颜色
        boll_upper.setColor(Qt.yellow)
        boll_middle.setColor(Qt.white)
        boll_lower.setColor(Qt.magenta)

        # 添加数据
        i = 0
        for index, day_data in self.__stockData.iterrows():
            boll_upper.append(i, day_data['boll_upper'])
            boll_middle.append(i, day_data['boll_middle'])
            boll_lower.append(i, day_data['boll_lower'])
            i += 1
        # 创建图表
        self.__chart.addSeries(boll_upper)
        self.__chart.addSeries(boll_middle)
        self.__chart.addSeries(boll_lower)
        boll_upper.attachAxis(self.__axis_x)
        boll_upper.attachAxis(self.__axis_price)
        boll_middle.attachAxis(self.__axis_x)
        boll_middle.attachAxis(self.__axis_price)
        boll_lower.attachAxis(self.__axis_x)
        boll_lower.attachAxis(self.__axis_price)

    # 画MACD曲线
    def plot_macd(self):
        macd_white = QLineSeries()
        macd_yellow = QLineSeries()
        # 创建差值柱
        macd_column = QStackedBarSeries()
        macd_column.setBarWidth(0.1)
        # 增粗成交量柱形图
        self.__volumeSeries.setBarWidth(1.4)
        macd_column_positive = QBarSet('red')
        macd_column_negative = QBarSet('green')
        macd_column.append(macd_column_positive)
        macd_column.append(macd_column_negative)
        # 设置线条颜色
        macd_white.setColor(Qt.white)
        macd_yellow.setColor(Qt.yellow)
        decorate_bar_series(macd_column_positive, Qt.darkRed)
        decorate_bar_series(macd_column_negative, Qt.darkGreen)

        # 添加数据
        i = 0
        for index, day_data in self.__stockData.iterrows():
            macd_white.append(i, day_data['macd_white'])
            macd_yellow.append(i, day_data['macd_yellow'])
            macd_column_positive.append(max(day_data['macd_column'], 0))
            macd_column_negative.append(min(day_data['macd_column'], 0))
            i += 1
        # 创建数值Y轴
        macd_axis = QValueAxis()
        macd_axis.setTickCount(3)
        # 寻找折线最大值确定显示范围
        max_abs = max(self.__stockData['macd_white'].abs().max(), self.__stockData['macd_yellow'].abs().max(), self.__stockData['macd_column'].abs().max())
        macd_axis.setMax(max_abs * 2)
        macd_axis.setMin(max_abs * -2)
        macd_axis.hide()
        self.__chart.addAxis(macd_axis, Qt.AlignRight)
        # 创建图表
        self.__chart.addSeries(macd_column)
        self.__chart.addSeries(macd_yellow)
        self.__chart.addSeries(macd_white)
        macd_white.attachAxis(macd_axis)
        macd_yellow.attachAxis(macd_axis)
        macd_column.attachAxis(macd_axis)

    # 画均线组合
    def plot_ma_pair(self, label_short: str,  label_long: str, use_different_axis: bool):
        ma_short = QLineSeries()
        ma_long = QLineSeries()
        # 设置均线颜色
        ma_short.setColor(Qt.white)
        ma_long.setColor(Qt.yellow)
        # 添加数据
        i = 0
        for index, day_data in self.__stockData.iterrows():
            ma_short.append(i, day_data[label_short])
            ma_long.append(i, day_data[label_long])
            i += 1
        # 创建图表
        self.__chart.addSeries(ma_long)
        self.__chart.addSeries(ma_short)
        # 是否拥有不同尺度的Y轴
        if use_different_axis:
            # 创建右侧Y轴显示数据
            y_axis = QValueAxis()
            y_axis.setTickCount(3)
            max_abs = max(self.__stockData[label_short].abs().max(), self.__stockData[label_long].abs().max())
            y_axis.setMax(max_abs * 1.5)
            y_axis.setMin(max_abs * -1.5)
            # 隐藏Y轴
            y_axis.hide()
            self.__chart.addAxis(y_axis, Qt.AlignRight)
            ma_short.attachAxis(y_axis)
            ma_long.attachAxis(y_axis)
        else:
            ma_short.attachAxis(self.__axis_price)
            ma_long.attachAxis(self.__axis_price)

    # 画单条均线
    def plot_ma(self, period: int, color):
        label = 'ma_' + str(period)
        ma_line = QLineSeries()
        ma_line.setColor(color)
        i = 0
        is_valid = False
        for index, day_data in self.__stockData.iterrows():
            # 避免部分数值因数据不够不存在
            if not math.isnan(day_data[label]):
                is_valid = True
                ma_line.append(i, day_data[label])
            elif i == 0:
                ma_line.append(i, 9999999)
            i += 1
        if is_valid:
            self.__chart.addSeries(ma_line)
            ma_line.attachAxis(self.__axis_price)

    # 画所有均线
    def plot_all_ma_lines(self):
        self.plot_ma(60, QColor(0, 127, 255))
        self.plot_ma(30, Qt.green)
        self.plot_ma(20, Qt.magenta)
        self.plot_ma(10, Qt.yellow)
        self.plot_ma(5, Qt.white)

        # 画出买卖记录
    def plot_trade_history(self, trade_history: StockInvestment, show_share_change=True):
        buy_history = QScatterSeries()
        sell_history = QScatterSeries()
        # 设置格式
        decorate_scatter_series(buy_history, 'B', QColor(255, 127, 0))
        decorate_scatter_series(sell_history, 'S', QColor(0, 255, 127))

        # 遍历买入记录
        for history in trade_history.buyTransactions:
            date = self.get_date_number(history.date)
            # 找不到日期，跳过此次交易
            if date == -1:
                continue
            buy_history.append(date, history.price)

        # 遍历卖出记录
        for history in trade_history.sellTransactions:
            date = self.get_date_number(history.date)
            # 找不到日期，跳过此次交易
            if date == -1:
                continue
            sell_history.append(date, history.price)

        if show_share_change:
            share_series = QLineSeries()
            share_series.setColor(QColor(255, 191, 127))
            max_share = last_share = 0
            # 记录每日的持仓情况
            for date, share in trade_history.shareAtDate.items():
                date_number = self.get_date_number(date)
                # 绘制阶梯型折线，确保昨日发生变化
                if date_number > 1:
                    share_series.append(date_number - 1, last_share)
                share_series.append(date_number, share)
                last_share = share
                # 获取最大持股数量
                if share > max_share:
                    max_share = share
            # 创建持仓量Y轴
            share_axis = QValueAxis()
            share_axis.setVisible(False)
            # 将持仓量折线置于最下方
            share_axis.setRange(0, max_share * 4)
            self.__chart.addAxis(share_axis, Qt.AlignRight)
            self.__chart.addSeries(share_series)
            share_series.attachAxis(share_axis)
            share_series.attachAxis(self.__axis_x)

        self.__chart.addSeries(buy_history)
        self.__chart.addSeries(sell_history)
        buy_history.attachAxis(self.__axis_price)
        buy_history.attachAxis(self.__axis_x)
        sell_history.attachAxis(self.__axis_price)
        sell_history.attachAxis(self.__axis_x)

    # 绘制选股日期标记
    def plot_search_date(self, date: str):
        search_mark = QScatterSeries()
        date_number = self.get_date_number(date)
        # 找不到日期，跳过
        if date_number == -1:
            return
        search_mark.append(date_number, self.__stockData['close'][date])
        # 设置格式
        decorate_scatter_series(search_mark, 'F', QColor(255, 255, 0), 20)
        self.__chart.addSeries(search_mark)
        search_mark.attachAxis(self.__axis_price)
        search_mark.attachAxis(self.__axis_x)

    # 通过日期获取第几个交易日
    def get_date_number(self, date: str):
        for i in range(len(self.__dates)):
            if date == self.__dates[i]:
                return i
        return -1


# 每日最高最低价的分布图
class PriceDistributionChart(QDialog, Ui_HistoryGraph):
    __axis_x = None
    __axis_y = None

    def __init__(self, stock_code: str, stock_data: pandas.DataFrame):
        super().__init__()
        self.setupUi(self)
        self.__stockCode = stock_code
        # 最大涨跌幅，若科创板则为20
        self.__value_range = 20 if 688000 <= int(stock_code) < 689000 else 10
        # 设定图表大小
        self.resize(500, 500)
        self.stockData = stock_data
        # 创建图表
        self.__chart = QChart()
        self.__chart.setBackgroundBrush(Qt.black)
        self.__chart.legend().hide()
        # 显示图表
        self.crtGraph.setChart(self.__chart)
        self.show()

    # 创建一个坐标轴
    def setup_axis(self, alignment, title: str):
        axis = QValueAxis()
        axis.setTickCount(3)
        axis.setGridLineColor(Qt.darkGray)
        axis.setLabelsColor(Qt.lightGray)
        axis.setTitleBrush(Qt.lightGray)
        axis.setTitleText(title)
        axis.setRange(-self.__value_range, self.__value_range)
        self.__chart.addAxis(axis, alignment)
        return axis

    # 创建序列
    def create_series(self, color):
        series = QScatterSeries()
        series.setMarkerSize(4)
        series.setColor(color)
        series.setBorderColor(color)
        self.__chart.addSeries(series)
        series.attachAxis(self.__axis_x)
        series.attachAxis(self.__axis_y)
        return series

    # 画最高最低分布图
    def plot_high_low_data(self):
        self.setWindowTitle(self.__stockCode + ' 最高最低涨跌幅分布')
        self.__axis_x = self.setup_axis(Qt.AlignBottom, '最低跌幅')
        self.__axis_y = self.setup_axis(Qt.AlignLeft, '最高涨幅')
        up_days = self.create_series(Qt.red)
        down_days = self.create_series(Qt.cyan)
        mid_days = self.create_series(Qt.white)
        for index, day_data in self.stockData.iterrows():
            day_low = day_data['low_pct']
            day_high = day_data['high_pct']
            # 收盘高于昨日收盘，红点
            if day_data['close_pct'] > 0:
                up_days.append(day_low, day_high)
            # 收盘低于昨日收盘，绿点
            elif day_data['close_pct'] < 0:
                down_days.append(day_low, day_high)
            # 收盘同于昨日收盘，白点
            else:
                mid_days.append(day_low, day_high)

    # 画开盘收盘分布图
    def plot_open_close_data(self):
        self.setWindowTitle(self.__stockCode + ' 开盘收盘涨跌幅分布')
        self.__axis_x = self.setup_axis(Qt.AlignBottom, '开盘涨跌幅')
        self.__axis_y = self.setup_axis(Qt.AlignLeft, '收盘涨跌幅')
        up_days = self.create_series(Qt.red)
        down_days = self.create_series(Qt.cyan)
        mid_days = self.create_series(Qt.white)
        for index, day_data in self.stockData.iterrows():
            day_open = day_data['open_pct']
            day_close = day_data['close_pct']
            # 收盘高于开盘，红点
            if day_close > day_open:
                up_days.append(day_open, day_close)
            # 收盘低于开盘，绿点
            elif day_close < day_open:
                down_days.append(day_open, day_close)
            # 平盘，白点
            else:
                mid_days.append(day_open, day_close)
