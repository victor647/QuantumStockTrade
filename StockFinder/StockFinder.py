from PyQt5.QtCore import QThread, pyqtSignal, Qt, QDate
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QListWidgetItem
from PyQt5.QtGui import QKeyEvent
from QtDesign.StockFinder_ui import Ui_StockFinder
from StockFinder.SearchResult import SearchResult
from Windows.ProgressBar import ProgressBar
import FileManager as FileManager
from datetime import datetime
import StockFinder.SearchCriteria as SearchCriteria
import tushare


stockFinderInstance = None


class StockFinder(QMainWindow, Ui_StockFinder):
    __searchResult = None
    __stockSearcher = None
    __progressBar = None
    __criteriaItems = []

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 初始化单例
        global stockFinderInstance
        stockFinderInstance = self

    # 快捷键设置
    def keyPressEvent(self, key: QKeyEvent):
        # Esc键清除选择
        if key.key() == Qt.Key_Escape:
            self.lstCriteriaItems.clearSelection()
        # 按删除键删除股票或指标组
        elif key.key() == Qt.Key_Delete or key.key() == Qt.Key_Backspace:
            self.remove_criteria_item()

    # 根据十大流通股东结构选股
    @staticmethod
    def search_by_holders_structure():
        # pro = tushare.pro_api('eee03f328c31ce7b74e1f0417863e4019723e9bdda3fb0d243cf9a1c')
        stock_list = FileManager.read_stock_list_file()
        today = QDate.currentDate()
        year = today.year()
        month = today.month()
        quarter = 4
        if month < 4:
            year -= 1
        elif month < 7:
            quarter = 1
        elif month < 10:
            quarter = 2
        else:
            quarter = 3

        search_result = []
        for index, row_stock in stock_list.iterrows():
            code_num = row_stock['code']
            code = str(code_num).zfill(6)
            data = tushare.top10_holders(code=code, year=year, quarter=quarter)[1]
            data['h_pro'] = data['h_pro'].astype(float)
            under_five = data[data['h_pro'] < 5]
            # 单人持股比例超过3%的跳过
            if under_five['h_pro'].max() > 3:
                continue
            count = 0
            for i, row_holder in under_five.iterrows():
                # 排除公司持股和限售情况
                if "有限公司" in row_holder['name'] or row_holder['sharetype'] == "限售流通股":
                    continue
                count += 1
                # 股权结构优秀，加入选中列表
                if count >= 5:
                    search_result.append(code)
                    break
            if index > 100:
                break

        file_path = QFileDialog.getSaveFileName(directory=FileManager.selected_stock_list_path(), filter='TXT(*.txt)')
        if file_path[0] != "":
            file = open(file_path[0], "w")
            for code in search_result:
                file.write(code + "\n")
            file.close()


    # 获取并导出全部股票信息
    @staticmethod
    def export_all_stock_data():
        FileManager.export_all_stock_data()

    # 保存基本面指标搜索条件
    def export_company_config(self):
        file_path = QFileDialog.getSaveFileName(directory=FileManager.search_config_path(), filter='JSON(*.json)')
        data = {
            "peOn": self.cbxPriceEarning.isChecked(),
            "peMin": self.spbPriceEarningMin.value(),
            "peMax": self.spbPriceEarningMax.value(),
            "pbOn": self.cbxPriceBook.isChecked(),
            "pbMin": self.spbPriceBookMin.value(),
            "pbMax": self.spbPriceBookMax.value(),
            "totalShareOn": self.cbxTotalShare.isChecked(),
            "totalShareMin": self.spbTotalShareMin.value(),
            "totalShareMax": self.spbTotalShareMax.value(),
            "totalAssetsOn": self.cbxTotalAssets.isChecked(),
            "totalAssetsMin": self.spbTotalAssetsMin.value(),
            "totalAssetsMax": self.spbTotalAssetsMax.value(),
            "grossProfitOn": self.cbxGrossProfit.isChecked(),
            "grossProfit": self.spbGrossProfit.value(),
            "netProfitOn": self.cbxNetProfit.isChecked(),
            "netProfit": self.spbNetProfit.value(),
            "incomeIncreaseOn": self.cbxIncomeIncrease.isChecked(),
            "incomeIncrease": self.spbIncomeIncrease.value(),
            "profitIncreaseOn": self.cbxProfitIncrease.isChecked(),
            "profitIncrease": self.spbProfitIncrease.value(),
            "netAssetProfitOn": self.cbxNetAssetProfit.isChecked(),
            "netAssetProfit": self.spbNetAssetProfit.value(),
            "totalHoldersOn": self.cbxTotalHolders.isChecked(),
            "totalHoldersMin": self.spbTotalHoldersMin.value(),
            "totalHoldersMax": self.spbTotalHoldersMax.value(),
            "includeSt": self.cbxIncludeStStock.isChecked(),
            "includeNew": self.cbxIncludeNewStock.isChecked(),
        }
        if file_path[0] != "":
            FileManager.export_config_as_json(data, file_path[0])

    def import_company_config(self):
        file_path = QFileDialog.getOpenFileName(directory=FileManager.search_config_path(), filter='JSON(*.json)')
        if file_path[0] != "":
            data = FileManager.import_json_config(file_path[0])
            self.cbxPriceEarning.setChecked(data['peOn'])
            self.spbPriceEarningMin.setValue(data['peMin'])
            self.spbPriceEarningMax.setValue(data['peMax'])
            self.cbxPriceBook.setChecked(data['pbOn'])
            self.spbPriceBookMin.setValue(data['pbMin'])
            self.spbPriceBookMax.setValue(data['pbMax'])
            self.cbxTotalShare.setChecked(data['totalShareOn'])
            self.spbTotalShareMin.setValue(data['totalShareMin'])
            self.spbTotalShareMax.setValue(data['totalShareMax'])
            self.cbxTotalAssets.setChecked(data['totalAssetsOn'])
            self.spbTotalAssetsMin.setValue(data['totalAssetsMin'])
            self.spbTotalAssetsMax.setValue(data['totalAssetsMax'])
            self.cbxGrossProfit.setChecked(data['grossProfitOn'])
            self.spbGrossProfit.setValue(data['grossProfit'])
            self.cbxNetProfit.setChecked(data['netProfitOn'])
            self.spbNetProfit.setValue(data['netProfit'])
            self.cbxIncomeIncrease.setChecked(data['incomeIncreaseOn'])
            self.spbIncomeIncrease.setValue(data['incomeIncrease'])
            self.cbxProfitIncrease.setChecked(data['profitIncreaseOn'])
            self.spbProfitIncrease.setValue(data['profitIncrease'])
            self.cbxNetAssetProfit.setChecked(data['netAssetProfitOn'])
            self.spbNetAssetProfit.setValue(data['netAssetProfit'])
            self.cbxTotalHolders.setChecked(data['totalHoldersOn'])
            self.spbTotalHoldersMin.setValue(data['totalHoldersMin'])
            self.spbTotalHoldersMax.setValue(data['totalHoldersMax'])
            self.cbxIncludeStStock.setChecked(data['includeSt'])
            self.cbxIncludeNewStock.setChecked(data['includeNew'])

    # 保存技术指标搜索条件
    def export_technical_config(self):
        file_path = QFileDialog.getSaveFileName(directory=FileManager.search_config_path(), filter='JSON(*.json)')
        if file_path[0] != "":
            FileManager.export_config_as_json(self.__criteriaItems, file_path[0])

    # 读取保存的技术指标搜索条件
    def import_technical_config(self):
        file_path = QFileDialog.getOpenFileName(directory=FileManager.search_config_path(), filter='JSON(*.json)')
        if file_path[0] != "":
            self.__criteriaItems = FileManager.import_json_config(file_path[0], SearchCriteria.import_criteria_item)
            self.update_criteria_list()

    # 更新搜索条件列表显示
    def update_criteria_list(self, edited_item=None):
        # 添加条件时
        if edited_item is not None and edited_item not in self.__criteriaItems:
            self.__criteriaItems.append(edited_item)
        # 重新生成图表
        self.lstCriteriaItems.clear()
        for item in self.__criteriaItems:
            operator = "<" if item.operator == "小于" else ">"
            text = "最近" + str(item.daysCountFirst) + "日" + item.queryLogic + item.field + operator
            if item.useAbsValue:
                text += str(item.absoluteValue)
            else:
                text += "最近" + str(item.daysCountSecond) + "日" + item.comparedLogic + item.field + "×" + str(item.relativePercentage) + "%"
            self.lstCriteriaItems.addItem(text)

    # 新增搜索条件
    def add_criteria_item(self):
        item = SearchCriteria.CriteriaItem()
        window = SearchCriteria.SearchCriteria(item)
        window.show()
        window.exec()

    # 双击编辑所选搜索条件
    def edit_selected_item(self, item: QListWidgetItem):
        index = self.lstCriteriaItems.indexFromItem(item)
        window = SearchCriteria.SearchCriteria(self.__criteriaItems[index.row()])
        window.show()
        window.exec()

    # 编辑所选搜索条件
    def modify_criteria_item(self):
        selection = self.lstCriteriaItems.selectedIndexes()
        if len(selection) == 0:
            return
        index = selection[0].row()
        item = self.__criteriaItems[index]
        window = SearchCriteria.SearchCriteria(item)
        window.show()
        window.exec()

    # 删除所选搜索条件
    def remove_criteria_item(self):
        selection = self.lstCriteriaItems.selectedIndexes()
        if len(selection) == 0:
            return
        index = selection[0].row()
        self.__criteriaItems.pop(index)
        self.update_criteria_list()

    # 重置搜索条件
    def reset_criteria_items(self):
        self.__criteriaItems = []
        self.lstCriteriaItems.clear()

    # 开始搜索全部股票
    def search_all_stocks(self):
        stock_list = FileManager.read_stock_list_file()
        self.__searchResult = SearchResult()
        self.__searchResult.show()
        self.__progressBar = ProgressBar(stock_list.shape[0])
        self.__progressBar.show()
        self.__stockSearcher = StockSearcher(stock_list)
        self.__stockSearcher.progressBarCallback.connect(self.__progressBar.update_search_progress)
        self.__stockSearcher.addItemCallback.connect(self.__searchResult.add_stock_item)
        self.__stockSearcher.finishedCallback.connect(self.search_finished)
        self.__stockSearcher.start()

    # 搜索完毕回调
    def search_finished(self):
        self.__progressBar.close()
        self.__searchResult.update_found_stock_count()

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
        if self.cbxTotalAssets.isChecked():
            assets = row['totalAssets']
            if assets < self.spbTotalAssetsMin.value() or assets > self.spbTotalAssetsMax.value():
                return False

        # 检测股票毛利率是否达标
        if self.cbxGrossProfit.isChecked():
            gpr = row['gpr']
            if gpr < self.spbGrossProfit.value():
                return False

        # 检测股票净利率是否达标
        if self.cbxNetProfit.isChecked():
            npr = row['npr']
            if npr < self.spbNetProfit.value():
                return False

        # 检测股票收入增长是否达标
        if self.cbxIncomeIncrease.isChecked():
            revenue = row['rev']
            if revenue < self.spbIncomeIncrease.value():
                return False

        # 检测股票利润增长是否达标
        if self.cbxProfitIncrease.isChecked():
            profit = row['profit']
            if profit < self.spbProfitIncrease.value():
                return False

        # 检测股票净资产收益率是否达标
        if self.cbxNetAssetProfit.isChecked():
            profit = row['esp']
            asset = row['bvps']
            if profit / asset * 100 < self.spbNetAssetProfit.value():
                return False

        # 检测股票股东人数是否符合范围
        if self.cbxTotalHolders.isChecked():
            holders = row['holders'] / 10000
            if holders < self.spbTotalHoldersMin.value() or holders > self.spbTotalHoldersMax.value():
                return False

        # 所有指标全部达标
        return True

    # 技术面指标分析
    def technical_index_match_requirement(self, code: str):
        # 获得股票历史数据
        data = FileManager.read_stock_history_data(code)
        # 跳过还未上市新股
        if data.shape[0] == 0:
            return False
        # 跳过当日停牌股票
        if data.iloc[-1]['tradestatus'] == 0:
            return False

        # 逐条筛选自定义指标
        for item in self.__criteriaItems:
            if not SearchCriteria.match_criteria_item(data, item):
                return False
        return True

    # 检测股票是否在所选交易所中
    def code_in_search_range(self, code: int):
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
