from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from QtDesign.LiveTracker_ui import Ui_LiveTracker
from PyQt5.QtCore import QThread, pyqtSignal
import Data.FileManager as FileManager
from Data.RealTimeStockData import *
import time
import Tools
import urllib.request as url



# 读取股票最近几条交易记录数据
def parse_recent_history(data):
    logs = data.split('|')
    histories = []
    for log in logs:
        log_split = log.split('/')
        history = RecentTradeHistory()
        history.time = log_split[0]
        history.price = float(log_split[1])
        history.volume = int(log_split[2])
        history.direction = log_split[3]
        history.worth = int(log_split[4])
        history.totalTradeCount = int(log_split[5])
        histories.append(history)
    return histories


liveTrackerInstance = None


class LiveTracker(QMainWindow, Ui_LiveTracker):
    stocksToMonitor = []
    StockMonitor = None
    stockData = {"": []}

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        global liveTrackerInstance
        liveTrackerInstance = self

    # 导入股票列表
    def import_stock_list(self):
        file_path = FileManager.import_selected_stock_list()
        if file_path[0] != "":
            file = open(file_path[0], "r")
            for line in file:
                code = line.rstrip('\n')
                self.add_stock_to_list(code)
            file.close()

    # 在列表中插入一只股票
    def add_stock_to_list(self, code):
        row_count = self.tblStockList.rowCount()
        self.tblStockList.insertRow(row_count)
        self.stocksToMonitor.append(code)
        self.tblStockList.setItem(row_count, 0, QTableWidgetItem(code))
        name = Tools.get_stock_name(code)
        self.tblStockList.setItem(row_count, 1, QTableWidgetItem(name))

    # 添加一只股票
    def add_stock_code(self):
        code = self.iptStockCode.text()
        self.add_stock_to_list(code)
        self.StockMonitor.update_stock_list(self.reformat_stock_list())

    # 移除一只股票
    def remove_stock_code(self):
        pass

    # 清空股票列表
    def clear_stock_list(self):
        self.stop_monitoring()
        self.stocksToMonitor = []
        self.tblStockList.clear()

    # 开始实时盯盘
    def start_monitoring(self):
        self.btnStartTracking.setEnabled(False)
        self.btnStopTracking.setEnabled(True)
        self.StockMonitor = StockMonitor(self.reformat_stock_list())
        self.StockMonitor.getInfoCallback.connect(self.parse_stock_live_data)
        self.StockMonitor.start()

    def reformat_stock_list(self):
        line = ""
        for code in self.stocksToMonitor:
            market = Tools.get_trade_center(code)
            line += market + code + ","
        return line[:-1]

    # 停止实时盯盘
    def stop_monitoring(self):
        self.btnStartTracking.setEnabled(True)
        self.btnStopTracking.setEnabled(False)
        self.StockMonitor.isMonitoring = False
        self.lblLastUpdateTime.setText("上次刷新：")
        self.stockData = {"": []}

    # 更新股票列表显示
    def update_stock_table(self):
        for i in range(len(self.stocksToMonitor)):
            code = self.stocksToMonitor[i]
            data = self.stockData[code][-1]
            Tools.add_price_item(self.tblStockList, data.currentPrice, data.previousClose, i, 2)
        self.lblLastUpdateTime.setText("上次刷新：" + time.strftime("%H:%M:%S"))

    # 得到实时行情的回调
    def parse_stock_live_data(self, data):
        for line in data:
            info = str(line).split('~')
            stock_data = RealTimeStockData()
            code = info[2]
            stock_data.currentPrice = float(info[3])
            stock_data.previousClose = float(info[4])
            stock_data.open = float(info[5])
            stock_data.totalVolume = int(info[6])
            stock_data.totalBuyVolume = int(info[7])
            stock_data.totalSellVolume = int(info[8])
            buy_sell_info = BuySellInfo()
            buy_sell_info.buyPrice1 = float(info[9])
            buy_sell_info.buyVolume1 = int(info[10])
            buy_sell_info.buyPrice2 = float(info[11])
            buy_sell_info.buyVolume2 = int(info[12])
            buy_sell_info.buyPrice3 = float(info[13])
            buy_sell_info.buyVolume3 = int(info[14])
            buy_sell_info.buyPrice4 = float(info[15])
            buy_sell_info.buyVolume4 = int(info[16])
            buy_sell_info.buyPrice5 = float(info[17])
            buy_sell_info.buyVolume5 = int(info[18])
            buy_sell_info.sellPrice1 = float(info[19])
            buy_sell_info.sellVolume1 = int(info[20])
            buy_sell_info.sellPrice2 = float(info[21])
            buy_sell_info.sellVolume2 = int(info[22])
            buy_sell_info.sellPrice3 = float(info[23])
            buy_sell_info.sellVolume3 = int(info[24])
            buy_sell_info.sellPrice4 = float(info[25])
            buy_sell_info.sellVolume4 = int(info[26])
            buy_sell_info.sellPrice5 = float(info[27])
            buy_sell_info.sellVolume5 = int(info[28])
            stock_data.buySellInfo = buy_sell_info
            stock_data.recentTradeHistory = parse_recent_history(info[29])
            stock_data.percentChange = float(info[32])

            if code not in self.stockData:
                self.stockData[code] = []
            self.stockData[code].append(stock_data)
            if len(self.stockData[code]) > 10:
                self.stockData[code].pop(0)
        self.update_stock_table()


class StockMonitor(QThread):
    getInfoCallback = pyqtSignal(object)
    isMonitoring = True

    def __init__(self, stock_list):
        super().__init__()
        self.url = "http://qt.gtimg.cn/q=" + stock_list

    def __del__(self):
        self.work = False
        self.terminate()

    def update_stock_list(self, stock_list):
        self.url = "http://qt.gtimg.cn/q=" + stock_list

    def run(self):
        while self.isMonitoring:
            data = url.urlopen(self.url)
            self.getInfoCallback.emit(data)
            time.sleep(liveTrackerInstance.spbUpdateFrequency.value())
