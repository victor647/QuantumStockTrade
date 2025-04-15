from QtDesign.FiveDaysFinder_ui import Ui_FiveDayShapeFinder
from PyQt6.QtWidgets import QDialog, QFileDialog
from Libraries import FileManager, Tools
from ShortTermTrading.FiveDayMatches import FiveDayMatches
import ShortTermTrading.StockFinder as StockFinder
import ShortTermTrading.SearchCriteria as SearchCriteria
import Data.TechnicalAnalysis as TA
import pandas


Instance = None


# 根据五日图形选股
class FiveDayFinder(QDialog, Ui_FiveDayShapeFinder):

    __currentEditingItem = None
    __matches = None

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.cbbOpenPosition.addItems(['低开', '高开', '平开'])
        self.cbbNeedleShape.addItems(['实体', '光头', '赤脚', '上影长', '下影长', '影等长'])
        self.cbbBodyHeight.addItems(['大', '中', '小', '十字'])
        self.cbbCandleColor.addItems(['阳线', '阴线', '白线'])
        # 初始化单例
        global Instance
        Instance = self
        self.criteriaItems = []

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
        self.cbbOpenPosition.setCurrentText(self.__currentEditingItem.openPosition)
        self.cbbNeedleShape.setCurrentText(self.__currentEditingItem.needleShape)
        self.cbbBodyHeight.setCurrentText(self.__currentEditingItem.bodyHeight)
        self.cbbCandleColor.setCurrentText(self.__currentEditingItem.candleColor)

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
        item.openPosition = self.cbbOpenPosition.currentText()
        item.needleShape = self.cbbNeedleShape.currentText()
        item.bodyHeight = self.cbbBodyHeight.currentText()
        item.candleColor = self.cbbCandleColor.currentText()

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
        if len(self.criteriaItems) == 0:
            Tools.show_error_dialog('选股条件为空！')
            return
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
            # 获取当日K线图形描述
            description = TA.candlestick_shape(day_data)
            if not criteria.match_criteria(description):
                return False
        return True

