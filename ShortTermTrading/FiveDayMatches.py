from QtDesign.FiveDayMatches_ui import Ui_FiveDayMatches
from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt
from Libraries import Tools
import Data.HistoryGraph as HistoryGraph


# 五日选股结果列表
class FiveDayMatches(QDialog, Ui_FiveDayMatches):
    __totalFiveDayPerformance = 0

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 为表格自动设置列宽
        self.tblMatches.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    # 显示股票详细数据
    def stock_detailed_info(self, row: int, column: int):
        stock_code = self.tblMatches.item(row, 0).text()
        # 通过网页打开
        if column < 2:
            Tools.open_stock_page(stock_code)
        # 直接画K线图
        else:
            HistoryGraph.plot_stock_search_and_trade(stock_code, self.tblMatches.item(row, 2).text())

    # 更新已找到的股票数量
    def update_matches_count(self, average_performance: float):
        self.lblMatchesSummary.setText('共出现{}次图形匹配，出现后平均5日涨幅{}%'.format(self.tblMatches.rowCount(), average_performance))

    # 在列表中添加一只找到的股票
    def add_match(self, items: list):
        row_count = self.tblMatches.rowCount()
        self.tblMatches.insertRow(row_count)
        for i in range(len(items)):
            # 涨跌幅百分比显示
            if i > 2:
                Tools.add_colored_item(self.tblMatches, row_count, i, items[i], '%')
            # 其他字符串格式数据
            else:
                item = QTableWidgetItem()
                item.setData(Qt.DisplayRole, items[i])
                self.tblMatches.setItem(row_count, i, item)
        # 计算平均五日表现
        self.__totalFiveDayPerformance += items[-2]
        self.update_matches_count(round(self.__totalFiveDayPerformance / (row_count + 1), 2))
