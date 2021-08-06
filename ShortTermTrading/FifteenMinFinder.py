from QtDesign.FifteenMinFinder_ui import Ui_FifteenMinFinder
from Tools import FileManager, Tools
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QHeaderView, QFileDialog

# 15分钟K线选股
class FifteenMinFinder(QDialog, Ui_FifteenMinFinder):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup_triggers()

    def setup_triggers(self):
        self.btnImportStockPool.clicked.connect(self.import_stock_pool)

    # 从文件导入股票池
    def import_stock_pool(self):
        FileManager.import_stock_list(self.fill_stock_list)

    # 根据导入的选股列表文件填表
    def fill_stock_list(self, code: str):
        name = Tools.get_stock_name_from_code(code)
        if name == '':
            return
        row_count = self.tblStockList.rowCount()
        self.tblStockList.insertRow(row_count)
        self.tblStockList.setItem(row_count, 0, QTableWidgetItem(code))
        self.tblStockList.setItem(row_count, 1, QTableWidgetItem(name))
        self.tblStockList.repaint()