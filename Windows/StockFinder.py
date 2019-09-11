from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from QtDesign.StockFinder_ui import Ui_StockFinder
from Windows.SearchResult import SearchResult
import tushare
import pandas


class StockFinder(QMainWindow, Ui_StockFinder):
    today = ""
    allStockData = []
    selectedStocks = []

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        now = QDate.currentDate()
        self.today = now.toString('yyyy-MM-dd')
        self.cbbPriceAverageComparison.addItems(['高于', '低于'])

    @staticmethod
    def get_all_stocks():
        all_stock_data = tushare.get_stock_basics()
        all_stock_data.to_csv('stock_data.csv')
        dialog = QMessageBox()
        dialog.setWindowTitle("成功")
        dialog.setText("已导出数据至stock_data.csv！")
        dialog.exec_()
        return

    def search_all_stocks(self):
        self.selectedStocks = []
        all_stock_data = pandas.read_csv('stock_data.csv')
        for index, row in all_stock_data.iterrows():
            code_num = row['code']
            # 判断股票是否在选中的交易所中
            if not self.code_in_search_range(code_num):
                continue
            # 基本面指标考察
            if not self.company_info_match_requirement(row):
                continue
            # 将股票代码固定为6位数
            code = str(code_num).zfill(6)

            if not self.technical_index_match_requirement(code):
                continue

            # 获得股票中文名称
            name = row['name']
            self.selectedStocks.append([code, name])

        search_result = SearchResult()
        search_result.show()
        search_result.get_stock_list(self.selectedStocks)
        search_result.exec()

    def company_info_match_requirement(self, row):
        # 检测股票市盈率是否符合范围
        if self.cbxPriceEarning.isChecked():
            pe = row['pe']
            if pe < self.spbPriceEarningMin.value() or pe > self.spbPriceEarningMax.value():
                return False

        # 检测股票市净率是否符合范围
        if self.cbxPriceBook.isChecked():
            pb = row['pb']
            if pb < self.spbPriceBookMin.value() or pb > self.spbPriceBookMax.value():
                return False

        # 检测股票总股本是否符合范围
        if self.cbxTotalShare.isChecked():
            totals = row['totals']
            if totals < self.spbTotalShareMin.value() or totals > self.spbTotalShareMax.value():
                return False

        # 检测股票总市值是否符合范围
        if self.cbxTotalAsset.isChecked():
            assets = row['totalAssets']
            if assets < self.spbTotalAssetsMin.value() or assets > self.spbTotalAssetsMax.value():
                return False
        return True

    def technical_index_match_requirement(self, code):
        # 昨日成交量超过平均
        # 股价连续上涨下跌
        # 昨日股价偏离均线
        if self.cbxAveragePriceBias.isChecked():
            # 获得股票今日数据
            data = tushare.get_hist_data(code, self.today)
            # 今日收盘价
            close = data.at[0, 'close']
            # 今日所选均线
            average = data.at[0, 'ma20']
            if self.cbbPriceAverageComparison.currentIndex() == 0:
                if (close / average - 1) * 100 < self.spbPriceDeviation.value():
                    return False
            else:
                if (close / average - 1) * 100 > self.spbPriceDeviation.value():
                    return False
        return True

    def code_in_search_range(self, code):
        if self.cbxShanghaiMain.isChecked() and 600000 <= code < 688000:
            return True
        if self.cbxShenZhenMain.isChecked() and 0 <= code < 2000:
            return True
        if self.cbxShenZhenSmall.isChecked() and 2000 <= code < 3000:
            return True
        if self.cbxShenZhenNew.isChecked() and 300000 <= code < 301000:
            return True
        if self.cbxShanghaiScience.isChecked() and 688000 <= code < 689000:
            return True
        return False

