from PyQt5.QtCore import QDate, QThread
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from QtDesign.StockFinder_ui import Ui_StockFinder
import Windows.SearchResult as SearchResult
import tushare
import pandas


class StockFinder(QMainWindow, Ui_StockFinder):
    today = ""
    startDate = ""
    allStockData = []
    searchResult = None
    isSearching = False
    stockSearcher = None

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        now = QDate.currentDate()
        start_date = now.addMonths(-1)
        self.today = now.toString('yyyy-MM-dd')
        self.startDate = start_date.toString('yyyy-MM-dd')
        self.cbbConsecutiveTrend.addItems(['上涨', '下跌'])
        self.cbbAveragePriceComparison.addItems(['高于', '低于'])
        self.cbbAverageVolumePeriod.addItems(['5日平均', '10日平均', '20日平均'])
        self.cbbAveragePricePeriod.addItems(['5日均线', '10日均线', '20日均线'])

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
        all_stock_data = pandas.read_csv('stock_data.csv')
        self.stockSearcher = StockSearcher(self, all_stock_data)
        self.show_search_result(all_stock_data.shape[0])
        self.stockSearcher.start()

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
        # 获得股票今日数据
        data = tushare.get_hist_data(code, self.startDate, self.today)
        # 跳过当日停牌股票
        if self.today not in data.index:
            return False
        # 昨日成交量超过平均
        if self.cbxAverageVolume.isChecked():
            # 今日成交量
            volume = data.loc[self.today, 'volume']
            # 均线成交量
            average_volume = data.loc[self.today, 'v_ma20']
            if self.cbbAverageVolumePeriod.currentIndex() == 0:
                average_volume = data.loc[self.today, 'v_ma5']
            elif self.cbbAverageVolumePeriod.currentIndex() == 1:
                average_volume = data.loc[self.today, 'v_ma10']

            if volume / average_volume < self.spbVolumeMultipler.value():
                return False

        # 股价连续上涨下跌

        # 昨日股价偏离均线
        if self.cbxAveragePriceBias.isChecked():
            # 今日收盘价
            close = data.loc[self.today, 'close']
            # 均线价格
            average_price = data.loc[self.today, 'ma20']
            if self.cbbAveragePricePeriod.currentIndex() == 0:
                average_price = data.loc[self.today, 'ma5']
            elif self.cbbAveragePricePeriod.currentIndex() == 1:
                average_price = data.loc[self.today, 'ma10']

            if self.cbbAveragePriceComparison.currentIndex() == 0:
                if (close / average_price - 1) * 100 < self.spbPriceDeviation.value():
                    return False
            else:
                if (close / average_price - 1) * 100 > self.spbPriceDeviation.value():
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

    def show_search_result(self, count):
        self.searchResult = SearchResult.SearchResult()
        self.searchResult.show()
        self.searchResult.totalStockCount = count
        self.searchResult.stockSearcher = self.stockSearcher


class StockSearcher(QThread):
    allStockData = None
    stockFinder = None
    isSearching = True

    def __init__(self, stock_finder, all_stock_data):
        super().__init__()
        self.allStockData = all_stock_data
        self.stockFinder = stock_finder

    def __del__(self):
        self.work = False
        self.terminate()

    def run(self):
        for index, row in self.allStockData.iterrows():
            if not self.isSearching:
                break
            code_num = row['code']
            # 将股票代码固定为6位数
            code = str(code_num).zfill(6)
            # 获得股票中文名称
            name = row['name']
            # 获得股票市盈率
            pe = row['pe']
            # 获得股票市净率
            pb = row['pb']
            # 获得股票总市值
            assets = row['totalAssets']
            self.stockFinder.searchResult.update_search_progress(index, code, name)
            # 判断股票是否在选中的交易所中
            if not self.stockFinder.code_in_search_range(code_num):
                continue
            # 基本面指标考察
            if self.stockFinder.cbxCompanyInfoEnabled.isChecked() and not self.stockFinder.company_info_match_requirement(row):
                continue

            # 技术面指标考察
            if self.stockFinder.cbxTechnicalIndexEnabled.isChecked() and not self.stockFinder.technical_index_match_requirement(code):
                continue
            self.stockFinder.searchResult.add_stock_item(code, name, pe, pb, assets)

        self.stockFinder.searchResult.finish_searching()
