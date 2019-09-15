from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from QtDesign.LiveTracker_ui import Ui_LiveTracker
import Data.FileManager as FileManager
import baostock.realtime.subscibe as baostock
import Tools


class LiveTracker(QMainWindow, Ui_LiveTracker):
    stocksToMonitor = []
    subscriptionId = 0

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    # 导入股票列表
    def import_stock_list(self):
        file_path = FileManager.import_selected_stock_list()
        if file_path[0] != "":
            file = open(file_path[0], "r")
            for line in file:
                code = line.rstrip('\n')
                row_count = self.tblStockList.rowCount()
                self.tblStockList.insertRow(row_count)
                market = Tools.get_trade_center(code)
                self.stocksToMonitor.append(market + '.' + code)
                self.tblStockList.setItem(row_count, 0, QTableWidgetItem(code))
            file.close()

    # 添加一只股票
    def add_stock_code(self):
        pass

    # 移除一只股票
    def remove_stock_code(self):
        pass

    # 清空股票列表
    def clear_stock_list(self):
        pass

    # 开始实时盯盘
    def start_monitoring(self):
        line = ""
        for code in self.stocksToMonitor:
            line += code + ","
        result = baostock.subscribe_by_code(code_list=line, fncallback=self.stock_live_callback)
        self.subscriptionId = result.serial_id

    # 停止实时盯盘
    def stop_monitoring(self):
        baostock.cancel_subscribe(self.subscriptionId)

    # 得到实时行情的回调
    def stock_live_callback(self, result_data):
        print(result_data.data)
