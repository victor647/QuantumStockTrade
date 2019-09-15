from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from QtDesign.StockFinder_ui import Ui_StockFinder
from Windows.SearchResult import SearchResult
from Windows.ProgressBar import ProgressBar
import Data.FileManager as FileManager
from datetime import datetime
import Windows.SearchCriteria as SearchCriteria
import os.path as path

stockFinderInstance = None


class StockFinder(QMainWindow, Ui_StockFinder):
    searchResult = None
    stockSearcher = None
    progressBar = None
    criteriaItems = []

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        global stockFinderInstance
        stockFinderInstance = self

    @staticmethod
    def export_all_stock_data():
        FileManager.export_all_stock_data()

    # 保存搜索条件
    def export_search_config(self):
        parent = path.join(path.pardir, "StockData", "SearchConfigs")
        file_path = QFileDialog.getSaveFileName(directory=parent, filter='JSON(*.json)')
        if file_path[0] != "":
            FileManager.export_search_config(self.criteriaItems, file_path[0])

    # 读取保存的搜索条件
    def import_search_config(self):
        parent = path.join(path.pardir, "StockData", "SearchConfigs")
        file_path = QFileDialog.getOpenFileName(directory=parent, filter='JSON(*.json)')
        if file_path[0] != "":
            self.criteriaItems = FileManager.import_search_config(file_path[0])
            self.update_criteria_list()

    # 更新搜索条件列表显示
    def update_criteria_list(self):
        self.lstCriteriaItems.clear()
        for item in self.criteriaItems:
            text = "过去" + str(item.daysCountFirst) + "日" + item.logic + item.field + item.operator
            if item.useAbsValue:
                text += str(item.absoluteValue)
            else:
                text += str(item.daysCountSecond) + "日平均" + str(item.relativePercentage) + "%"
            self.lstCriteriaItems.addItem(text)

    # 新增搜索条件
    def add_criteria_item(self):
        item = SearchCriteria.CriteriaItem()
        self.criteriaItems.append(item)
        window = SearchCriteria.SearchCriteria(item)
        window.show()
        window.exec()

    # 编辑所选搜索条件
    def modify_criteria_item(self):
        selection = self.lstCriteriaItems.selectedIndexes()
        if len(selection) == 0:
            return
        index = selection[0].row()
        item = self.criteriaItems[index]
        window = SearchCriteria.SearchCriteria(item)
        window.show()
        window.exec()

    # 删除所选搜索条件
    def remove_criteria_item(self):
        selection = self.lstCriteriaItems.selectedIndexes()
        if len(selection) == 0:
            return
        index = selection[0].row()
        self.criteriaItems.pop(index)
        self.update_criteria_list()

    # 重置搜索条件
    def reset_criteria_items(self):
        self.criteriaItems = []
        self.lstCriteriaItems.clear()

    # 搜索全部股票
    def search_all_stocks(self):
        stock_list = FileManager.read_stock_list_file()
        self.searchResult = SearchResult()
        self.searchResult.show()
        self.progressBar = ProgressBar(stock_list.shape[0])
        self.progressBar.show()
        self.stockSearcher = StockSearcher(stock_list)
        self.stockSearcher.progressBarCallback.connect(self.progressBar.update_search_progress)
        self.stockSearcher.addItemCallback.connect(self.searchResult.add_stock_item)
        self.stockSearcher.finishedCallback.connect(self.search_finished)
        self.stockSearcher.start()

    # 搜索完毕回调
    def search_finished(self):
        self.progressBar.close()
        self.searchResult.update_found_stock_count()

    # 基本面指标分析
    def company_info_match_requirement(self, row):
        # 检测股票是否是ST股
        if not self.cbxIncludeStStock.isChecked():
            name = row['name']
            if "ST" in name:
                return False

        # 检测股票是否为次新股
        if not self.cbxIncludeNewStock.isChecked():
            date = row['timeToMarket']
            # 去除还未上市的股票
            if date == 0:
                return False
            # 从数字获取日期
            start_date = datetime.strptime(str(date), "%Y%M%d")
            # 排除上市半年内股票
            if (datetime.today() - start_date).days < 180:
                return False

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

    # 技术面指标分析
    def technical_index_match_requirement(self, code):
        # 获得股票历史数据
        data = FileManager.read_stock_history_data(code)
        # 跳过当日停牌股票
        if data.iloc[-1]['tradestatus'] == 0:
            return False

        # 逐条筛选自定义指标
        for item in self.criteriaItems:
            if not SearchCriteria.match_criteria_item(data, item):
                return False
        return True

    # 检测股票是否在所选交易所中
    def code_in_search_range(self, code):
        # 上海主板
        if self.cbxShanghaiMain.isChecked() and 600000 <= code < 688000:
            return True
        # 深圳主板
        if self.cbxShenZhenMain.isChecked() and 0 <= code < 2000:
            return True
        # 中小板
        if self.cbxShenZhenSmall.isChecked() and 2000 <= code < 3000:
            return True
        # 创业板
        if self.cbxShenZhenNew.isChecked() and 300000 <= code < 301000:
            return True
        # 科创板
        if self.cbxShanghaiScience.isChecked() and 688000 <= code < 689000:
            return True
        return False


# 多线程股票搜索算法
class StockSearcher(QThread):
    addItemCallback = pyqtSignal(list)
    progressBarCallback = pyqtSignal(int, str, str)
    finishedCallback = pyqtSignal()

    def __init__(self, stock_list):
        super().__init__()
        self.stock_list = stock_list

    def __del__(self):
        self.work = False
        self.terminate()

    def run(self):
        for index, row in self.stock_list.iterrows():
            code_num = row['code']
            # 将股票代码固定为6位数
            code = str(code_num).zfill(6)
            # 获得股票中文名称
            name = row['name']
            # 更新窗口进度条
            self.progressBarCallback.emit(index, code, name)
            # 判断股票是否在选中的交易所中
            if not stockFinderInstance.code_in_search_range(code_num):
                continue
            # 基本面指标考察
            if stockFinderInstance.cbxCompanyInfoEnabled.isChecked() and not stockFinderInstance.company_info_match_requirement(row):
                continue
            # 技术面指标考察
            if stockFinderInstance.cbxTechnicalIndexEnabled.isChecked() and not stockFinderInstance.technical_index_match_requirement(code):
                continue
            # 获得股票市盈率
            pe = row['pe']
            # 获得股票市净率
            pb = row['pb']
            # 获得股票总市值
            assets = row['totalAssets']
            # 获得股票行业信息
            industry = row['industry']
            # 获得股票上市地区
            area = row['area']
            # 将符合要求的股票信息打包
            items = [code, name, industry, area, pe, pb, assets]
            # 添加股票信息至列表
            self.addItemCallback.emit(items)
        # 搜索结束回调
        self.finishedCallback.emit()
