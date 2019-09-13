from QtDesign.SearchCriteria_ui import Ui_SearchCriteria
from PyQt5.QtWidgets import QDialog
import Tools

class CriteriaItem:
    logic = "平均"
    operator = "大于"
    field = "股价"
    daysCountFirst = 1
    daysCountSecond = 5
    useAbsValue = False
    relativePercentage = 20
    absoluteValue = 10


class SearchCriteria(QDialog, Ui_SearchCriteria):

    def __init__(self, stock_finder, criteria_item):
        super().__init__()
        self.setupUi(self)
        self.stockFinder = stock_finder
        self.cbbQueryLogic.addItems(['平均', '累计', '连续', '最高', '最低'])
        self.cbbOperator.addItems(['大于', '小于'])
        self.cbbComparisonItem.addItems(['股价', '涨跌幅', '换手率'])
        self.criteriaItem = criteria_item

    def save_changes(self):
        self.criteriaItem.logic = self.cbbQueryLogic.currentText()
        self.criteriaItem.operator = self.cbbOperator.currentText()
        self.criteriaItem.field = self.cbbComparisonItem.currentText()
        self.criteriaItem.daysCountFirst = self.spbFirstPeriod.value()
        self.criteriaItem.useAbsValue = self.rbnAbsValue.isChecked()
        self.criteriaItem.daysCountSecond = self.spbAveragePeriod.value()
        self.criteriaItem.relativePercentage = self.spbRelativePercentage.value()
        self.criteriaItem.absoluteValue = self.spbAbsValue.value()
        self.close()

    def discard_changes(self):
        self.close()


