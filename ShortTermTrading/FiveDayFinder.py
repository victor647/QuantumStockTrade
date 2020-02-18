from QtDesign.FiveDaysFinder_ui import Ui_FiveDayShapeFinder
from PyQt5.QtWidgets import QDialog


# 根据五日图形选股
class FiveDayFinder(QDialog, Ui_FiveDayShapeFinder):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.cbbQueryField.addItems(['开盘涨跌幅', '收盘涨跌幅', '日内涨跌幅', '最高涨幅', '最低跌幅', '振幅', '换手率'])

    # 开始寻找图形
    def start_searching(self):
        if self.rbnSingleStock.isChecked():
            self.search_single_stock()
        if self.rbnAllStocks.isChecked():
            self.search_all_stocks()

    # 在单只股票中寻找不同日期
    def search_single_stock(self):

    # 在全部股票中寻找同一日期
    def search_all_stocks(self):
