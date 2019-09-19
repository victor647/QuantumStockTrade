from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView, QMessageBox
from QtDesign.LiveTracker_ui import Ui_LiveTracker
from PyQt5.QtCore import QThread, pyqtSignal
import Data.FileManager as FileManager
import RealTimeMonitor.RealTimeStockData as RealTimeStockData
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
        # 最近异动提醒记录
        self.__recentMessages = dict()
        # 初始化下拉列表内容
        self.cbbRecentMeasurement.addItems(['次交易', '分钟'])
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
    def add_stock_to_list(self, code: str):
        # 去除重复股票代码
        if code in self.__stocksToMonitor:
            return
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
            self.__StockMonitor.update_stock_watch_list(self.__stocksToMonitor)

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
            self.stop_monitoring()
        else:
            # 删除单只股票数据
            del self.__stockRecentTransactions[code]
            del self.__stockLiveData[code]

    # 清空股票列表
    def clear_stock_list(self):
        self.stop_monitoring()
        self.__stocksToMonitor = []
        # 重置交易记录和实时数据
        self.__stockRecentTransactions = dict()
        self.__stockLiveData = dict()
        self.tblStockList.setRowCount(0)

    # 开始实时盯盘
    def start_monitoring(self):
        if len(self.__stocksToMonitor) == 0:
            return
        # 切换开关状态
        global isMonitoring
        isMonitoring = True
        # UI按钮开关调整
        self.btnStartTracking.setEnabled(False)
        self.btnStopTracking.setEnabled(True)
        self.__StockMonitor = StockMonitor()
        # 读取需要盯盘的股票列表
        self.__StockMonitor.update_stock_watch_list(self.__stocksToMonitor)
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

    # 更新窗口股票列表信息显示
    def update_stock_table(self):
        for row in range(len(self.__stocksToMonitor)):
            # 通过表格当前行数获得股票代码
            code = self.__stocksToMonitor[row]
            # 获取当前股票实时数据
            live_data = self.__stockLiveData[code]
            # 获取当前股票交易记录全数据
            stock_transaction_database = self.__stockRecentTransactions[code]
            # 获取指定规则下最近交易记录列表
            if self.cbbRecentMeasurement.currentIndex() == 0:
                # 按照交易次数选取
                recent_transactions_list = RealTimeStockData.fetch_recent_transactions_by_count(stock_transaction_database, self.spbRecentMeasureCount.value())
            else:
                # 按照交易时间选取
                recent_transactions_list = RealTimeStockData.fetch_recent_transactions_by_minute(stock_transaction_database, self.spbRecentMeasureCount.value())
            # 数据初始列数
            column = 2
            # 最近成交记录
            newest_transaction = recent_transactions_list[0]
            info = Tools.time_int_to_string(newest_transaction.time) + "  " + str(newest_transaction.volume) + "手" + newest_transaction.direction
            self.tblStockList.setItem(row, column, QTableWidgetItem(info))
            column += 1
            # 最新价格
            Tools.add_colored_item(self.tblStockList, live_data.currentPrice, row, column, threshold=live_data.previousClose)
            column += 1
            # 涨跌幅
            Tools.add_colored_item(self.tblStockList, live_data.percentChange, row, column, "%")
            column += 1
            self.check_daily_percentage(code, live_data.percentChange)
            # 五档委比数据
            ratio = live_data.bidInfo.get_bid_ratio()
            Tools.add_colored_item(self.tblStockList, ratio, row, column, "%")
            column += 1
            self.check_bid_ratio(code, ratio)
            # 最近涨跌幅
            change = RealTimeStockData.get_recent_change(recent_transactions_list)
            ratio = round(change / live_data.previousClose * 100, 2)
            Tools.add_colored_item(self.tblStockList, ratio, row, column, "%")
            column += 1
            self.check_short_term_percentage(code, ratio)
            # 最近成交外盘占比
            ratio = RealTimeStockData.get_active_buy_ratio(recent_transactions_list)
            Tools.add_colored_item(self.tblStockList, ratio, row, column, "%", 50)
            column += 1
            self.check_short_term_active_buy(code, ratio)
            # 最近成交额
            amount = RealTimeStockData.get_total_amount(recent_transactions_list)
            self.tblStockList.setItem(row, column, QTableWidgetItem(str(amount) + "万"))
            self.check_short_term_amount(code, amount)

        # 更新上次刷新列表时间
        self.lblLastUpdateTime.setText("上次刷新：" + time.strftime("%H:%M:%S"))

    # 检测涨跌幅是否达到设定值
    def check_daily_percentage(self, code: str, percent: float):
        if percent > self.spbDailyPercentChange.value():
            QMessageBox.information(self, "个股异动提示", code + "当前日内涨幅达到" + str(percent) + "%")
        elif percent < self.spbDailyPercentChange.value() * -1:
            QMessageBox.information(self, "个股异动提示", code + "当前日内跌幅达到" + str(percent) + "%")

    # 检测最近涨跌幅是否达到设定值
    def check_short_term_percentage(self, code: str, percent: float):
        if percent > self.spbShortTermPercentChange.value():
            QMessageBox.information(self, "个股异动提示", code + "短时涨幅达到" + str(percent) + "%")
        elif percent < self.spbShortTermPercentChange.value() * -1:
            QMessageBox.information(self, "个股异动提示", code + "短时跌幅达到" + str(percent) + "%")

    # 检测委比是否达到设定值
    def check_bid_ratio(self, code: str, ratio: float):
        if ratio > self.spbBuyBidPercent.value():
            QMessageBox.information(self, "个股异动提示", code + "委比高于" + str(ratio) + "%")
        elif ratio < self.spbBuyBidPercent.value() * -1:
            QMessageBox.information(self, "个股异动提示", code + "委比低于" + str(ratio) + "%")

    # 检测短时内外盘占比是否达到设定值
    def check_short_term_active_buy(self, code: str, percent: float):
        if percent > self.spbActiveBuyPercent.value():
            QMessageBox.information(self, "个股异动提示", code + "短时外盘达到" + str(percent) + "%")
        elif percent < 100 - self.spbActiveBuyPercent.value():
            QMessageBox.information(self, "个股异动提示", code + "短时内盘达到" + str(100 - percent) + "%")

    # 检测短时成交额是否达到设定值
    def check_short_term_amount(self, code: str, amount: float):
        if amount > self.spbShortTermAmount.value():
            QMessageBox.information(self, "个股异动提示", code + "短时成交额达到" + str(amount) + "万")

    def add_message_log(self, code: str, text: str):
        if self.__recentMessages[code]
        QMessageBox.information(self, "个股异动提示", code + text)


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
    def update_stock_watch_list(self, stock_list):
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
