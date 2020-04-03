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
        column = 0
        # 股票代码
        self.tblStockList.setItem(row_count, column, QTableWidgetItem(items[column]))
        column += 1
        # 股票名称
        self.tblStockList.setItem(row_count, column, QTableWidgetItem(items[column]))
        column += 1
        # 选股日收盘价
        column = Tools.add_sortable_item(self.tblStockList, row_count, column, items[column])
        # 次日开盘、五日收盘、默认收益、次日最低、五日最高、最大收益
        for i in range(6):
            column = Tools.add_colored_item(self.tblStockList, row_count, column, items[column], '%')
        # 股票行业
        self.tblStockList.setItem(row_count, column, QTableWidgetItem(items[column]))
        column += 1
        # 股票地区
        self.tblStockList.setItem(row_count, column, QTableWidgetItem(items[column]))
        column += 1
        # 市盈率
        column = Tools.add_sortable_item(self.tblStockList, row_count, column, items[column])
        # 市净率
        column = Tools.add_sortable_item(self.tblStockList, row_count, column, items[column])
        # 总市值
        column = Tools.add_sortable_item(self.tblStockList, row_count, column, items[column], str(items[column]) + '亿')
        # 净资产收益率
        Tools.add_sortable_item(self.tblStockList, row_count, column, items[column], str(items[column]) + '%')
        self.update_found_stock_count()

    # 显示股票详细数据
    def stock_detailed_info(self, row: int, column: int):
        code = self.tblStockList.item(row, 0).text()
        # 通过网页打开
        if column > 8:
            Tools.open_stock_page(code)
        # 大盘K线图
        elif column == 5:
            market, index = Tools.get_trade_center_and_index(code)
            HistoryGraph.plot_stock_search_status(market + index, self.__searchDate)
        # 股票K线图
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
