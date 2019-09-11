from QtDesign.SearchResult_ui import Ui_SearchResult
from PyQt5.QtWidgets import QDialog, QTableWidgetItem


class SearchResult(QDialog, Ui_SearchResult):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def get_stock_list(self, stock_list):
        for stock in stock_list:
            self.add_stock_item(stock)

    def add_stock_item(self, item):
        row_count = self.tblStockList.rowCount()
        self.tblStockList.insertRow(row_count)
        self.tblStockList.setItem(row_count, 0, QTableWidgetItem(item[0]))
        self.tblStockList.setItem(row_count, 1, QTableWidgetItem(item[1]))
