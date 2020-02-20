from QtDesign.SearchCriteria_ui import Ui_SearchCriteria
from PyQt5.QtWidgets import QDialog
import ShortTermTrading.StockFinder as StockFinder
import pandas


# 五日选股指标内容
class FiveDayCriteriaItem:
    dayIndex = 1
    field = '收盘价'
    operator = '大于'
    value = -2

    # 自定义排序算法
    def __lt__(self, other):
        return self.dayIndex < other.dayIndex

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


# 自定义技术指标内容
class CriteriaItem:
    queryLogic = '平均'
    comparedLogic = '平均'
    queryField = '收盘价'
    comparedField = '收盘价'
    queryPeriodBegin = 3
    queryPeriodEnd = 1
    comparedPeriodBegin = 10
    comparedPeriodEnd = 1
    comparedObject = '比值'
    operator = '大于'
    value = 1

    # 转换为界面上显示的文字
    def to_display_text(self):
        if self.operator == '小于':
            operator = '<'
        elif self.operator == '大于':
            operator = '>'
        else:
            operator = '='
        if self.comparedObject != '差值':
            connector = operator
        else:
            connector = '-'
        # 获取时间段数据
        if self.queryPeriodBegin == self.queryPeriodEnd:
            if self.queryPeriodBegin == 1:
                text = '最新'
            else:
                text = str(self.queryPeriodBegin) + '日前'
        elif self.queryPeriodEnd == 1:
            text = '最近' + str(self.queryPeriodBegin) + '日内' + self.queryLogic
        else:
            text = '最近' + str(self.queryPeriodBegin) + '日到' + str(self.queryPeriodEnd) + '日之间' + self.queryLogic
        text += self.queryField + connector
    
        if self.comparedObject == '绝对值':
            text += str(self.value) + ('元' if '价' in self.queryField else '%')
        else:
            if self.comparedPeriodBegin == self.comparedPeriodEnd:
                if self.comparedPeriodBegin == 1:
                    text += '最新'
                else:
                    text += str(self.comparedPeriodBegin) + '日前'
            elif self.comparedPeriodEnd == 1:
                text += '最近' + str(self.comparedPeriodBegin) + '日内' + self.comparedLogic
            else:
                text += '最近' + str(self.comparedPeriodBegin) + '日到' + str(self.comparedPeriodEnd) + '日之间' + self.comparedLogic
            text += self.comparedField
    
            if self.comparedObject == '比值' and self.value != 1:
                text += '×' + str(self.value)
            if self.comparedObject == '差值':
                text += operator + str(self.value)
                if '价' in self.queryField and '价' in self.comparedField:
                    text += '元'
                if '价' not in self.queryField and '价' not in self.comparedField:
                    text += '%'
        return text

    # 通过json导入搜索条件
    @staticmethod
    def import_criteria_item(json_data: dict):
        item = CriteriaItem()
        item.queryLogic = json_data['queryLogic']
        item.comparedLogic = json_data['comparedLogic']
        item.queryField = json_data['queryField']
        item.comparedField = json_data['comparedField']
        item.queryPeriodBegin = json_data['queryPeriodBegin']
        item.queryPeriodEnd = json_data['queryPeriodEnd']
        item.comparedPeriodBegin = json_data['comparedPeriodBegin']
        item.comparedPeriodEnd = json_data['comparedPeriodEnd']
        item.comparedObject = json_data['comparedObject']
        item.operator = json_data['operator']
        item.value = json_data['value']
        return item


# 获取数据库对应列表
def get_column_label(field: str):
    if field == '开盘价':
        return 'open'
    elif field == '收盘价':
        return 'close'
    elif field == '最高价':
        return 'high'
    elif field == '最低价':
        return 'low'
    elif field == '开盘涨跌幅':
        return 'open_pct'
    elif field == '收盘涨跌幅':
        return 'close_pct'
    elif field == '日内涨跌幅':
        return 'daily_pct'
    elif field == '最高涨幅':
        return 'high_pct'
    elif field == '最低跌幅':
        return 'low_pct'
    elif field == '振幅':
        return 'amplitude'
    else:
        return 'turn'


# 根据逻辑获取数据值
def get_data_value(logic: str, data: pandas.DataFrame):
    if logic == '平均':
        return data.mean()
    elif logic == '累计':
        return data.sum()
    elif logic == '最高':
        return data.max()
    else:
        return data.min()


# 检测股票技术指标是否符合规定
def match_criteria_item(data: pandas.DataFrame, item: CriteriaItem):
    # 上市天数少于指标范围则跳过
    if data.shape[0] < item.queryPeriodBegin:
        return False
    # 获取初始值类型
    query_label = get_column_label(item.queryField)
    # 获取初始值范围
    if item.queryPeriodEnd == 1:
        data_first = data[query_label].tail(item.queryPeriodBegin)
    elif item.queryPeriodBegin == item.queryPeriodEnd:
        data_first = data[query_label].iloc[-item.queryPeriodBegin]
    else:
        data_first = data[query_label].iloc[-item.queryPeriodBegin:-(item.queryPeriodEnd - 1)]
    # 获取初始值
    value_first = get_data_value(item.queryLogic, data_first)
    # 获取参照值类型
    compared_label = get_column_label(item.comparedField)
    # 获取参照数据
    if item.comparedObject == '绝对值':
        value_second = item.value
    else:
        # 上市天数少于指标范围则跳过
        if data.shape[0] < item.comparedPeriodBegin:
            return False
        # 获取参照值范围
        if item.comparedPeriodEnd == 1:
            data_second = data[compared_label].tail(item.comparedPeriodBegin)
        elif item.comparedPeriodBegin == item.comparedPeriodEnd:
            data_second = data[compared_label].iloc[-item.comparedPeriodBegin]
        else:
            data_second = data[compared_label].iloc[-item.comparedPeriodBegin:-(item.comparedPeriodEnd - 1)]
        # 获取参照值
        if item.comparedObject == '差值':
            value_second = get_data_value(item.comparedLogic, data_second) + item.value
        else:
            value_second = get_data_value(item.comparedLogic, data_second) * item.value

    # 返回比较结果
    if item.operator == '大于':
        return value_first > value_second
    elif item.operator == '小于':
        return value_first < value_second
    else:
        return value_first == value_second


class SearchCriteria(QDialog, Ui_SearchCriteria):

    def __init__(self, criteria_item: CriteriaItem):
        super().__init__()
        self.setupUi(self)
        # 初始化指标下拉列表内容
        logic_items = ['平均', '累计', '最高', '最低']
        self.cbbQueryLogic.addItems(logic_items)
        self.cbbComparedLogic.addItems(logic_items)
        self.cbbOperator.addItems(['大于', '小于', '等于'])
        field_items = ['开盘价', '收盘价', '最高价', '最低价', '开盘涨跌幅', '收盘涨跌幅', '日内涨跌幅', '最高涨幅', '最低跌幅', '振幅', '换手率']
        self.cbbQueryField.addItems(field_items)
        self.cbbComparedField.addItems(field_items)
        self.criteriaItem = criteria_item
        self.read_item_data()

    # 从指标中初始化界面数值显示
    def read_item_data(self):
        self.cbbQueryLogic.setCurrentText(self.criteriaItem.queryLogic)
        self.cbbOperator.setCurrentText(self.criteriaItem.operator)
        self.cbbQueryField.setCurrentText(self.criteriaItem.queryField)
        self.spbQueryPeriodBegin.setValue(self.criteriaItem.queryPeriodBegin)
        self.spbQueryPeriodEnd.setValue(self.criteriaItem.queryPeriodEnd)
        self.spbComparedPeriodBegin.setValue(self.criteriaItem.comparedPeriodBegin)
        self.spbComparedPeriodEnd.setValue(self.criteriaItem.comparedPeriodEnd)
        self.cbbComparedLogic.setCurrentText(self.criteriaItem.comparedLogic)
        self.cbbComparedField.setCurrentText(self.criteriaItem.comparedField)
        if self.criteriaItem.comparedObject == '绝对值':
            self.rbnAbsValue.setChecked(True)
        elif self.criteriaItem.comparedObject == '差值':
            self.rbnDifference.setChecked(True)
        else:
            self.rbnRatio.setChecked(True)
        self.spbValue.setValue(self.criteriaItem.value)

    # 保存编辑后的指标
    def save_changes(self):
        self.criteriaItem.queryLogic = self.cbbQueryLogic.currentText()
        self.criteriaItem.comparedLogic = self.cbbComparedLogic.currentText()
        self.criteriaItem.queryField = self.cbbQueryField.currentText()
        self.criteriaItem.comparedField = self.cbbComparedField.currentText()
        self.criteriaItem.queryPeriodBegin = self.spbQueryPeriodBegin.value()
        self.criteriaItem.queryPeriodEnd = self.spbQueryPeriodEnd.value()
        self.criteriaItem.comparedPeriodBegin = self.spbComparedPeriodBegin.value()
        self.criteriaItem.comparedPeriodEnd = self.spbComparedPeriodEnd.value()
        self.criteriaItem.operator = self.cbbOperator.currentText()

        if self.rbnAbsValue.isChecked():
            self.criteriaItem.comparedObject = '绝对值'
        elif self.rbnDifference.isChecked():
            self.criteriaItem.comparedObject = '差值'
        else:
            self.criteriaItem.comparedObject = '比值'
        self.criteriaItem.value = self.spbValue.value()
        StockFinder.Instance.update_criteria_list(self.criteriaItem)
        self.close()

    # 根据数据情况更新GUI显示
    def update_gui(self):
        # 避免开始时间短于结束时间
        if self.spbQueryPeriodBegin.value() < self.spbQueryPeriodEnd.value():
            temp = self.spbQueryPeriodEnd.value()
            self.spbQueryPeriodEnd.setValue(self.spbQueryPeriodBegin.value())
            self.spbQueryPeriodBegin.setValue(temp)
        if self.spbComparedPeriodBegin.value() < self.spbComparedPeriodEnd.value():
            temp = self.spbComparedPeriodEnd.value()
            self.spbComparedPeriodEnd.setValue(self.spbComparedPeriodBegin.value())
            self.spbComparedPeriodBegin.setValue(temp)
        # 当开始结束同一天时禁用数值选取逻辑
        self.cbbQueryLogic.setEnabled(self.spbQueryPeriodBegin.value() != self.spbQueryPeriodEnd.value())
        self.cbbComparedLogic.setEnabled(self.spbComparedPeriodBegin.value() != self.spbComparedPeriodEnd.value())
