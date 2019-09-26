from QtDesign.SearchCriteria_ui import Ui_SearchCriteria
from PyQt5.QtWidgets import QDialog
import StockFinder.StockFinder as StockFinder
import pandas


# 自定义技术指标内容
class CriteriaItem:
    queryLogic = "平均"
    operator = "大于"
    field = "股价"
    daysCountFirst = 1
    daysCountSecond = 5
    useAbsValue = False
    absoluteValue = 10
    comparedLogic = "平均"
    relativePercentage = 20


# 检测股票技术指标是否符合规定
def match_criteria_item(data: pandas.DataFrame, item: CriteriaItem):
    column_label = ""
    if item.field == "涨跌幅":
        column_label = "pctChg"
    elif item.field == "换手率":
        column_label = "turn"
    elif item.field == "股价":
        if item.queryLogic == "开盘":
            column_label = "open"
        elif item.queryLogic == "收盘":
            column_label = "close"
        elif item.queryLogic == "最高":
            column_label = "high"
        elif item.queryLogic == "最低":
            column_label = "low"

    # 获取初始值
    value_first = 0
    data_first = data[column_label].tail(item.daysCountFirst)
    if item.queryLogic == "平均":
        value_first = data_first.mean()
    elif item.queryLogic == "累计":
        value_first = data_first.sum()
    elif item.queryLogic == "最高":
        value_first = data_first.max()
    elif item.queryLogic == "最低":
        value_first = data_first.min()
    elif item.comparedLogic == "开盘":
        value_first = data_first.values[0]
    elif item.comparedLogic == "收盘":
        value_first = data_first.values[-1]

    # 获取参照物绝对值
    value_second = item.absoluteValue
    if not item.useAbsValue:
        # 相对值乘以系数
        ratio = item.relativePercentage / 100
        data_second = data[column_label].tail(item.daysCountSecond)
        raw_value_second = 0
        if item.comparedLogic == "平均":
            raw_value_second = data_second.mean()
        elif item.comparedLogic == "累计":
            raw_value_second = data_second.sum()
        elif item.comparedLogic == "最高":
            raw_value_second = data_second.max()
        elif item.comparedLogic == "最低":
            raw_value_second = data_second.min()
        elif item.comparedLogic == "开盘":
            raw_value_second = data_second.values[0]
        elif item.comparedLogic == "收盘":
            raw_value_second = data_second.values[-1]
        value_second = raw_value_second * ratio
    # 返回比较结果
    if item.operator == "大于":
        return value_first > value_second
    else:
        return value_first < value_second


# 通过json导入搜索条件
def import_criteria_item(json_data: dict):
    item = CriteriaItem()
    item.queryLogic = json_data['queryLogic']
    item.operator = json_data['operator']
    item.field = json_data['field']
    item.daysCountFirst = json_data['daysCountFirst']
    item.daysCountSecond = json_data['daysCountSecond']
    item.useAbsValue = json_data['useAbsValue']
    item.absoluteValue = json_data['absoluteValue']
    item.comparedLogic = json_data['comparedLogic']
    item.relativePercentage = json_data['relativePercentage']
    return item


class SearchCriteria(QDialog, Ui_SearchCriteria):

    def __init__(self, criteria_item: CriteriaItem):
        super().__init__()
        self.setupUi(self)
        # 初始化指标下拉列表内容
        self.cbbQueryLogic.addItems(['平均', '累计', '开盘', '收盘', '最高', '最低'])
        self.cbbComparedLogic.addItems(['平均', '累计', '开盘', '收盘', '最高', '最低'])
        self.cbbOperator.addItems(['大于', '小于'])
        self.cbbComparisonField.addItems(['股价', '涨跌幅', '换手率'])
        self.criteriaItem = criteria_item
        self.read_item_data()

    # 从指标中初始化界面数值显示
    def read_item_data(self):
        self.cbbQueryLogic.setCurrentText(self.criteriaItem.queryLogic)
        self.cbbOperator.setCurrentText(self.criteriaItem.operator)
        self.cbbComparisonField.setCurrentText(self.criteriaItem.field)
        self.spbFirstPeriod.setValue(self.criteriaItem.daysCountFirst)
        self.spbAveragePeriod.setValue(self.criteriaItem.daysCountSecond)
        self.rbnAbsValue.setChecked(self.criteriaItem.useAbsValue)
        self.cbbComparedLogic.setCurrentText(self.criteriaItem.comparedLogic)
        self.spbRelativePercentage.setValue(self.criteriaItem.relativePercentage)
        self.spbAbsValue.setValue(self.criteriaItem.absoluteValue)

    # 保存编辑后的指标
    def save_changes(self):
        self.criteriaItem.queryLogic = self.cbbQueryLogic.currentText()
        self.criteriaItem.operator = self.cbbOperator.currentText()
        self.criteriaItem.field = self.cbbComparisonField.currentText()
        self.criteriaItem.daysCountFirst = self.spbFirstPeriod.value()
        self.criteriaItem.daysCountSecond = self.spbAveragePeriod.value()
        self.criteriaItem.comparedLogic = self.cbbComparedLogic.currentText()
        self.criteriaItem.useAbsValue = self.rbnAbsValue.isChecked()
        self.criteriaItem.relativePercentage = self.spbRelativePercentage.value()
        self.criteriaItem.absoluteValue = self.spbAbsValue.value()
        StockFinder.stockFinderInstance.update_criteria_list(self.criteriaItem)
        self.close()

    # 放弃编辑离开
    def discard_changes(self):
        self.close()
