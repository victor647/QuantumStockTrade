from QtDesign.FiveDaysFinder_ui import Ui_FiveDayShapeFinder
from PyQt5.QtWidgets import QDialog, QFileDialog
from Tools import FileManager, Tools
from ShortTermTrading.FiveDayMatches import FiveDayMatches
from ShortTermTrading.StockSearchThread import FiveDaySearcherSingle, FiveDaySearcherMultiple
import ShortTermTrading.StockFinder as StockFinder
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
        # 弹出匹配结果界面
        self.__matches = FiveDayMatches()
        self.__matches.show()
        if self.rbnSingleStock.isChecked():
            self.search_single_stock()
        else:
            self.search_all_stocks()

    # 在单只股票中寻找不同日期
    def search_single_stock(self):
        stock_code = Tools.get_stock_code(self.iptStockCode)
        search_process = FiveDaySearcherSingle(stock_code)
        search_process.addItemCallback.connect(self.__matches.add_match)
        search_process.start()

    # 在全部股票中寻找同一日期
    def search_all_stocks(self):
        # 确保选股日期不是周末
        search_date = Tools.get_nearest_trade_date(StockFinder.Instance.dteSearchDate.date()).toString('yyyy-MM-dd')
        search_process = FiveDaySearcherMultiple(search_date)
        search_process.addItemCallback.connect(self.__matches.add_match)
        search_process.start()

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

