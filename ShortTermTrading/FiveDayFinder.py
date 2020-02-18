from QtDesign.FiveDaysFinder_ui import Ui_FiveDayShapeFinder
from PyQt5.QtWidgets import QDialog, QFileDialog
from Tools import FileManager


# 五日指标内容
class FiveDayCriteriaItem:
    dayIndex = 1
    field = '收盘价'
    operator = '大于'
    value = -2

    # 转换为界面上显示的文字
    def to_display_text(self):
        return '第{}天{}{}{}%'.format(self.dayIndex, self.field, self.operator, self.value)

    # 通过json导入搜索条件
    @staticmethod
    def import_criteria_item(json_data: dict):
        item = FiveDayCriteriaItem()
        item.dayIndex = json_data['dayIndex']
        item.field = json_data['field']
        item.operator = json_data['operator']
        item.value = json_data['value']
        return item


# 根据五日图形选股
class FiveDayFinder(QDialog, Ui_FiveDayShapeFinder):

    __criteriaItems = []
    __currentEditingItem = None

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.cbbQueryField.addItems(['开盘涨跌幅', '收盘涨跌幅', '日内涨跌幅', '最高涨幅', '最低跌幅', '振幅', '换手率'])

    # 删除一个条件
    def remove_criteria(self):
        selection = self.lstCriteriaItems.selectedIndexes()
        if len(selection) == 0:
            return
        index = selection[0].row()
        self.__criteriaItems.pop(index)
        self.lstCriteriaItems.takeItem(index)

    # 清除所有条件
    def clear_criterias(self):
        self.__criteriaItems = []
        self.lstCriteriaItems.clear()

    # 选取条件
    def select_criteria(self):
        selection = self.lstCriteriaItems.selectedIndexes()
        if len(selection) == 0:
            return
        index = selection[0].row()
        self.__currentEditingItem = self.__criteriaItems[index]

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
            item = FiveDayCriteriaItem()
            self.update_criteria_item(item)
            self.__criteriaItems.append(item)
            self.lstCriteriaItems.addItem(item.to_display_text())
        # 编辑所选的已有条件
        else:
            self.update_criteria_item(self.__currentEditingItem)
            self.lstCriteriaItems.clear()
            for item in self.__criteriaItems:
                self.lstCriteriaItems.addItem(item.to_display_text())

    # 更新所选条件内容
    def update_criteria_item(self, item: FiveDayCriteriaItem):
        item.dayIndex = self.spbDayIndex.value()
        item.field = self.cbbQueryField.currentText()
        item.operator = '大于' if self.rbnGreaterThan.isChecked() else '小于'
        item.value = self.spbCriteriaValue.value()

    # 导出条件组
    def export_config(self):
        file_path = QFileDialog.getSaveFileName(directory=FileManager.search_config_path(), filter='JSON(*.json)')
        if file_path[0] != '':
            FileManager.export_config_as_json(self.__criteriaItems, file_path[0])

    # 导入条件组
    def import_config(self):
        file_path = QFileDialog.getOpenFileName(directory=FileManager.search_config_path(), filter='JSON(*.json)')
        if file_path[0] != '':
            self.__criteriaItems = FileManager.import_json_config(file_path[0], FiveDayCriteriaItem.import_criteria_item)
            for item in self.__criteriaItems:
                self.lstCriteriaItems.addItem(item.to_display_text())

    # 开始寻找图形
    def start_searching(self):
        if self.rbnSingleStock.isChecked():
            self.search_single_stock()
        if self.rbnAllStocks.isChecked():
            self.search_all_stocks()

    # 在单只股票中寻找不同日期
    def search_single_stock(self):
        pass

    # 在全部股票中寻找同一日期
    def search_all_stocks(self):
        pass
