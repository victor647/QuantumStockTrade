from PyQt5.QtWidgets import QDialog
from PyQt5.QtChart import QCandlestickSeries, QCandlestickSet, QBarSeries, QBarSet, QChart, QValueAxis, QBarCategoryAxis, QLineSeries
from PyQt5.QtCore import Qt
from QtDesign.HistoryGraph_ui import Ui_HistoryGraph
import pandas


# 显示K线图
class HistoryGraph(QDialog, Ui_HistoryGraph):

    def __init__(self, code: str, stock_data: pandas.DataFrame):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(code)
        self.stockData = stock_data
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
        self.x_axis.setTitleText(stock_data.index[0] + ' ~ ' + stock_data.index[-1])
        self.chart.addAxis(self.x_axis, Qt.AlignBottom)
        # 添加股价Y轴
        self.price_axis = QValueAxis()
        self.price_axis.setTickCount(6)
        self.chart.addAxis(self.price_axis, Qt.AlignLeft)
        # 显示图表
        self.crtCandleStick.setChart(self.chart)
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
        volume_series = QBarSeries()
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
        boll_middle.setColor(Qt.darkGray)
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
