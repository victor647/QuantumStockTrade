from PyQt5.QtWidgets import QDialog
from PyQt5.QtChart import *
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QColor, QFont
from QtDesign.HistoryGraph_ui import Ui_HistoryGraph
from Data.InvestmentStatus import StockInvestment
import pandas, math


# 美化散点图
def decorate_scatter_series(series: QScatterSeries, text: str, color: QColor):
    series.setPointLabelsVisible(True)
    series.setPointLabelsFormat(text)
    series.setPointLabelsFont(QFont("Helvetica", 12, QFont.Bold))
    series.setPointLabelsColor(color)
    series.setMarkerSize(5)
    series.setColor(color)
    series.setBorderColor(Qt.gray)


# 美化柱状图
def decorate_bar_series(bar_set: QBarSet, color: QColor, transparent=False):
    # 设置颜色
    bar_set.setColor(Qt.transparent if transparent else color)
    bar_set.setBorderColor(color)


# 显示K线图
class HistoryGraph(QDialog, Ui_HistoryGraph):
    volumeSeries = None

    def __init__(self, code: str, stock_data: pandas.DataFrame, show_year=False):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(code + '走势：' + stock_data.index[0] + ' ~ ' + stock_data.index[-1])
        self.stockData = stock_data
        # 创建图表
        self.chart = QChart()
        self.chart.setBackgroundBrush(Qt.black)
        # 隐藏图例
        self.chart.legend().hide()
        # 初始化日期显示
        self.__dates = []
        for index, day_data in self.stockData.iterrows():
            self.__dates.append(index)
        # 创建日期x轴
        self.x_axis = QBarCategoryAxis()
        self.x_axis.setCategories(self.__dates)
        self.chart.addAxis(self.x_axis, Qt.AlignBottom)
        # 若日期过多，则创建专门的日期显示X轴
        if len(self.__dates) > 20:
            # 根据数据数量调节宽度
            self.resize(len(self.__dates) * 15 + 100, 550)
            self.setMinimumSize(len(self.__dates) * 10 + 250, 400)
            self.x_axis.hide()
            date_axis = QDateTimeAxis()
            date_axis.setTickCount(11)
            date_axis.setFormat('yy/MM/dd' if show_year else 'MM/dd')
            date_axis.setGridLineColor(Qt.black)
            date_axis.setLabelsColor(Qt.lightGray)
            date_axis.setMin(QDateTime.fromString(self.stockData.index[0], 'yyyy-MM-dd'))
            date_axis.setMax(QDateTime.fromString(self.stockData.index[-1], 'yyyy-MM-dd'))
            self.chart.addAxis(date_axis, Qt.AlignBottom)
        else:
            self.resize(500, 500)
            self.setMinimumSize(400, 400)
            self.x_axis.setGridLineColor(Qt.black)
            self.x_axis.setLabelsColor(Qt.lightGray)

        # 添加股价Y轴
        self.price_axis = QValueAxis()
        self.price_axis.setTickCount(9)
        self.price_axis.setGridLineColor(Qt.darkGray)
        self.price_axis.setLabelsColor(Qt.lightGray)
        self.chart.addAxis(self.price_axis, Qt.AlignLeft)
        # 显示图表
        self.crtGraph.setChart(self.chart)
        self.show()

    # 画股价蜡烛图
    def plot_price(self):
        price_series = QCandlestickSeries()
        # 设置蜡烛图颜色
        price_series.setDecreasingColor(Qt.cyan)
        price_series.setIncreasingColor(Qt.transparent)
        # 添加数据
        for index, day_data in self.stockData.iterrows():
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
        self.chart.addSeries(price_series)
        # 避开成交量图形区域
        max_price = self.stockData['high'].max()
        min_price = self.stockData['low'].min()
        self.price_axis.setMax(max_price)
        self.price_axis.setMin(min_price - (max_price - min_price) / 3)
        price_series.attachAxis(self.x_axis)
        price_series.attachAxis(self.price_axis)

    # 画成交量柱状图
    def plot_volume(self):
        self.volumeSeries = QStackedBarSeries()
        self.volumeSeries.setBarWidth(0.7)
        volume_bar_up = QBarSet('up')
        volume_bar_down = QBarSet('down')
        decorate_bar_series(volume_bar_up, Qt.red, True)
        decorate_bar_series(volume_bar_down, Qt.cyan)
        self.volumeSeries.append(volume_bar_up)
        self.volumeSeries.append(volume_bar_down)
        # 添加数据
        for index, day_data in self.stockData.iterrows():
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
        self.chart.addSeries(self.volumeSeries)
        # 创建成交量Y轴在右侧
        volume_axis = QValueAxis()
        volume_axis.setGridLineColor(Qt.darkGray)
        volume_axis.setLabelsColor(Qt.lightGray)
        volume_axis.setTickCount(9)
        # 将成交量图形置于最下方
        volume_axis.setMax(self.stockData['turn'].max() * 4)
        self.chart.addAxis(volume_axis, Qt.AlignRight)
        self.volumeSeries.attachAxis(volume_axis)
        self.volumeSeries.attachAxis(self.x_axis)

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
        for index, day_data in self.stockData.iterrows():
            boll_upper.append(i, day_data['boll_upper'])
            boll_middle.append(i, day_data['boll_middle'])
            boll_lower.append(i, day_data['boll_lower'])
            i += 1
        # 创建图表
        self.chart.addSeries(boll_upper)
        self.chart.addSeries(boll_middle)
        self.chart.addSeries(boll_lower)
        boll_upper.attachAxis(self.x_axis)
        boll_upper.attachAxis(self.price_axis)
        boll_middle.attachAxis(self.x_axis)
        boll_middle.attachAxis(self.price_axis)
        boll_lower.attachAxis(self.x_axis)
        boll_lower.attachAxis(self.price_axis)

    # 画MACD曲线
    def plot_macd(self):
        macd_white = QLineSeries()
        macd_yellow = QLineSeries()
        # 创建差值柱
        macd_column = QStackedBarSeries()
        macd_column.setBarWidth(0.1)
        # 增粗成交量柱形图
        self.volumeSeries.setBarWidth(1.4)
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
        for index, day_data in self.stockData.iterrows():
            macd_white.append(i, day_data['macd_white'])
            macd_yellow.append(i, day_data['macd_yellow'])
            macd_column_positive.append(max(day_data['macd_column'], 0))
            macd_column_negative.append(min(day_data['macd_column'], 0))
            i += 1
        # 创建数值Y轴
        macd_axis = QValueAxis()
        macd_axis.setTickCount(3)
        # 寻找折线最大值确定显示范围
        max_abs = max(self.stockData['macd_white'].abs().max(), self.stockData['macd_yellow'].abs().max(), self.stockData['macd_column'].abs().max())
        macd_axis.setMax(max_abs * 2)
        macd_axis.setMin(max_abs * -2)
        macd_axis.hide()
        self.chart.addAxis(macd_axis, Qt.AlignRight)
        # 创建图表
        self.chart.addSeries(macd_column)
        self.chart.addSeries(macd_yellow)
        self.chart.addSeries(macd_white)
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
        for index, day_data in self.stockData.iterrows():
            ma_short.append(i, day_data[label_short])
            ma_long.append(i, day_data[label_long])
            i += 1
        # 创建图表
        self.chart.addSeries(ma_long)
        self.chart.addSeries(ma_short)
        # 是否拥有不同尺度的Y轴
        if use_different_axis:
            # 创建右侧Y轴显示数据
            y_axis = QValueAxis()
            y_axis.setTickCount(3)
            max_abs = max(self.stockData[label_short].abs().max(), self.stockData[label_long].abs().max())
            y_axis.setMax(max_abs * 1.5)
            y_axis.setMin(max_abs * -1.5)
            # 隐藏Y轴
            y_axis.hide()
            self.chart.addAxis(y_axis, Qt.AlignRight)
            ma_short.attachAxis(y_axis)
            ma_long.attachAxis(y_axis)
        else:
            ma_short.attachAxis(self.price_axis)
            ma_long.attachAxis(self.price_axis)

    # 画单条均线
    def plot_ma(self, period: int, color):
        ma_line = QLineSeries()
        ma_line.setColor(color)
        label = 'ma_' + str(period)
        i = 0
        is_valid = False
        for index, day_data in self.stockData.iterrows():
            # 避免部分数值因数据不够不存在
            if not math.isnan(day_data[label]):
                is_valid = True
            ma_line.append(i, day_data[label])
            i += 1
        if is_valid:
            self.chart.addSeries(ma_line)
            ma_line.attachAxis(self.price_axis)

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
            self.chart.addAxis(share_axis, Qt.AlignRight)
            self.chart.addSeries(share_series)
            share_series.attachAxis(share_axis)
            share_series.attachAxis(self.x_axis)

        self.chart.addSeries(buy_history)
        self.chart.addSeries(sell_history)
        buy_history.attachAxis(self.price_axis)
        buy_history.attachAxis(self.x_axis)
        sell_history.attachAxis(self.price_axis)
        sell_history.attachAxis(self.x_axis)

    # 通过日期获取第几个交易日
    def get_date_number(self, date: str):
        for i in range(len(self.__dates)):
            if date == self.__dates[i]:
                return i
        return -1
