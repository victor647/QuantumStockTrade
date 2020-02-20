from QtDesign.FiveDaysFinder_ui import Ui_FiveDayShapeFinder
from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal
from Tools import FileManager, Tools
from Tools.ProgressBar import ProgressBar
from ShortTermTrading.FiveDayMatches import FiveDayMatches
import Data.TechnicalAnalysis as TechnicalAnalysis
import ShortTermTrading.SearchCriteria as SearchCriteria
import pandas


Instance = None


# 根据五日图形选股
class FiveDayFinder(QDialog, Ui_FiveDayShapeFinder):

    criteriaItems = []
    __currentEditingItem = None
    __matches = None

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.cbbQueryField.addItems(['开盘涨跌幅', '收盘涨跌幅', '日内涨跌幅', '最高涨幅', '最低跌幅', '振幅', '换手率'])
        # 初始化单例
        global Instance
        Instance = self

    # 删除一个条件
    def remove_criteria(self):
        selection = self.lstCriteriaItems.selectedIndexes()
        if len(selection) == 0:
            return
        index = selection[0].row()
        self.criteriaItems.pop(index)
        self.lstCriteriaItems.takeItem(index)

    # 清除所有条件
    def clear_criterias(self):
        self.criteriaItems = []
        self.lstCriteriaItems.clear()

    # 选取条件
    def select_criteria(self):
        selection = self.lstCriteriaItems.selectedIndexes()
        if len(selection) == 0:
            self.__currentEditingItem = None
            return
        index = selection[0].row()
        self.__currentEditingItem = self.criteriaItems[index]

    # 编辑条件
    def edit_criteria(self):
        self.select_criteria()
        self.spbDayIndex.setValue(self.__currentEditingItem.dayIndex)
        self.cbbQueryField.setCurrentText(self.__currentEditingItem.field)
        if self.__currentEditingItem.operator == '大于':
            self.rbnGreaterThan.setChecked(True)
        else:
            self.rbnLessThan.setChecked(True)
        self.spbCriteriaValue.setValue(self.__currentEditingItem.value)

    # 保存编辑好的条件
    def save_criteria(self):
        # 创建新的条件
        if self.__currentEditingItem is None:
            item = SearchCriteria.FiveDayCriteriaItem()
            self.update_criteria_item(item)
            self.criteriaItems.append(item)
            self.refresh_items_display()
        # 编辑所选的已有条件
        else:
            self.update_criteria_item(self.__currentEditingItem)
            self.refresh_items_display()
        # 取消条件列表中的选定
        self.lstCriteriaItems.clearSelection()

    # 更新所选条件内容
    def update_criteria_item(self, item: SearchCriteria.FiveDayCriteriaItem):
        item.dayIndex = self.spbDayIndex.value()
        item.field = self.cbbQueryField.currentText()
        item.operator = '大于' if self.rbnGreaterThan.isChecked() else '小于'
        item.value = self.spbCriteriaValue.value()

    # 导出条件组
    def export_config(self):
        file_path = QFileDialog.getSaveFileName(directory=FileManager.search_config_path(), filter='JSON(*.json)')
        if file_path[0] != '':
            FileManager.export_config_as_json(self.criteriaItems, file_path[0])

    # 导入条件组
    def import_config(self):
        file_path = QFileDialog.getOpenFileName(directory=FileManager.search_config_path(), filter='JSON(*.json)')
        if file_path[0] != '':
            self.criteriaItems = FileManager.import_json_config(file_path[0], SearchCriteria.FiveDayCriteriaItem.import_criteria_item)
            self.refresh_items_display()

    # 排序更新列表显示
    def refresh_items_display(self):
        self.criteriaItems.sort()
        self.lstCriteriaItems.clear()
        for item in self.criteriaItems:
            self.lstCriteriaItems.addItem(item.to_display_text())

    # 开始寻找图形
    def start_searching(self):
        if self.rbnSingleStock.isChecked():
            code = Tools.get_stock_code(self.iptStockCode)
            self.search_single_stock(code)
        if self.rbnAllStocks.isChecked():
            self.search_all_stocks()

    # 在单只股票中寻找不同日期
    def search_single_stock(self, stock_code: str):
        # 弹出匹配结果界面
        self.__matches = FiveDayMatches()
        self.__matches.show()
        # 开始匹配线程
        search_process = FiveDaySingleStockSearcher(stock_code)
        search_process.addItemCallback.connect(self.__matches.add_match)
        search_process.start()

    # 在全部股票中寻找同一日期
    def search_all_stocks(self):
        pass

    # 是否符合条件组
    def match_criteria(self, day_index: int, stock_data: pandas.DataFrame):
        for criteria in self.criteriaItems:
            day_data = stock_data.iloc[day_index + criteria.dayIndex - 1]
            label = SearchCriteria.get_column_label(criteria.field)
            if criteria.operator == '大于' and day_data[label] < criteria.value:
                return False
            if criteria.operator == '小于' and day_data[label] > criteria.value:
                return False
        return True


# 多线程股票搜索算法
class FiveDaySingleStockSearcher(QThread):
    addItemCallback = pyqtSignal(list)
    progressBarCallback = pyqtSignal(int, str, str)
    finishedCallback = pyqtSignal()

    def __init__(self, stock_code: str):
        super().__init__()
        self.stockCode = stock_code
        self.stockData = FileManager.read_stock_history_data(self.stockCode, True)
        # 获取条件组中用到的最长日数
        self.maxDaysUsed = Instance.criteriaItems[-1].dayIndex - 1
        # 弹出选股进度条
        progress_bar = ProgressBar(self.stockData.shape[0], self.stockCode + '图形寻找', self)
        progress_bar.show()
        self.progressBarCallback.connect(progress_bar.update_search_progress)
        self.finishedCallback.connect(progress_bar.destroy)

    def __del__(self):
        self.work = False
        self.terminate()

    def run(self):
        # 获取股票名称
        stock_name = Tools.get_stock_name_from_code(self.stockCode)
        for day_index in range(self.stockData.shape[0] - self.maxDaysUsed):
            date = self.stockData.index[day_index]
            self.progressBarCallback.emit(day_index, stock_name, date)
            if Instance.match_criteria(day_index, self.stockData):
                next_day_performance = self.get_day_performance(day_index, 1)
                three_day_performance = self.get_day_performance(day_index, 3)
                five_day_performance = self.get_day_performance(day_index, 5)
                ten_day_performance = self.get_day_performance(day_index, 10)
                # 打包数据列表
                items = [self.stockCode, stock_name, date, next_day_performance, three_day_performance, five_day_performance, ten_day_performance]
                self.addItemCallback.emit(items)
        # 搜索结束回调
        self.finishedCallback.emit()

    # 计算图形出现后x日的股价表现
    def get_day_performance(self, shape_start_date: int, days: int):
        shape_end_day_index = shape_start_date + self.maxDaysUsed
        period_end_day_index = shape_end_day_index + days
        # 若距今日期不够，则按照最后一日价格计算
        if period_end_day_index >= self.stockData.shape[0]:
            period_end_day_index = -1
        # 获得图形出现时价格和x日后价格
        shape_end_price = self.stockData.iloc[shape_end_day_index]['close']
        period_end_price = self.stockData.iloc[period_end_day_index]['close']
        return TechnicalAnalysis.get_percentage_from_price(period_end_price, shape_end_price)

