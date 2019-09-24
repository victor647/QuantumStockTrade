from PyQt5.QtWidgets import QMainWindow, QMessageBox
from QtDesign.LiveTracker_ui import Ui_LiveTracker
from PyQt5.QtCore import QThread, pyqtSignal
import Data.FileManager as FileManager
from RealTimeMonitor.MonitorCondition import *
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
        # 每只股票实时数据
        self.__stockLiveData = dict()
        # 盯盘的股票代码列表
        self.__stocksToMonitor = list()
        # 初始化下拉列表内容
        self.cbbRecentMeasurement.addItems(['次交易', '分钟'])

    # 快捷键设置
    def keyPressEvent(self, key: QKeyEvent):
        # Esc键清除选择
        if key.key() == Qt.Key_Escape:
            self.tblStockList.clearSelection()
            self.trwMonitorConditions.clearSelection()
        # 按删除键删除股票或指标组
        elif key.key() == Qt.Key_Delete or key.key() == Qt.Key_Backspace:
            if self.tblStockList.selectedItems() is not None:
                self.remove_stock_code()
            if self.trwMonitorConditions.selectedItems() is not None:
                self.delete_condition()
        # 按回车键编辑指标组
        elif key.key() == Qt.Key_Enter:
            if self.trwMonitorConditions.selectedItems() is not None:
                self.edit_condition()

    # 在东方财富网站打开股票主页
    def open_stock_page(self, row: int, column: int):
        if column != 0:
            return
        code = self.tblStockList.item(row, 0).text()
        Tools.open_stock_page(code)

    # 导入股票列表
    def import_stock_list(self):
        FileManager.import_stock_list(self.add_stock_to_watch_list)

    # 导出股票列表
    def export_stock_list(self):
        FileManager.export_stock_list(self.tblStockList)

    # 在列表中插入一只股票
    def add_stock_to_watch_list(self, code: str):
        # 去除重复股票代码
        if code in self.__stocksToMonitor:
            return
        row_count = self.tblStockList.rowCount()
        self.tblStockList.insertRow(row_count)
        # 获取股票名称
        name = Tools.get_stock_name(code)
        # 加入盯盘代码列表
        self.__stocksToMonitor.append(code)
        # 生成盯盘指标根节点
        code_node = QTreeWidgetItem(self.trwMonitorConditions, [code + " " + name])
        self.__stockLiveData[code] = RealTimeStockData.StockMonitorData(code_node, code)
        # 在窗口列表中添加股票信息
        self.tblStockList.setItem(row_count, 0, QTableWidgetItem(code))
        self.tblStockList.setItem(row_count, 1, QTableWidgetItem(name))

    # 添加股票按钮
    def add_stock_code(self):
        code = self.iptStockCode.text()
        self.add_stock_to_watch_list(code)
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
        self.trwMonitorConditions.invisibleRootItem().removeChild(self.__stockLiveData[code].codeNode)
        if len(self.__stocksToMonitor) == 0:
            # 清空整个列表
            self.stop_monitoring()
        else:
            # 删除单只股票数据
            del self.__stockLiveData[code]

    # 清空股票列表
    def clear_stock_list(self):
        self.stop_monitoring()
        self.__stocksToMonitor = []
        # 重置股票实时数据
        self.__stockLiveData = dict()
        self.tblStockList.setRowCount(0)
        # 重置盯盘指标树状图
        self.trwMonitorConditions.clear()

    # 添加盯盘指标组合
    def add_condition(self):
        # 未选中则跳过
        if len(self.trwMonitorConditions.selectedItems()) == 0:
            return
        selected_item = self.trwMonitorConditions.selectedItems()[0]
        parent = selected_item.parent()
        # 如果选中的是股票代码
        if parent is None:
            code = selected_item.text(0).split(' ')[0]
            self.__stockLiveData[code].add_monitor_condition_group()
            selected_item.setExpanded(True)
        # 如果选中的是其他指标组
        elif parent.parent() is None:
            code = parent.text(0).split(' ')[0]
            self.__stockLiveData[code].add_monitor_condition_group()
            parent.setExpanded(True)

    # 删除盯盘指标组合
    def delete_condition(self):
        if len(self.trwMonitorConditions.selectedItems()) == 0:
            return
        selected_item = self.trwMonitorConditions.selectedItems()[0]
        parent = selected_item.parent()
        # 如果选中的是股票代码则跳过
        if parent is None:
            return
        # 如果选中的是条件组，则没有上上层
        if parent.parent() is None:
            # 获取股票代码
            code = parent.text(0).split(' ')[0]
            # 删除条件组
            self.__stockLiveData[code].remove_monitor_condition_group(selected_item)

    # 编辑盯盘指标组合
    def edit_condition(self):
        if len(self.trwMonitorConditions.selectedItems()) == 0:
            return
        selected_item = self.trwMonitorConditions.selectedItems()[0]
        self.edit_monitor_condition(selected_item)

    # 打开编辑界面
    def edit_monitor_condition(self, selected_item: QTreeWidgetItem):
        parent = selected_item.parent()
        # 如果选中的是股票代码根节点
        if parent is None:
            # 如果没有条件组则添加一个
            if selected_item.childCount() == 0:
                code = selected_item.text(0).split(' ')[0]
                self.__stockLiveData[code].add_monitor_condition_group()
                selected_item.setExpanded(True)
            return
        # 获取股票代码根节点
        code_node = parent.parent()
        # 如果选中的是条件组则编辑当前条件组
        if code_node is None:
            code = parent.text(0).split(' ')[0]
            # 获取选中指标组合的排位
            index_group = parent.indexOfChild(selected_item)
            monitor = MonitorConditionEditor(self.__stockLiveData[code].monitorConditionGroups[index_group])
            monitor.show()
            monitor.exec_()
        # 编辑所选的指标
        else:
            # 获取股票代码
            code = code_node.text(0).split(' ')[0]
            # 获取选中指标组合的排位
            index_group = code_node.indexOfChild(parent)
            monitor = MonitorConditionEditor(self.__stockLiveData[code].monitorConditionGroups[index_group])
            monitor.show()
            monitor.exec_()

    def copy_condition(self):
        pass

    def paste_condition(self):
        pass

    # 从json文件导入每只股票的盯盘指标
    def import_conditions(self):
        for data in self.__stockLiveData.values():
            # 从配置文件导入json数据
            json_data = FileManager.import_json_config(FileManager.monitor_config_path(data.code))
            # 初始化盯盘条件组
            data.monitorConditionGroups = []
            for group in json_data:
                item_group = ConditionItemGroup.deserialize_from_json(group)
                data.create_item_group_node(item_group)
                data.monitorConditionGroups.append(item_group)
                for i in range(len(item_group.conditionItems)):
                    item_group.create_individual_item_node(item_group.conditionItems[i], i)

    # 导出每只股票的盯盘指标到json文件
    def export_conditions(self):
        for data in self.__stockLiveData.values():
            FileManager.export_config_as_json(data.monitorConditionGroups, FileManager.monitor_config_path(data.code))

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
            # 获取指定规则下最近交易记录列表
            if self.cbbRecentMeasurement.currentIndex() == 0:
                # 按照交易次数选取
                recent_transactions_list = self.__stockLiveData[code].fetch_recent_transactions_by_count(self.spbRecentMeasureCount.value())
            else:
                # 按照交易时间选取
                recent_transactions_list = self.__stockLiveData[code].fetch_recent_transactions_by_minute(self.spbRecentMeasureCount.value())
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
            # 五档委比数据
            ratio = live_data.bidInfo.get_bid_ratio()
            Tools.add_colored_item(self.tblStockList, ratio, row, column, "%")
            column += 1
            # 最近涨跌幅
            change = RealTimeStockData.get_recent_change(recent_transactions_list)
            ratio = round(change / live_data.previousClose * 100, 2)
            Tools.add_colored_item(self.tblStockList, ratio, row, column, "%")
            column += 1
            # 最近成交外盘占比
            ratio = RealTimeStockData.get_active_buy_ratio(recent_transactions_list)
            Tools.add_colored_item(self.tblStockList, ratio, row, column, "%", 50)
            column += 1
            # 最近成交额
            amount = RealTimeStockData.get_total_amount(recent_transactions_list)
            self.tblStockList.setItem(row, column, QTableWidgetItem(str(amount) + "万"))

            self.__stockLiveData[code].analyze_stock_data(recent_transactions_list)

        # 更新上次刷新列表时间
        self.lblLastUpdateTime.setText("上次刷新：" + time.strftime("%H:%M:%S"))

    # 发布异动提示消息
    def add_message_log(self, code: str, message: str):
        name = Tools.get_stock_name(code)
        QMessageBox.information(self, "个股异动提示", code + name + message)

    # 得到实时行情的回调
    def parse_stock_live_data(self, url_data):
        # 获取每只股票的实时数据
        for stock_data in url_data:
            # 将长串字符分隔
            live_info_list = str(stock_data).split('~')
            # 获取股票代码
            code = live_info_list[2]
            # 更新股票实时价格和交易信息
            self.__stockLiveData[code].update_stock_data(live_info_list)
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
