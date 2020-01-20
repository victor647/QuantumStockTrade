from PyQt5.QtWidgets import QDialog
from PyQt5.QtChart import QCandlestickSeries, QCandlestickSet, QBarSeries, QStackedBarSeries, QBarSet, QChart, QValueAxis, QBarCategoryAxis, QLineSeries
from PyQt5.QtCore import Qt
from QtDesign.HistoryGraph_ui import Ui_HistoryGraph
import pandas


# 显示K线图
class HistoryGraph(QDialog, Ui_HistoryGraph):

    def __init__(self, code: str, stock_data: pandas.DataFrame):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(code + '走势：' + stock_data.index[0] + ' ~ ' + stock_data.index[-1])
        self.stockData = stock_data
        # 创建图表
        self.chart = QChart()
        # 隐藏图例
        self.chart.legend().hide()
        # 初始化日期显示
        dates = []
        for index, day_data in self.stockData.iterrows():
            dates.append(index[5:])
        # 创建日期x轴
        self.x_axis = QBarCategoryAxis()
        self.x_axis.setCategories(dates)
        self.chart.addAxis(self.x_axis, Qt.AlignBottom)
        # 添加股价Y轴
        self.price_axis = QValueAxis()
        self.price_axis.setTickCount(6)
        self.chart.addAxis(self.price_axis, Qt.AlignLeft)
        # 根据数据数量决定是否隐藏x轴
        if len(dates) > 20:
            self.x_axis.hide()
        # 显示图表
        self.crtGraph.setChart(self.chart)
        self.show()

    # 画股价蜡烛图
    def plot_price(self):
        price_series = QCandlestickSeries()
        # 设置蜡烛图颜色
        price_series.setDecreasingColor(Qt.darkGreen)
        price_series.setIncreasingColor(Qt.red)
        # 添加数据
        for index, day_data in self.stockData.iterrows():
            price_series.append(QCandlestickSet(day_data['open'], day_data['high'], day_data['low'], day_data['close']))
        # 创建图表
        self.chart.addSeries(price_series)
        # 避开成交量图形区域
        max_price = self.stockData['high'].max()
        min_price = self.stockData['low'].min()
        self.price_axis.setMax(max_price)
        self.price_axis.setMin(min_price - (max_price - min_price) * 0.2)
        price_series.attachAxis(self.x_axis)
        price_series.attachAxis(self.price_axis)

    # 画成交量柱状图
    def plot_volume(self):
        volume_series = QStackedBarSeries()
        volume_bar = QBarSet('换手率')
        volume_series.append(volume_bar)
        # 添加数据
        for index, day_data in self.stockData.iterrows():
            volume_bar.append(round(day_data['turn'], 2))
        self.chart.addSeries(volume_series)
        # 创建成交量Y轴在右侧
        volume_axis = QValueAxis()
        volume_axis.setTickCount(6)
        # 将成交量图形置于最下方
        volume_axis.setMax(self.stockData['turn'].max() * 5)
        self.chart.addAxis(volume_axis, Qt.AlignRight)
        volume_series.attachAxis(volume_axis)
        volume_series.attachAxis(self.x_axis)

    # 画布林线轨道
    def plot_boll(self):
        boll_upper = QLineSeries()
        boll_middle = QLineSeries()
        boll_lower = QLineSeries()
        # 设置轨道颜色
        boll_upper.setColor(Qt.darkYellow)
        boll_middle.setColor(Qt.gray)
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
        macd_column.setBarWidth(0.5)
        macd_column_positive = QBarSet('')
        macd_column_negative = QBarSet('')
        macd_column.append(macd_column_positive)
        macd_column.append(macd_column_negative)
        # 设置线条颜色
        macd_white.setColor(Qt.gray)
        macd_yellow.setColor(Qt.darkYellow)
        macd_column_positive.setColor(Qt.red)
        macd_column_negative.setColor(Qt.green)

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

    # 画均线
    def plot_ma(self, label_short: str, label_long: str, separate_axis: bool):
        ma_short = QLineSeries()
        ma_long = QLineSeries()
        # 设置均线颜色
        ma_short.setColor(Qt.gray)
        ma_long.setColor(Qt.darkYellow)
        # 添加数据
        i = 0
        for index, day_data in self.stockData.iterrows():
            ma_short.append(i, day_data[label_short])
            ma_long.append(i, day_data[label_long])
            i += 1
        # 创建图表
        self.chart.addSeries(ma_long)
        self.chart.addSeries(ma_short)
        if separate_axis:
            y_axis = QValueAxis()
            y_axis.setTickCount(3)
            max_abs = max(self.stockData[label_short].abs().max(), self.stockData[label_long].abs().max())
            y_axis.setMax(max_abs * 1.5)
            y_axis.setMin(max_abs * -1.5)
            y_axis.hide()
            self.chart.addAxis(y_axis, Qt.AlignRight)
            ma_short.attachAxis(y_axis)
            ma_long.attachAxis(y_axis)
        else:
            ma_short.attachAxis(self.price_axis)
            ma_long.attachAxis(self.price_axis)
