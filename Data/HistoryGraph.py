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
        # 创建两个图表
        self.mainChart = QChart()
        self.secondaryChart = QChart()
        # 隐藏图例
        self.mainChart.legend().hide()
        self.secondaryChart.legend().hide()
        # 初始化日期显示
        dates = []
        for index, day_data in self.stockData.iterrows():
            dates.append(index[5:])
        # 创建日期x轴
        self.x_axis_main = QBarCategoryAxis()
        self.x_axis_secondary = QBarCategoryAxis()
        self.x_axis_main.setCategories(dates)
        self.x_axis_secondary.setCategories(dates)
        self.x_axis_secondary.setTitleText(stock_data.index[0] + ' ~ ' + stock_data.index[-1])
        self.mainChart.addAxis(self.x_axis_main, Qt.AlignTop)
        self.secondaryChart.addAxis(self.x_axis_secondary, Qt.AlignBottom)
        # 添加股价Y轴
        self.price_axis = QValueAxis()
        self.price_axis.setTickCount(6)
        self.mainChart.addAxis(self.price_axis, Qt.AlignLeft)
        # 显示图表
        self.crtMainGraph.setChart(self.mainChart)
        self.crtSecondaryGraph.setChart(self.secondaryChart)
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
        self.mainChart.addSeries(price_series)
        # 避开成交量图形区域
        max_price = self.stockData['high'].max()
        min_price = self.stockData['low'].min()
        self.price_axis.setMax(max_price)
        self.price_axis.setMin(min_price - (max_price - min_price) * 0.2)
        price_series.attachAxis(self.x_axis_main)
        price_series.attachAxis(self.price_axis)

    # 画成交量柱状图
    def plot_volume(self):
        volume_series = QBarSeries()
        volume_bar = QBarSet('换手率')
        volume_series.append(volume_bar)
        # 添加数据
        for index, day_data in self.stockData.iterrows():
            volume_bar.append(round(day_data['turn'], 2))
        self.mainChart.addSeries(volume_series)
        # 创建成交量Y轴在右侧
        volume_axis = QValueAxis()
        volume_axis.setTickCount(6)
        # 将成交量图形置于最下方
        volume_axis.setMax(self.stockData['turn'].max() * 5)
        self.mainChart.addAxis(volume_axis, Qt.AlignRight)
        volume_series.attachAxis(volume_axis)
        volume_series.attachAxis(self.x_axis_main)

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
        self.mainChart.addSeries(boll_upper)
        self.mainChart.addSeries(boll_middle)
        self.mainChart.addSeries(boll_lower)
        boll_upper.attachAxis(self.x_axis_main)
        boll_upper.attachAxis(self.price_axis)
        boll_middle.attachAxis(self.x_axis_main)
        boll_middle.attachAxis(self.price_axis)
        boll_lower.attachAxis(self.x_axis_main)
        boll_lower.attachAxis(self.price_axis)

    # 画MACD曲线
    def plot_macd(self):
        macd_white = QLineSeries()
        macd_yellow = QLineSeries()
        # 创建差值柱
        macd_column = QBarSeries()
        macd_column_positive = QBarSet('')
        macd_column_negative = QBarSet('')
        macd_column.append(macd_column_positive)
        macd_column.append(macd_column_negative)
        # 设置轨道颜色
        macd_yellow.setColor(Qt.darkYellow)
        macd_white.setColor(Qt.darkGray)
        macd_column_positive.setColor(Qt.red)
        macd_column_negative.setColor(Qt.darkGreen)

        # 添加数据
        i = 0
        for index, day_data in self.stockData.iterrows():
            macd_white.append(i, day_data['macd_white'])
            macd_yellow.append(i, day_data['macd_yellow'])
            macd_column_positive.append(max(day_data['macd_column'], 0))
            macd_column_negative.append(min(day_data['macd_column'], 0))
            i += 1
        # 创建成交量Y轴在右侧
        macd_axis = QValueAxis()
        macd_axis.setTickCount(3)
        # 寻找折线最大值确定显示范围
        max_abs = self.stockData['macd_white'].abs().max()
        macd_axis.setMax(max_abs * 1.2)
        macd_axis.setMin(max_abs * -1.2)
        self.secondaryChart.addAxis(macd_axis, Qt.AlignLeft)
        # 创建图表
        self.secondaryChart.addSeries(macd_white)
        self.secondaryChart.addSeries(macd_yellow)
        self.secondaryChart.addSeries(macd_column)
        macd_white.attachAxis(self.x_axis_main)
        macd_white.attachAxis(macd_axis)
        macd_yellow.attachAxis(self.x_axis_main)
        macd_yellow.attachAxis(macd_axis)
        macd_column.attachAxis(self.x_axis_main)
        macd_column.attachAxis(macd_axis)
