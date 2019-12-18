from QtDesign.SearchCriteria_ui import Ui_SearchCriteria
from PyQt5.QtWidgets import QDialog
import StockFinder.StockFinder as StockFinder
import pandas


# 自定义技术指标内容
class CriteriaItem:
    queryLogic = "平均"
    operator = "大于"
    field = "股价"
    queryPeriodBegin = 3
    queryPeriodEnd = 1
    comparedPeriodBegin = 10
    comparedPeriodEnd = 1
    comparedObject = "比值"
    comparedLogic = "平均"
    value = 1


# 检测股票技术指标是否符合规定
def match_criteria_item(data: pandas.DataFrame, item: CriteriaItem):
    column_label = "close_pct"
    if item.field == "最高涨幅":
        column_label = "high_pct"
    elif item.field == "最低跌幅":
        column_label = "low_pct"
    elif item.field == "振幅":
        column_label = "amplitude"
    elif item.field == "换手率":
        column_label = "turn"
    elif item.field == "股价":
        if item.queryLogic == "开盘":
            column_label = "open"
        elif item.queryLogic == "最高":
            column_label = "high"
        elif item.queryLogic == "最低":
            column_label = "low"
        else:
            column_label = "close"

    # 获取初始值
    value_first = 0
    if item.queryPeriodEnd == 1:
        data_first = data[column_label].tail(item.queryPeriodBegin)
    else:
        data_first = data[column_label].iloc[-item.queryPeriodBegin:-(item.queryPeriodEnd - 1)]
    if item.queryLogic == "平均":
        value_first = data_first.mean()
    elif item.queryLogic == "累计":
        value_first = data_first.sum()
    elif item.queryLogic == "最高":
        value_first = data_first.max()
    elif item.queryLogic == "最低":
        value_first = data_first.min()
    elif item.queryLogic == "开盘":
        value_first = data_first.values[0]
    elif item.queryLogic == "收盘":
        value_first = data_first.values[-1]

    # 获取参照数据
    if item.comparedObject == "绝对值":
        value_second = item.value
    else:
        if item.comparedPeriodEnd == 1:
            data_second = data[column_label].tail(item.comparedPeriodBegin)
        else:
            data_second = data[column_label].iloc[-item.comparedPeriodBegin:-(item.comparedPeriodEnd - 1)]
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
        # 取差值或者比值
        if item.comparedObject == "差值":
            value_second = raw_value_second + item.value
        else:
            value_second = raw_value_second * item.value

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
    item.queryPeriodBegin = json_data['queryPeriodBegin']
    item.queryPeriodEnd = json_data['queryPeriodEnd']
    item.comparedPeriodBegin = json_data['comparedPeriodBegin']
    item.comparedPeriodEnd = json_data['comparedPeriodEnd']
    item.comparedLogic = json_data['comparedLogic']
    item.comparedObject = json_data['comparedObject']
    item.value = json_data['value']
    return item


class SearchCriteria(QDialog, Ui_SearchCriteria):

    def __init__(self, criteria_item: CriteriaItem):
        super().__init__()
        self.setupUi(self)
        # 初始化指标下拉列表内容
        self.cbbQueryLogic.addItems(['平均', '累计', '开盘', '收盘', '最高', '最低'])
        self.cbbComparedLogic.addItems(['平均', '累计', '开盘', '收盘', '最高', '最低'])
        self.cbbOperator.addItems(['大于', '小于'])
        self.cbbComparisonField.addItems(['股价', '收盘涨幅', '最高涨幅', '最低跌幅', '振幅', '换手率'])
        self.criteriaItem = criteria_item
        self.read_item_data()

    # 从指标中初始化界面数值显示
    def read_item_data(self):
        self.cbbQueryLogic.setCurrentText(self.criteriaItem.queryLogic)
        self.cbbOperator.setCurrentText(self.criteriaItem.operator)
        self.cbbComparisonField.setCurrentText(self.criteriaItem.field)
        self.spbQueryPeriodBegin.setValue(self.criteriaItem.queryPeriodBegin)
        self.spbQueryPeriodEnd.setValue(self.criteriaItem.queryPeriodEnd)
        self.spbComparedPeriodBegin.setValue(self.criteriaItem.comparedPeriodBegin)
        self.spbComparedPeriodEnd.setValue(self.criteriaItem.comparedPeriodEnd)
        self.cbbComparedLogic.setCurrentText(self.criteriaItem.comparedLogic)
        if self.criteriaItem.comparedObject == "绝对值":
            self.rbnAbsValue.setChecked(True)
        elif self.criteriaItem.comparedObject == "差值":
            self.rbnDifference.setChecked(True)
        else:
            self.rbnRatio.setChecked(True)
        self.spbValue.setValue(self.criteriaItem.value)

    # 保存编辑后的指标
    def save_changes(self):
        self.criteriaItem.queryLogic = self.cbbQueryLogic.currentText()
        self.criteriaItem.operator = self.cbbOperator.currentText()
        self.criteriaItem.field = self.cbbComparisonField.currentText()
        self.criteriaItem.queryPeriodBegin = self.spbQueryPeriodBegin.value()
        self.criteriaItem.queryPeriodEnd = self.spbQueryPeriodEnd.value()
        self.criteriaItem.comparedPeriodBegin = self.spbComparedPeriodBegin.value()
        self.criteriaItem.comparedPeriodEnd = self.spbComparedPeriodEnd.value()
        self.criteriaItem.comparedLogic = self.cbbComparedLogic.currentText()
        if self.rbnAbsValue.isChecked():
            self.criteriaItem.comparedObject = "绝对值"
        elif self.rbnDifference.isChecked():
            self.criteriaItem.comparedObject = "差值"
        else:
            self.criteriaItem.comparedObject = "比值"
        self.criteriaItem.value = self.spbValue.value()
        StockFinder.stockFinderInstance.update_criteria_list(self.criteriaItem)
        self.close()

    # 放弃编辑离开
    def discard_changes(self):
        self.close()

    # 根据所选的区间范围决定区间可选值
    def update_gui(self):
        self.spbQueryPeriodBegin.setEnabled(self.cbbQueryLogic.currentText() != "收盘")
        self.spbQueryPeriodEnd.setEnabled(self.cbbQueryLogic.currentText() != "开盘")
        self.spbComparedPeriodBegin.setEnabled(self.cbbComparedLogic.currentText() != "收盘")
        self.spbComparedPeriodEnd.setEnabled(self.cbbComparedLogic.currentText() != "开盘")
