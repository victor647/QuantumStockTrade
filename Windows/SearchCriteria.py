from QtDesign.SearchCriteria_ui import Ui_SearchCriteria
from PyQt5.QtWidgets import QDialog
import Windows.StockFinder as StockFinder
import pandas


# 自定义技术指标内容
class CriteriaItem:
    logic = "平均"
    operator = "大于"
    field = "股价"
    daysCountFirst = 1
    daysCountSecond = 5
    useAbsValue = False
    relativePercentage = 20
    absoluteValue = 10


# 检测股票技术指标是否符合规定
def match_criteria_item(data: pandas.DataFrame, item: CriteriaItem):
    # 获取比较对象
    column_label = "close"
    if item.field == "涨跌幅":
        column_label = "pctChg"
    elif item.field == "换手率":
        column_label = "turn"
    elif item.field == "股价":
        if item.logic == "最高":
            column_label = "high"
        elif item.logic == "最低":
            column_label = "low"

    # 获取初始值
    value_first = 0
    if item.logic == "平均":
        value_first = data[column_label].tail(item.daysCountFirst).mean()
    elif item.logic == "累计":
        value_first = data[column_label].tail(item.daysCountFirst).sum()
    elif item.logic == "最高":
        value_first = data[column_label].tail(item.daysCountFirst).max()
    elif item.logic == "最低":
        value_first = data[column_label].tail(item.daysCountFirst).min()

    # 获取参照物绝对值
    value_second = item.absoluteValue
    if not item.useAbsValue:
        # 相对值乘以系数
        ratio = item.relativePercentage / 100 + 1
        raw_value_second = data[column_label].tail(item.daysCountSecond).mean()
        value_second = raw_value_second * ratio
    # 返回比较结果
    if item.operator == "大于":
        return value_first > value_second
    else:
        return value_first < value_second


# 通过json导入搜索条件
def import_criteria_item(dct):
    item = CriteriaItem()
    item.logic = dct['logic']
    item.operator = dct['operator']
    item.field = dct['field']
    item.daysCountFirst = dct['daysCountFirst']
    item.daysCountSecond = dct['daysCountSecond']
    item.useAbsValue = dct['useAbsValue']
    item.relativePercentage = dct['relativePercentage']
    item.absoluteValue = dct['absoluteValue']
    return item


class SearchCriteria(QDialog, Ui_SearchCriteria):

    def __init__(self, criteria_item: CriteriaItem):
        super().__init__()
        self.setupUi(self)
        # 初始化指标下拉列表内容
        self.cbbQueryLogic.addItems(['平均', '累计', '最高', '最低'])
        self.cbbOperator.addItems(['大于', '小于'])
        self.cbbComparisonField.addItems(['收盘价', '股价', '涨跌幅', '换手率'])
        self.criteriaItem = criteria_item
        self.read_item_data()

    # 从指标中初始化界面数值显示
    def read_item_data(self):
        self.cbbQueryLogic.setCurrentText(self.criteriaItem.logic)
        self.cbbOperator.setCurrentText(self.criteriaItem.operator)
        self.cbbComparisonField.setCurrentText(self.criteriaItem.field)
        self.spbFirstPeriod.setValue(self.criteriaItem.daysCountFirst)
        self.spbAveragePeriod.setValue(self.criteriaItem.daysCountSecond)
        self.rbnAbsValue.setChecked(self.criteriaItem.useAbsValue)
        self.spbRelativePercentage.setValue(self.criteriaItem.relativePercentage)
        self.spbAbsValue.setValue(self.criteriaItem.absoluteValue)

    # 保存编辑后的指标
    def save_changes(self):
        self.criteriaItem.logic = self.cbbQueryLogic.currentText()
        self.criteriaItem.operator = self.cbbOperator.currentText()
        self.criteriaItem.field = self.cbbComparisonField.currentText()
        self.criteriaItem.daysCountFirst = self.spbFirstPeriod.value()
        self.criteriaItem.daysCountSecond = self.spbAveragePeriod.value()
        self.criteriaItem.useAbsValue = self.rbnAbsValue.isChecked()
        self.criteriaItem.relativePercentage = self.spbRelativePercentage.value()
        self.criteriaItem.absoluteValue = self.spbAbsValue.value()
        StockFinder.stockFinderInstance.update_criteria_list()
        self.close()

    # 放弃编辑离开
    def discard_changes(self):
        self.close()
