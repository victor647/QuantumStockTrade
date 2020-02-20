from QtDesign.SearchResult_ui import Ui_SearchResult
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from Tools import Tools, FileManager
import Data.HistoryGraph as HistoryGraph


class SearchResult(QDialog, Ui_SearchResult):

    def __init__(self, search_date: str):
        super().__init__()
        self.setupUi(self)
        self.__searchDate = search_date
        # 显示选股日期
        self.lblSearchDate.setText('选股日期：' + search_date)
        # 为表格自动设置列宽
        self.tblStockList.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    # 快捷键设置
    def keyPressEvent(self, key: QKeyEvent):
        # Esc键清除选择
        if key.key() == Qt.Key_Escape:
            self.tblStockList.clearSelection()
        # 按删除键删除股票或指标组
        elif key.key() == Qt.Key_Delete or key.key() == Qt.Key_Backspace:
            self.delete_selected_stocks()

    # 更新已找到的股票数量
    def update_found_stock_count(self):
        self.lblTotalStockFound.setText('共找到{}只股票!'.format(self.tblStockList.rowCount()))

    # 在列表中添加一只找到的股票
    def add_stock_item(self, items: list):
        row_count = self.tblStockList.rowCount()
        self.tblStockList.insertRow(row_count)
        for i in range(len(items)):
            item = QTableWidgetItem()
            item.setData(Qt.DisplayRole, items[i])
            self.tblStockList.setItem(row_count, i, item)
        self.update_found_stock_count()

    # 显示股票详细数据
    def stock_detailed_info(self, row: int, column: int):
        code = self.tblStockList.item(row, 0).text()
        # 通过网页打开
        if column > 1:
            Tools.open_stock_page(code)
        # 直接画K线图
        else:
            HistoryGraph.plot_stock_search_status(code, self.__searchDate)

    # 删除所选中的股票
    def delete_selected_stocks(self):
        for item in self.tblStockList.selectedItems():
            self.tblStockList.removeRow(item.row())
        self.update_found_stock_count()

    # 导出找到的股票列表到txt文件
    def export_stock_list(self):
        FileManager.export_stock_list(self.tblStockList, self.__searchDate)
