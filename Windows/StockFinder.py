from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow
from QtDesign.StockFinder_ui import Ui_StockFinder
from Windows.SearchResult import SearchResult
from Windows.ProgressBar import ProgressBar
import Data.FileManager as FileManager


class StockFinder(QMainWindow, Ui_StockFinder):
    searchResult = None
    isSearching = False
    stockSearcher = None
    progressBar = None

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.cbbConsecutiveTrend.addItems(['上涨', '下跌'])
        self.cbbAveragePriceComparison.addItems(['高于', '低于'])

    @staticmethod
    def export_all_stock_data():
        FileManager.export_all_stock_data()

    def search_all_stocks(self):
        stock_list = FileManager.read_stock_list_file()
        self.searchResult = SearchResult()
        self.searchResult.show()
        self.progressBar = ProgressBar(stock_list.shape[0])
        self.progressBar.show()
        self.stockSearcher = StockSearcher(self, stock_list)
        self.stockSearcher.progressBarCallback.connect(self.progressBar.update_search_progress)
        self.stockSearcher.addItemCallback.connect(self.searchResult.add_stock_item)
        self.stockSearcher.finishedCallback.connect(self.search_finished)
        self.stockSearcher.start()

    def search_finished(self):
        self.progressBar.close()
        self.searchResult.finish_searching()

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
        # 获得股票历史数据
        data = FileManager.read_stock_history_data(code)
        # 跳过当日停牌股票
        if data.iloc[-1]['tradestatus'] == 0:
            return False
        # 昨日成交量超过平均
        if self.cbxAverageVolume.isChecked():
            # 今日成交量
            volume = data.iloc[-1]['turn']
            # 均线成交量
            average_volume_period = self.spbAverageVolumePeriod.value() * -1
            average_volume = data['turn'][average_volume_period:-1].mean()
            if volume / average_volume < self.spbVolumeMultipler.value():
                return False

        # 股价连续上涨下跌
        if self.cbxConsecutiveTrend.isChecked():
            days = self.spbConsecutiveUpDays.value() * -1
            yesterday = data.iloc[days]['close']
            for i in range(days + 1, -1):
                today = data.iloc[i]['close']
                if self.cbbConsecutiveTrend.currentIndex() == 0:
                    if today < yesterday:
                        return False
                else:
                    if today > yesterday:
                        return False

        # 昨日股价偏离均线
        if self.cbxAveragePriceBias.isChecked():
            # 今日收盘价
            close = data.iloc[-1]['close']
            # 均线价格
            average_price_period = self.spbAveragePricePeriod.value() * -1
            average_price = data['close'][average_price_period:-1].mean()
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


class StockSearcher(QThread):
    isSearching = True
    addItemCallback = pyqtSignal(list)
    progressBarCallback = pyqtSignal(int, str, str)
    finishedCallback = pyqtSignal()

    def __init__(self, stock_finder, stock_list):
        super().__init__()
        self.stock_list = stock_list
        self.stockFinder = stock_finder

    def __del__(self):
        self.work = False
        self.terminate()

    def run(self):
        for index, row in self.stock_list.iterrows():
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
            self.progressBarCallback.emit(index, code, name)
            # 判断股票是否在选中的交易所中
            if not self.stockFinder.code_in_search_range(code_num):
                continue
            # 基本面指标考察
            if self.stockFinder.cbxCompanyInfoEnabled.isChecked() and not self.stockFinder.company_info_match_requirement(row):
                continue

            # 技术面指标考察
            if self.stockFinder.cbxTechnicalIndexEnabled.isChecked() and not self.stockFinder.technical_index_match_requirement(code):
                continue
            items = [code, name, pe, pb, assets]
            self.addItemCallback.emit(items)
        self.finishedCallback.emit()

