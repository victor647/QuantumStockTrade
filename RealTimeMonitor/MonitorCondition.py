import time
import RealTimeMonitor.RealTimeStockData as RealTimeStockData
import RealTimeMonitor.LiveTracker as LiveTracker
from QtDesign.MonitorCondition_ui import Ui_MonitorCondition
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QDialog, QTreeWidgetItem, QTableWidget, QTableWidgetItem, QComboBox


def base_message():
    return "最近" + str(LiveTracker.liveTrackerInstance.spbRecentMeasureCount.value()) + LiveTracker.liveTrackerInstance.cbbRecentMeasurement.currentText()


# 单条监测指标
class ConditionItem:

    def __init__(self, field: str, threshold_value: str):
        self.field = field
        self.thresholdValue = float(threshold_value)

    # 从json导入数据
    @classmethod
    def from_json(cls, json_data: dict):
        field = json_data['field']
        value = json_data['thresholdValue']
        return cls(field, value)

    def match_condition(self, live_data: RealTimeStockData.StockMonitorData, recent_transactions: list):
        # 根据指标内容判断
        if self.field == "短时成交额":
            value = RealTimeStockData.get_total_amount(recent_transactions)
            if value > self.thresholdValue:
                return base_message() + "成交额达到" + str(value) + "万元"
        elif self.field == "短时涨跌幅":
            value = RealTimeStockData.get_recent_change(recent_transactions)
            if value > self.thresholdValue:
                return base_message() + "涨幅达到" + str(value) + "%"
            elif value < self.thresholdValue * -1:
                return base_message() + "跌幅达到" + str(value) + "%"
        elif self.field == "日内涨跌幅":
            value = live_data.percentChange
            if value > self.thresholdValue:
                return "日内涨幅达到" + str(value) + "%"
            elif value < self.thresholdValue * -1:
                return "日内跌幅达到" + str(value) + "%"
        elif self.field == "短时内外盘占比":
            value = RealTimeStockData.get_active_buy_ratio(recent_transactions)
            if value > self.thresholdValue:
                return base_message() + "外盘占比达到" + str(value) + "%"
            elif value < 100 - self.thresholdValue:
                return base_message() + "内盘占比达到" + str(value) + "%"
        elif self.field == "当前委比":
            value = live_data.bidInfo.get_bid_ratio()
            if value > self.thresholdValue:
                return "当前委比超过" + str(value) + "%"
            elif value < self.thresholdValue * -1:
                return "当前委比低于" + str(value) + "%"
        return ""


# 单个监测条件的所有监测指标
class ConditionItemGroup:
    # 上次触发的时间
    __lastTriggered = 0
    conditionGroupNode = None

    def __init__(self, name: str, cool_down: int, items: list):
        self.name = name
        self.coolDownTime = cool_down
        self.conditionItems = items

    # 从json导入
    @classmethod
    def deserialize_from_json(cls, json_data: dict):
        name = json_data['name']
        cool_down = json_data['coolDownTime']
        condition_items = list(map(ConditionItem.from_json, json_data['conditionItems']))
        return cls(name, cool_down, condition_items)

    # 生成一个默认指标
    def add_default_condition(self):
        condition_item = ConditionItem("日内涨跌幅", "3")
        self.create_individual_item_node(condition_item, 0)
        self.conditionItems.append(condition_item)

    # 创建新的子节点
    def create_individual_item_node(self, item: ConditionItem, index: int):
        item_node = QTreeWidgetItem()
        item_node.setText(0, "指标" + str(index + 1))
        item_node.setText(1, item.field)
        item_node.setText(2, str(item.thresholdValue))
        self.conditionGroupNode.addChild(item_node)

    # 设置指标组名称
    def set_name_and_cool_down(self, name: str, cool_down: int):
        self.conditionGroupNode.setText(0, name)
        self.name = name
        self.conditionGroupNode.setText(3, str(cool_down))
        self.coolDownTime = cool_down

    def check_condition_match(self, live_data: RealTimeStockData.StockMonitorData, recent_transactions: list):
        # 获得当前时间
        now = int(time.strftime("%H%M%S"))
        # 还在冷却时间中，返回
        if now - self.__lastTriggered < self.coolDownTime * 100:
            return
        output_message = ""
        for condition in self.conditionItems:
            message = condition.match_condition(live_data, recent_transactions)
            # 任何一个条件不满足则返回
            if message == "":
                return
            # 返回消息不为空，添加至输出消息
            output_message += message
        # 更新提示消息时间至当前
        self.__lastTriggered = now
        # 发送弹出消息
        LiveTracker.liveTrackerInstance.add_message_log(live_data.code, output_message + "!")

    # 更新修改过的指标内容
    def update_condition_items(self, table: QTableWidget):
        self.conditionItems = []
        for i in reversed(range(self.conditionGroupNode.childCount())):
            self.conditionGroupNode.removeChild(self.conditionGroupNode.child(i))
        for row in range(table.rowCount()):
            item_field = table.cellWidget(row, 0).currentText()
            item_value = table.item(row, 1).text()
            # 根据表格内容生成指标
            condition_item = ConditionItem(item_field, item_value)
            # 创建子节点
            self.create_individual_item_node(condition_item, row)
            # 添加当前指标到列表中
            self.conditionItems.append(condition_item)
        # 展开节点显示
        self.conditionGroupNode.setExpanded(True)


# 盯盘指标编辑器窗口
class MonitorConditionEditor(QDialog, Ui_MonitorCondition):

    def __init__(self, condition_group: ConditionItemGroup):
        super().__init__()
        self.setupUi(self)
        self.__conditionGroup = condition_group
        # 获取指标组合名称
        self.txtGroupName.setText(condition_group.name)
        # 获取冷却时间
        self.spbCoolDownTime.setValue(condition_group.coolDownTime)
        # 从保存的盯盘指标中读取并初始化表格
        row = 0
        for condition_item in condition_group.conditionItems:
            self.tblMonitorItems.insertRow(row)
            box = QComboBox()
            box.addItems(["日内涨跌幅", "短时涨跌幅", "短时成交额", "短时内外盘占比", "当前委比"])
            box.setCurrentText(condition_item.field)
            self.tblMonitorItems.setCellWidget(row, 0, box)
            self.tblMonitorItems.setItem(row, 1, QTableWidgetItem(str(condition_item.thresholdValue)))
            row += 1

    # 快捷键设置
    def keyPressEvent(self, key: QKeyEvent):
        # 回车键保存
        if key.key() == Qt.Key_Enter:
            self.save_changes()

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
            self.tblMonitorItems.removeRow(selection.row())

    # 保存并关闭窗口
    def save_changes(self):
        self.__conditionGroup.update_condition_items(self.tblMonitorItems)
        self.__conditionGroup.set_name_and_cool_down(self.txtGroupName.text(), self.spbCoolDownTime.value())
        self.close()

    # 放弃修改并关闭窗口
    def discard_changes(self):
        self.close()
