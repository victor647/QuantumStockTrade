from PyQt5.QtCore import pyqtSignal, Qt, QDate, QThread
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QListWidgetItem, QMessageBox
from PyQt5.QtGui import QKeyEvent
from QtDesign.StockFinder_ui import Ui_StockFinder
from ShortTermTrading.SearchResult import SearchResult
from ShortTermTrading.BatchSearcher import BatchSearcher
from ShortTermTrading.FiveDayFinder import FiveDayFinder
from Tools.ProgressBar import ProgressBar
from datetime import datetime
import ShortTermTrading.SearchCriteria as SearchCriteria
import tushare, pandas
from Tools import Tools, FileManager
import Data.TechnicalAnalysis as DataAnalyzer


Instance = None


class StockFinder(QMainWindow, Ui_StockFinder):
    __searchResult = None
    __criteriaItems = []

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 初始化单例
        global Instance
        Instance = self
        # 初始化选股日期
        self.dteSearchDate.setDate(QDate.currentDate())
        # 初始化技术面指标下拉菜单
        self.cbbMacdBehaviour.addItems(['金叉', '死叉', '翻红', '翻绿', '红柱缩短', '绿柱缩短'])
        self.cbbBollBehaviour.addItems(['上穿', '下穿'])
        self.cbbBollTrack.addItems(['上轨', '中轨', '下轨'])
        self.cbbExpmaBehaviour.addItems(['多头下穿白线', '多头下穿黄线', '空头上穿白线', '空头上穿黄线', '金叉转为多头', '死叉转为空头'])
        self.cbbMaBehaviour.addItems(['金叉', '死叉'])
        self.cbbTrixBehaviour.addItems(['金叉', '死叉'])

    # 快捷键设置
    def keyPressEvent(self, key: QKeyEvent):
        # Esc键清除选择
        if key.key() == Qt.Key_Escape:
            self.lstCriteriaItems.clearSelection()
        # 按删除键删除股票或指标组
        elif key.key() == Qt.Key_Delete or key.key() == Qt.Key_Backspace:
            self.remove_criteria_item()

    # 打开批量自动选股器
    @staticmethod
    def run_batch_searcher():
        batch_searcher = BatchSearcher()
        batch_searcher.show()
        batch_searcher.exec_()

    # 五日图形选股
    @staticmethod
    def five_day_search():
        finder = FiveDayFinder()
        finder.show()
        finder.exec_()

    # 根据十大流通股东结构选股
    @staticmethod
    def search_by_holders_structure():
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
                if '有限公司' in row_holder['name'] or row_holder['sharetype'] == '限售流通股':
                    continue
                count += 1
                # 股权结构优秀，加入选中列表
                if count >= 5:
                    search_result.append(code)
                    break
            if index > 100:
                break

        file_path = QFileDialog.getSaveFileName(directory=FileManager.selected_stock_list_path(), filter='TXT(*.txt)')
        if file_path[0] != '':
            file = open(file_path[0], 'w')
            for code in search_result:
                file.write(code + '\n')
            file.close()

    # 获取并导出全部股票K线
    @staticmethod
    def export_all_stock_data():
        FileManager.export_all_stock_data()

    # 获取两市全部股票列表
    def export_all_stock_list(self):
        FileManager.save_stock_list_file()
        QMessageBox.information(self, '成功', '导出全部股票列表成功！')

    # 保存基本面指标搜索条件
    def export_basic_config(self):
        file_path = QFileDialog.getSaveFileName(directory=FileManager.search_config_path(), filter='JSON(*.json)')
        data = {
            'peOn': self.cbxPriceEarning.isChecked(),
            'peMin': self.spbPriceEarningMin.value(),
            'peMax': self.spbPriceEarningMax.value(),
            'pbOn': self.cbxPriceBook.isChecked(),
            'pbMin': self.spbPriceBookMin.value(),
            'pbMax': self.spbPriceBookMax.value(),
            'totalShareOn': self.cbxTotalShare.isChecked(),
            'totalShareMin': self.spbTotalShareMin.value(),
            'totalShareMax': self.spbTotalShareMax.value(),
            'totalAssetsOn': self.cbxTotalAssets.isChecked(),
            'totalAssetsMin': self.spbTotalAssetsMin.value(),
            'totalAssetsMax': self.spbTotalAssetsMax.value(),
            'grossProfitOn': self.cbxGrossProfit.isChecked(),
            'grossProfit': self.spbGrossProfit.value(),
            'netProfitOn': self.cbxNetProfit.isChecked(),
            'netProfit': self.spbNetProfit.value(),
            'incomeIncreaseOn': self.cbxIncomeIncrease.isChecked(),
            'incomeIncrease': self.spbIncomeIncrease.value(),
            'profitIncreaseOn': self.cbxProfitIncrease.isChecked(),
            'profitIncrease': self.spbProfitIncrease.value(),
            'netAssetProfitOn': self.cbxNetAssetProfit.isChecked(),
            'netAssetProfit': self.spbNetAssetProfit.value(),
            'totalHoldersOn': self.cbxTotalHolders.isChecked(),
            'totalHoldersMin': self.spbTotalHoldersMin.value(),
            'totalHoldersMax': self.spbTotalHoldersMax.value(),
            'includeSt': self.cbxIncludeStStock.isChecked(),
            'timeToMarketOn': self.cbxTimeToMarket.isChecked(),
            'timeToMarketMin': self.spbTimeToMarketMin.value(),
            'timeToMarketMax': self.spbTimeToMarketMax.value(),
        }
        if file_path[0] != '':
            FileManager.export_config_as_json(data, file_path[0])

    # 载入基本面指标搜索条件
    def import_basic_config(self):
        file_path = QFileDialog.getOpenFileName(directory=FileManager.search_config_path(), filter='JSON(*.json)')
        if file_path[0] != '':
            data = FileManager.import_json_config(file_path[0])
            if 'peOn' not in data:
                Tools.show_error_dialog('选取的配置文件格式不对！')
                return
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
            self.cbxTimeToMarket.setChecked(data['timeToMarketOn'])
            self.spbTimeToMarketMin.setValue(data['timeToMarketMin'])
            self.spbTimeToMarketMax.setValue(data['timeToMarketMax'])

    # 保存技术面指标搜索条件
    def export_technical_config(self):
        file_path = QFileDialog.getSaveFileName(directory=FileManager.search_config_path(), filter='JSON(*.json)')
        data = {
            'timePeriod': self.spbTechnicalTimePeriod.value(),
            'macdOn': self.cbxMacdEnabled.isChecked(),
            'macdBehaviour': self.cbbMacdBehaviour.currentText(),
            'bollOn': self.cbxBollEnabled.isChecked(),
            'bollBehaviour': self.cbbBollBehaviour.currentText(),
            'bollTrack': self.cbbBollTrack.currentText(),
            'expmaOn': self.cbxExpmaEnabled.isChecked(),
            'expmaBehaviour': self.cbbExpmaBehaviour.currentText(),
            'maOn': self.cbxMaEnabled.isChecked(),
            'maShort': self.spbMaShort.value(),
            'maBehaviour': self.cbbMaBehaviour.currentText(),
            'maLong': self.spbMaLong.value(),
            'trixOn': self.cbxTrixEnabled.isChecked(),
            'trixBehaviour': self.cbbTrixBehaviour.currentText()
        }
        if file_path[0] != '':
            FileManager.export_config_as_json(data, file_path[0])

    # 载入技术面指标搜索条件
    def import_technical_config(self):
        file_path = QFileDialog.getOpenFileName(directory=FileManager.search_config_path(), filter='JSON(*.json)')
        if file_path[0] != '':
            data = FileManager.import_json_config(file_path[0])
            if 'timePeriod' not in data:
                Tools.show_error_dialog('选取的配置文件格式不对！')
                return
            self.spbTechnicalTimePeriod.setValue(data['timePeriod'])
            self.cbxMacdEnabled.setChecked(data['macdOn'])
            self.cbbMacdBehaviour.setCurrentText(data['macdBehaviour'])
            self.cbxBollEnabled.setChecked(data['bollOn'])
            self.cbbBollBehaviour.setCurrentText(data['bollBehaviour'])
            self.cbbBollTrack.setCurrentText(data['bollTrack'])
            self.cbxExpmaEnabled.setChecked(data['expmaOn'])
            self.cbbExpmaBehaviour.setCurrentText(data['expmaBehaviour'])
            self.cbxMaEnabled.setChecked(data['maOn'])
            self.spbMaShort.setValue(data['maShort'])
            self.cbbMaBehaviour.setCurrentText(data['maBehaviour'])
            self.spbMaLong.setValue(data['maLong'])
            self.cbxTrixEnabled.setChecked(data['trixOn'])
            self.cbbTrixBehaviour.setCurrentText(data['trixBehaviour'])

    # 保存自定义指标搜索条件
    def export_custom_config(self):
        file_path = QFileDialog.getSaveFileName(directory=FileManager.search_config_path(), filter='JSON(*.json)')
        if file_path[0] != '':
            FileManager.export_config_as_json(self.__criteriaItems, file_path[0])

    # 载入自定义指标搜索条件
    def import_custom_config(self):
        file_path = QFileDialog.getOpenFileName(directory=FileManager.search_config_path(), filter='JSON(*.json)')
        if file_path[0] != '':
            self.__criteriaItems = FileManager.import_json_config(file_path[0], SearchCriteria.import_criteria_item)
            self.update_criteria_list()

    # 更新自定义搜索条件列表显示
    def update_criteria_list(self, edited_item=None):
        # 添加条件时
        if edited_item is not None and edited_item not in self.__criteriaItems:
            self.__criteriaItems.append(edited_item)
        # 重新生成图表
        self.lstCriteriaItems.clear()
        for item in self.__criteriaItems:
            self.lstCriteriaItems.addItem(item.to_display_text())

    # 新增自定义搜索条件
    @staticmethod
    def add_criteria_item():
        item = SearchCriteria.CriteriaItem()
        window = SearchCriteria.SearchCriteria(item)
        window.show()
        window.exec()

    # 双击编辑所选自定义搜索条件
    def edit_selected_item(self, item: QListWidgetItem):
        index = self.lstCriteriaItems.indexFromItem(item)
        window = SearchCriteria.SearchCriteria(self.__criteriaItems[index.row()])
        window.show()
        window.exec()

    # 点击编辑按钮编辑所选自定义搜索条件
    def modify_criteria_item(self):
        selection = self.lstCriteriaItems.selectedIndexes()
        if len(selection) == 0:
            return
        index = selection[0].row()
        item = self.__criteriaItems[index]
        window = SearchCriteria.SearchCriteria(item)
        window.show()
        window.exec()

    # 删除所选自定义搜索条件
    def remove_criteria_item(self):
        selection = self.lstCriteriaItems.selectedIndexes()
        if len(selection) == 0:
            return
        index = selection[0].row()
        self.__criteriaItems.pop(index)
        self.lstCriteriaItems.takeItem(index)

    # 清空自定义搜索条件
    def reset_criteria_items(self):
        self.__criteriaItems = []
        self.lstCriteriaItems.clear()

    # 开始搜索全部股票
    def search_all_stocks(self):
        stock_list = FileManager.read_stock_list_file()
        # 确保选股日期不是周末
        search_date = Tools.get_nearest_trade_date(self.dteSearchDate.date()).toString('yyyy-MM-dd')
        # 弹出搜索结果界面
        self.__searchResult = SearchResult(search_date)
        self.__searchResult.show()
        # 开始选股进程
        search_process = StockSearcher(stock_list, search_date, False)
        search_process.addItemCallback.connect(self.__searchResult.add_stock_item)
        search_process.start()

    # 批量选股器自动选股接口
    @staticmethod
    def auto_search(searcher: BatchSearcher, start_date: QDate, end_date: QDate):
        stock_list = FileManager.read_stock_list_file()
        current_searching_date = start_date
        # 初始化选股结果列表
        while current_searching_date < end_date:
            # 确保选股日期不是周末
            current_searching_date = Tools.get_nearest_trade_date(current_searching_date)
            date_string = current_searching_date.toString('yyyy-MM-dd')
            # 开始选股进程
            search_process = StockSearcher(stock_list, date_string, True, searcher.iptCriteriaName.text())
            search_process.start()
            current_searching_date = searcher.move_to_next_date(current_searching_date)

    # 基本面指标分析
    def match_basic_criterias(self, row: pandas.DataFrame, search_date: str):
        # 检测股票是否是ST股
        if not self.cbxIncludeStStock.isChecked():
            name = row['name']
            if 'ST' in name:
                return False

        # 检测股票上市时间是否符合范围
        if self.cbxTimeToMarket.isChecked():
            date = row['timeToMarket']
            # 去除还未上市的股票
            if date == 0:
                return False
            # 获取上市和搜索日期
            date_to_market = datetime.strptime(str(date), '%Y%m%d')
            date_at_search = datetime.strptime(search_date, '%Y-%m-%d')
            # 获取上市月数
            months_to_market = (date_at_search - date_to_market).days / 30.45
            if months_to_market < self.spbTimeToMarketMin.value() or months_to_market > self.spbTimeToMarketMax.value():
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

    # 自定义指标分析
    def match_custom_criterias(self, data: pandas.DataFrame):
        # 若没有自定义指标则跳过
        if len(self.__criteriaItems) == 0:
            return True
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

    # 技术指标分析
    def match_technical_criterias(self, data: pandas.DataFrame):
        # 跳过上市一个月内的新股
        if data.shape[0] < 20:
            return False
        period = self.spbTechnicalTimePeriod.value() + 1
        # 检测MACD图形
        if self.cbxMacdEnabled.isChecked() and not DataAnalyzer.match_macd(data, period, self.cbbMacdBehaviour.currentText()):
            return False
        # 检测BOLL区间
        if self.cbxBollEnabled.isChecked() and not DataAnalyzer.match_boll(data, period, self.cbbBollTrack.currentText(), self.cbbBollBehaviour.currentText()):
            return False
        # 检测EXPMA图形
        if self.cbxExpmaEnabled.isChecked() and not DataAnalyzer.match_expma(data, period, self.cbbExpmaBehaviour.currentText()):
            return False
        # 检测均线交叉
        if self.cbxMaEnabled.isChecked() and not DataAnalyzer.match_ma(data, period, self.spbMaShort.value(), self.spbMaLong.value(), self.cbbMaBehaviour.currentText()):
            return False
        # 检测TRIX图形
        if self.cbxTrixEnabled.isChecked() and not DataAnalyzer.match_trix(data, period, self.cbbTrixBehaviour.currentText()):
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

    def __init__(self, stock_list, search_date: str, export_to_file: bool, folder_name=''):
        super().__init__()
        self.stockList = stock_list
        self.selectedStocks = []
        self.searchDate = search_date
        # 弹出选股进度条
        progress_bar = ProgressBar(stock_list.shape[0], search_date + '选股', self)
        progress_bar.show()
        self.progressBarCallback.connect(progress_bar.update_search_progress)
        self.finishedCallback.connect(progress_bar.destroy)
        if export_to_file:
            self.finishedCallback.connect(lambda: FileManager.export_auto_search_stock_list(self.selectedStocks, folder_name, self.searchDate))

    def __del__(self):
        self.work = False
        self.terminate()

    def run(self):
        for index, row in self.stockList.iterrows():
            code_num = row['code']
            # 将股票代码固定为6位数
            code = str(code_num).zfill(6)
            # 获得股票中文名称
            name = row['name']
            # 更新窗口进度条
            self.progressBarCallback.emit(index, code, name)
            # 判断股票是否在选中的交易所中
            if not Instance.code_in_search_range(code_num):
                continue
            # 基本面指标考察
            if Instance.cbxBasicCriteriasEnabled.isChecked() and not Instance.match_basic_criterias(row, self.searchDate):
                continue

            # 获得股票历史数据
            data = FileManager.read_stock_history_data(code, True)
            # 剪去选股日期之后的数据
            data = data.loc[:self.searchDate]
            # 技术面指标考察
            if Instance.cbxTechnicalCriteriasEnabled.isChecked() and not Instance.match_technical_criterias(data):
                continue
            # 自定义指标考察
            if not Instance.match_custom_criterias(data):
                continue
            # 获得股票行业信息
            industry = row['industry']
            # 获得股票上市地区
            area = row['area']
            # 获得股票市盈率
            pe = row['pe']
            # 获得股票市净率
            pb = row['pb']
            # 获得股票总市值
            assets = row['totalAssets']
            # 净资产收益率
            roe = str(round(row['esp'] / row['bvps'] * 100, 2)) + '%'
            # 将符合要求的股票信息打包
            items = [code, name, industry, area, pe, pb, assets, roe]
            # 添加股票信息至列表
            self.addItemCallback.emit(items)
            self.selectedStocks.append(code)
        # 搜索结束回调
        self.finishedCallback.emit()
