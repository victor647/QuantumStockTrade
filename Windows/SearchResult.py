from QtDesign.SearchResult_ui import Ui_SearchResult
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
import Tools
import webbrowser


class SearchResult(QDialog, Ui_SearchResult):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def finish_searching(self):
        self.lblTotalStockFound.setText("共找到" + str(self.tblStockList.rowCount()) + "只股票!")

    def get_stock_list(self, stock_list):
        for stock in stock_list:
            self.add_stock_item(stock)

    def add_stock_item(self, items):
        row_count = self.tblStockList.rowCount()
        self.tblStockList.insertRow(row_count)
        for i in range(len(items)):
            item = QTableWidgetItem(str(items[i]))
            self.tblStockList.setItem(row_count, i, item)

    def open_stock_page(self, row, column):
        if column != 0:
            return
        code = self.tblStockList.item(row, 0).text()
        market = Tools.get_trade_center(code)
        webbrowser.open("http://quote.eastmoney.com/"+ market + code + ".html")


