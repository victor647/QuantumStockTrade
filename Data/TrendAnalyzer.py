import baostock, pandas
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView
from QtDesign.TrendAnalyzer_ui import Ui_TrendAnalyzer
import Data.TechnicalAnalysis as TA
from Data.HistoryGraph import CandleStickChart, PriceDistributionChart
from Tools import Tools


# 股票趋势高低点
class HighLowPoint:
    type = ''
    date = ''
    # 涨跌天数
    totalDays = 0
    upDays = 0
    downDays = 0
    flatDays = 0
    price = 0
    percentChange = 0
    biasFromAverage = 0


# 分析个股趋势和箱体
class TrendAnalyzer(QMainWindow, Ui_TrendAnalyzer):
    highLowPoints = []

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup_triggers()
        self.tblHighLowPoints.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    # 分析K线得到趋势箱体统计
    def calculate_trends(self):
        self.tblHighLowPoints.setRowCount(0)
        self.highLowPoints = []

        total_days = self.stockDatabase.shape[0]
        for base_index in range(total_days):
            base_high = self.stockDatabase.iloc[base_index]['high']
            base_low = self.stockDatabase.iloc[base_index]['low']
            is_high = is_low = True
            # 遍历前后十天的情况
            for index in range(base_index - 10, base_index + 10):
                if index < 0 or index >= total_days:
                    continue
                if is_high and self.stockDatabase.iloc[index]['high'] > base_high:
                    is_high = False
                if is_low and self.stockDatabase.iloc[index]['low'] < base_low:
                    is_low = False
                if not is_high and not is_low:
                    break
            if is_high:
                self.add_high_low_point(self.stockDatabase.index[base_index], '高点')
            elif is_low:
                self.add_high_low_point(self.stockDatabase.index[base_index], '低点')

    # 趋势发生改变
    def add_high_low_point(self, date: str, point_type: str):
        point = HighLowPoint()
        point.date = date
        point.type = point_type
        # 根据高低点类型决定价格取值
        if point_type == '高点':
            point.price = self.stockDatabase.loc[date]['high']
        else:
            point.price = self.stockDatabase.loc[date]['low']
        point.biasFromAverage = TA.get_percent_change_from_price(point.price, self.stockDatabase.loc[date]['ma_5'])

        if len(self.highLowPoints) > 0:
            last_point = self.highLowPoints[-1]
            # 避免出现连续同种趋势
            if last_point.type == point_type:
                return
            period = self.stockDatabase[last_point.date:date]
            start_price = last_point.price
        else:
            period = self.stockDatabase[:date]
            start_price = self.stockDatabase.iloc[0]['open']

        for index, day_data in period.iterrows():
            # 计算趋势内涨跌日数
            day_close = round(day_data['close'], 2)
            day_open = round(day_data['open'], 2)
            if day_close > day_open:
                point.upDays += 1
            elif day_close < day_open:
                point.downDays += 1
            else:
                point.flatDays += 1
            point.totalDays += 1
        # 计算累计涨跌幅
        point.percentChange = TA.get_percent_change_from_price(point.price, start_price)

        self.highLowPoints.append(point)
        self.set_points_table(point)

    # 在图表中添加一个趋势
    def set_points_table(self, point: HighLowPoint):
        row = self.tblHighLowPoints.rowCount()
        self.tblHighLowPoints.insertRow(row)
        # 出现日期
        self.tblHighLowPoints.setItem(row, 0, QTableWidgetItem(point.date))
        # 高低点类型
        self.tblHighLowPoints.setItem(row, 1, QTableWidgetItem(point.type))
        # 最高最低价格
        column = 2
        column = Tools.add_sortable_item(self.tblHighLowPoints, row, column, round(point.price, 2))
        # 偏离MA5
        column = Tools.add_colored_item(self.tblHighLowPoints, row, column, point.biasFromAverage, '%')
        # 波段时长
        column = Tools.add_sortable_item(self.tblHighLowPoints, row, column, point.totalDays)
        # 涨跌天数
        days_string = str(point.upDays) + '-' + str(point.downDays) + '-' + str(point.flatDays)
        column = Tools.add_sortable_item(self.tblHighLowPoints, row, column, point.upDays, days_string)
        # 累计涨跌幅
        column = Tools.add_colored_item(self.tblHighLowPoints, row, column, point.percentChange, '%')