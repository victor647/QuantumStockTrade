from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QDialog, QMessageBox
from QtDesign.BatchSearcher_ui import Ui_BatchSearcher
import StockSearcher.StockFinder as StockFinder
import FileManager


# 批量选股工具
class BatchSearcher(QDialog, Ui_BatchSearcher):
    current_searching_date = QDate()
    output_folder = ""
    criteriaName = ""

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
        # 设定选股条件名称作为导出文件名
        self.criteriaName = self.iptCriteriaName.text()
        # 设定首个选股日期
        self.current_searching_date = self.dteStartDate.date()
        # 选取选股结果输出文件夹
        self.output_folder = FileManager.select_folder()
        if self.output_folder == "":
            return
        # 从开始日期开始每经过间隔日期选股一次
        StockFinder.stockFinderInstance.auto_search(self)

    # 进入下一个选股日期
    def move_to_next_date(self):
        if self.cbbIntervalType.currentText() == "日":
            self.current_searching_date = self.current_searching_date.addDays(self.spbInterval.value())
        elif self.cbbIntervalType.currentText() == "周":
            self.current_searching_date = self.current_searching_date.addDays(self.spbInterval.value() * 7)
        else:
            self.current_searching_date = self.current_searching_date.addMonths(self.spbInterval.value())
        # 日期没达到结束点，继续选股
        if self.current_searching_date < self.dteEndDate.date():
            StockFinder.stockFinderInstance.auto_search(self)
        else:
            StockFinder.stockFinderInstance.progressBar.close()
            QMessageBox.information(self, "成功", "批量自动选股已完成！")
            self.close()



