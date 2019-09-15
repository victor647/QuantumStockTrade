from QtDesign.SearchResult_ui import Ui_SearchResult
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QFileDialog
import Tools
import webbrowser
import os.path as path


class SearchResult(QDialog, Ui_SearchResult):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    # 更新已找到的股票数量
    def update_found_stock_count(self):
        self.lblTotalStockFound.setText("共找到" + str(self.tblStockList.rowCount()) + "只股票!")

    # 在列表中添加一只找到的股票
    def add_stock_item(self, items):
        row_count = self.tblStockList.rowCount()
        self.tblStockList.insertRow(row_count)
        for i in range(len(items)):
            item = QTableWidgetItem(str(items[i]))
            self.tblStockList.setItem(row_count, i, item)
        self.update_found_stock_count()

    # 在东方财富网站打开股票主页
    def open_stock_page(self, row, column):
        if column != 0:
            return
        code = self.tblStockList.item(row, 0).text()
        market = Tools.get_trade_center(code)
        webbrowser.open("http://quote.eastmoney.com/" + market + code + ".html")

    # 导出找到的股票列表到txt文件
    def export_stock_list(self):
        parent = path.join(path.pardir, "StockData", "SelectedStocks")
        file_path = QFileDialog.getSaveFileName(directory=parent, filter='TXT(*.txt)')
        if file_path[0] != "":
            file = open(file_path[0], "w")
            for i in range(self.tblStockList.rowCount()):
                text = self.tblStockList.item(i, 0).text()
                file.write(text + "\n")
            file.close()
