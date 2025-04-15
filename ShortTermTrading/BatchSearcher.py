from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QDialog
from QtDesign.BatchSearcher_ui import Ui_BatchSearcher
import ShortTermTrading.StockFinder as StockFinder


# 批量选股工具
class BatchSearcher(QDialog, Ui_BatchSearcher):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        today = QDate.currentDate()
        # 初始化日期显示
        self.dteStartDate.setDate(today.addMonths(-1))
        self.dteEndDate.setDate(today)
        # 初始化间隔选项
        self.cbbIntervalType.addItems(['日', '周', '月'])

    # 开始选股
    def start_searching(self):
        # 从开始日期开始每经过间隔日期选股一次
        StockFinder.Instance.auto_search(self, self.dteStartDate.date(), self.dteEndDate.date())

    # 进入下一个选股日期
    def move_to_next_date(self, current_searching_date: QDate):
        if self.cbbIntervalType.currentText() == '日':
            current_searching_date = current_searching_date.addDays(self.spbInterval.value())
            # 若不是交易日则继续往下加日期
            while current_searching_date.dayOfWeek() > 5:
                current_searching_date = current_searching_date.addDays(1)
        elif self.cbbIntervalType.currentText() == '周':
            current_searching_date = current_searching_date.addDays(self.spbInterval.value() * 7)
        else:
            current_searching_date = current_searching_date.addMonths(self.spbInterval.value())
        return current_searching_date



