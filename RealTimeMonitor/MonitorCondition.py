import time
import RealTimeMonitor.RealTimeStockData as RealTimeStockData
import RealTimeMonitor.LiveTracker as LiveTracker
from QtDesign.MonitorCondition_ui import Ui_MonitorCondition
from PyQt5.QtWidgets import QDialog, QTreeWidgetItem, QTableWidget, QTableWidgetItem, QComboBox


def base_message():
    return "最近" + LiveTracker.liveTrackerInstance.spbRecentMeasureCount + LiveTracker.liveTrackerInstance.cbbRecentMeasurement.currentText()


# 单条监测指标
class ConditionItem:

    def __init__(self, item_node: QTreeWidgetItem, index: int, field: str, value: str):
        self.field = field
        self.thresholdValue = float(value)
        self.message = ""
        item_node.setText(0, "指标" + str(index + 1))
        item_node.setText(1, field)
        item_node.setText(2, value)

    def match_condition(self, live_data: RealTimeStockData.StockMonitorData, recent_transactions: list):
        # 根据指标内容判断
        if self.field == "短时成交额":
            value = RealTimeStockData.get_total_amount(recent_transactions)
            if value > self.thresholdValue:
                self.message = base_message() + "成交额达到" + str(value) + "万元"
                return True
        elif self.field == "短时涨跌幅":
            value = RealTimeStockData.get_recent_change(recent_transactions)
            if value > self.thresholdValue:
                self.message = base_message() + "涨幅达到" + str(value) + "%"
                return True
            elif value < self.thresholdValue * -1:
                self.message = base_message() + "跌幅达到" + str(value) + "%"
                return True
        elif self.field == "日内涨跌幅":
            value = live_data.percentChange
            if value > self.thresholdValue:
                self.message = "日内涨幅达到" + str(value) + "%"
                return True
            elif value < self.thresholdValue * -1:
                self.message = "日内跌幅达到" + str(value) + "%"
                return True
        elif self.field == "短时内外盘占比":
            value = RealTimeStockData.get_active_buy_ratio(recent_transactions)
            if value > self.thresholdValue:
                self.message = base_message() + "外盘占比达到" + str(value) + "%"
                return True
            elif value < 100 - self.thresholdValue:
                self.message = base_message() + "内盘占比达到" + str(value) + "%"
                return True
        elif self.field == "当前委比":
            value = live_data.bidInfo.get_bid_ratio()
            if value > self.thresholdValue:
                self.message = "当前委比超过" + str(value) + "%"
                return True
            elif value < self.thresholdValue * -1:
                self.message = "当前委比低于" + str(value) + "%"
                return True
        return False


# 单个监测条件的所有监测指标
class ConditionItemGroup:
    lastTriggered = 0
    coolDownTime = 10
    name = ""

    def __init__(self, item_node: QTreeWidgetItem):
        self.itemNode = item_node
        self.name = item_node.text(0)
        self.conditionItems = []
        # 默认放一个指标进去
        child_node = QTreeWidgetItem()
        self.itemNode.addChild(child_node)
        self.conditionItems.append(ConditionItem(child_node, 0, "日内涨跌幅", "3"))

    # 设置指标组名称
    def set_name(self, name: str):
        self.itemNode.setText(0, name)
        self.name = name

    def check_condition_match(self, live_data: RealTimeStockData.StockMonitorData, recent_transactions: list):
        # 获得当前时间
        now = int(time.strftime("%H%M%S"))
        # 还在冷却时间中，返回
        if now - self.lastTriggered < self.coolDownTime * 100:
            return
        for condition in self.conditionItems:
            # 任何一个条件不满足则返回
            if not condition.match_condition(live_data, recent_transactions):
                return
        # 更新提示消息时间至当前
        self.lastTriggered = now
        # 发送弹出消息
        LiveTracker.liveTrackerInstance.add_message_log(live_data.code, self.get_message_string())

    # 从所有单条指标中获取消息文本
    def get_message_string(self):
        message = ""
        for condition in self.conditionItems:
            message += condition.message
        message += "!"
        return message

    # 更新修改过的指标内容
    def update_condition_items(self, table: QTableWidget):
        self.conditionItems = []
        for i in reversed(range(self.itemNode.childCount())):
            self.itemNode.removeChild(self.itemNode.child(i))
        for row in range(table.rowCount()):
            item_field = table.cellWidget(row, 0).currentText()
            item_value = table.item(row, 1).text()
            # 在树状图上添加一个子节点
            child_node = QTreeWidgetItem()
            self.itemNode.addChild(child_node)
            # 添加当前指标到列表中
            self.conditionItems.append(ConditionItem(child_node, row, item_field, item_value))


# 盯盘指标编辑器窗口
class MonitorConditionEditor(QDialog, Ui_MonitorCondition):

    def __init__(self, condition_group: ConditionItemGroup):
        super().__init__()
        self.setupUi(self)
        self.conditionGroup = condition_group
        # 从保存的盯盘指标中读取并初始化表格
        self.txtGroupName.setText(condition_group.name)
        row = 0
        for condition_item in condition_group.conditionItems:
            self.tblMonitorItems.insertRow(row)
            box = QComboBox()
            box.addItems(["日内涨跌幅", "短时涨跌幅", "短时成交额", "短时内外盘占比", "当前委比"])
            box.setCurrentText(condition_item.field)
            self.tblMonitorItems.setCellWidget(row, 0, box)
            self.tblMonitorItems.setItem(row, 1, QTableWidgetItem(str(condition_item.thresholdValue)))
            row += 1

    # 添加盯盘指标
    def add_condition_item(self):
        box = QComboBox()
        box.addItems(["日内涨跌幅", "短时涨跌幅", "短时成交额", "短时内外盘占比", "当前委比"])
        row_count = self.tblMonitorItems.rowCount()
        self.tblMonitorItems.insertRow(row_count)
        self.tblMonitorItems.setCellWidget(row_count, 0, box)
        self.tblMonitorItems.setItem(row_count, 1, QTableWidgetItem("0"))

    # 删除盯盘指标
    def delete_condition_item(self):
        selected_items = self.tblMonitorItems.selectedItems()
        # 如果没有选中的则默认删除最后一条
        if len(selected_items) == 0:
            row_count = self.tblMonitorItems.rowCount()
            # 确保列表中存在内容
            if row_count > 0:
                self.tblMonitorItems.removeRow(row_count)
        # 删除选中的行
        else:
            selection = selected_items[0]
            self.tblMonitorItems.removeRow(selection.row)

    # 保存并关闭窗口
    def save_changes(self):
        self.conditionGroup.update_condition_items(self.tblMonitorItems)
        self.conditionGroup.set_name(self.txtGroupName.text())
        self.conditionGroup.itemNode.setExpanded(True)
        self.close()

    # 放弃修改并关闭窗口
    def discard_changes(self):
        self.conditionGroup.itemNode.setExpanded(True)
        self.close()
