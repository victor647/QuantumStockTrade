from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView
from QtDesign.LiveTracker_ui import Ui_LiveTracker
from PyQt5.QtCore import QThread, pyqtSignal
import Data.FileManager as FileManager
import Data.RealTimeStockData as RealTimeStockData
import time
import Tools
import urllib.request as url


liveTrackerInstance = None
isMonitoring = False


class LiveTracker(QMainWindow, Ui_LiveTracker):
    __StockMonitor = None

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        global liveTrackerInstance
        liveTrackerInstance = self
        # 每只股票当前的价格、成交量等信息
        self.__stockLiveData = dict()
        # 每只股票最近几分钟的成交记录
        self.__stockRecentTransactions = dict()
        # 盯盘的股票代码列表
        self.__stocksToMonitor = list()
        # 为表格自动设置列宽
        self.tblStockList.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

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
        # 加入盯盘代码列表
        self.__stocksToMonitor.append(code)
        # 初始化成交记录
        self.__stockRecentTransactions[code] = dict()
        # 获取股票名称
        name = Tools.get_stock_name(code)
        # 在窗口列表中添加股票信息
        self.tblStockList.setItem(row_count, 0, QTableWidgetItem(code))
        self.tblStockList.setItem(row_count, 1, QTableWidgetItem(name))

    # 添加股票按钮
    def add_stock_code(self):
        code = self.iptStockCode.text()
        self.add_stock_to_list(code)
        if isMonitoring:
            self.__StockMonitor.update_stock_list(self.__stocksToMonitor)

    # 移除一只股票
    def remove_stock_code(self):
        selection = self.tblStockList.selectedIndexes()
        if len(selection) == 0:
            return
        index = selection[0].row()
        code = self.tblStockList.item(index, 0).text()
        self.__stocksToMonitor.pop(index)
        self.tblStockList.removeRow(index)
        if len(self.__stocksToMonitor) == 0:
            # 清空整个列表
            self.clear_stock_list()
        else:
            # 删除单只股票数据
            del self.__stockRecentTransactions[code]
            del self.__stockLiveData[code]

    # 清空股票列表
    def clear_stock_list(self):
        self.stop_monitoring()
        self.__stocksToMonitor = []

    # 开始实时盯盘
    def start_monitoring(self):
        # 切换开关状态
        global isMonitoring
        isMonitoring = True
        # UI按钮开关调整
        self.btnStartTracking.setEnabled(False)
        self.btnStopTracking.setEnabled(True)
        self.__StockMonitor = StockMonitor()
        # 读取需要盯盘的股票列表
        self.__StockMonitor.update_stock_list(self.__stocksToMonitor)
        self.__StockMonitor.getInfoCallback.connect(self.parse_stock_live_data)
        self.__StockMonitor.start()

    # 停止实时盯盘
    def stop_monitoring(self):
        # 切换开关状态
        global isMonitoring
        isMonitoring = False
        # UI按钮开关调整
        self.btnStartTracking.setEnabled(True)
        self.btnStopTracking.setEnabled(False)
        # 重置刷新时间文字
        self.lblLastUpdateTime.setText("上次刷新：")
        # 重置交易记录和实时数据
        self.__stockRecentTransactions = dict()
        self.__stockLiveData = dict()

    # 更新窗口股票列表信息显示
    def update_stock_table(self):
        for i in range(len(self.__stocksToMonitor)):
            code = self.__stocksToMonitor[i]
            live_data = self.__stockLiveData[code]
            recent_transactions = self.__stockRecentTransactions[code]
            # 最新价格和涨跌幅数据
            Tools.add_price_item(self.tblStockList, live_data.currentPrice, live_data.previousClose, i, 2)
            # 五档委比数据
            Tools.add_colored_item(self.tblStockList, live_data.bidInfo.get_bid_ratio(), i, 3, "%")
            # 1分钟涨跌幅
            change = RealTimeStockData.get_one_minute_change(recent_transactions)
            ratio = round(change / live_data.previousClose * 100, 2)
            Tools.add_colored_item(self.tblStockList, ratio, i, 4, "%")
            # 1分钟外盘比例
            Tools.add_colored_item(self.tblStockList, RealTimeStockData.get_active_buy_ratio(recent_transactions), i, 5, "%", 50)
            # 1分钟成交额
            self.tblStockList.setItem(i, 6, QTableWidgetItem(str(RealTimeStockData.get_one_minute_worth(recent_transactions)) + "万"))

        # 更新上次刷新列表时间
        self.lblLastUpdateTime.setText("上次刷新：" + time.strftime("%H:%M:%S"))

    # 得到实时行情的回调
    def parse_stock_live_data(self, url_data):
        # 获取每只股票的实时数据
        for stock_data in url_data:
            # 将长串字符分隔
            live_info_list = str(stock_data).split('~')
            # 获取股票代码
            code = live_info_list[2]
            # 读取股票实时价格和买卖盘信息
            self.__stockLiveData[code] = RealTimeStockData.StockLiveStatus(code, live_info_list)
            # 读取股票最近6条成交记录
            RealTimeStockData.parse_recent_transactions(live_info_list[29], self.__stockRecentTransactions[code])
        # 更新窗口股票列表信息显示
        self.update_stock_table()


class StockMonitor(QThread):
    getInfoCallback = pyqtSignal(object)
    url = ""

    # 通过股票代码列表更新访问地址
    def update_stock_list(self, stock_list):
        line = ""
        for code in stock_list:
            market = Tools.get_trade_center(code)
            line += market + code + ","
        self.url = "http://qt.gtimg.cn/q=" + line[:-1]

    def run(self):
        while isMonitoring:
            # 从腾讯获取最新行情
            data = url.urlopen(self.url)
            # 将获得的数据传回主线程分析
            self.getInfoCallback.emit(data)
            # 根据设定的刷新频率循环
            time.sleep(liveTrackerInstance.spbUpdateFrequency.value())
