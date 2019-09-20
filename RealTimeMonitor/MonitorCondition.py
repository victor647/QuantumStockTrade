import time
import RealTimeMonitor.RealTimeStockData as RealTimeStockData
import RealTimeMonitor.LiveTracker as LiveTracker


def base_message():
    return "最近" + LiveTracker.liveTrackerInstance.spbRecentMeasureCount + LiveTracker.liveTrackerInstance.cbbRecentMeasurement.currentText()


# 单条监测指标
class ConditionItem:
    field = ""
    threshold_value = 0
    message = ""

    def match_condition(self, live_data: RealTimeStockData.StockLiveStatus, transaction_list: list):
        # 根据指标内容判断
        if self.field == "成交额":
            value = RealTimeStockData.get_total_amount(transaction_list)
            if value > self.threshold_value:
                self.message = base_message() + "成交额达到" + str(value) + "万元"
                return True
        elif self.field == "短时涨跌幅":
            value = RealTimeStockData.get_recent_change(transaction_list)
            if value > self.threshold_value:
                self.message = base_message() + "涨幅达到" + str(value) + "%"
                return True
            elif value < self.threshold_value * -1:
                self.message = base_message() + "跌幅达到" + str(value) + "%"
                return True
        elif self.field == "日内涨跌幅":
            value = live_data.percentChange
            if value > self.threshold_value:
                self.message = "日内涨幅达到" + str(value) + "%"
                return True
            elif value < self.threshold_value * -1:
                self.message = "日内跌幅达到" + str(value) + "%"
                return True
        elif self.field == "内外盘占比":
            value = RealTimeStockData.get_active_buy_ratio(transaction_list)
            if value > self.threshold_value:
                self.message = base_message() + "外盘占比达到" + str(value) + "%"
                return True
            elif value < 100 - self.threshold_value:
                self.message = base_message() + "内盘占比达到" + str(value) + "%"
                return True
        elif self.field == "委比":
            value = live_data.bidInfo.get_bid_ratio()
            if value > self.threshold_value:
                self.message = "当前委比超过" + str(value) + "%"
                return True
            elif value < self.threshold_value * -1:
                self.message = "当前委比低于" + str(value) + "%"
                return True
        return False


# 单个监测条件的所有监测指标
class MatchCondition:
    conditionItems = []
    lastTriggered = 0
    coolDownTime = 10

    def check_condition_match(self, live_data: RealTimeStockData.StockLiveStatus, transaction_list: list):
        # 获得当前时间
        now = int(time.strftime("%H%M%S"))
        # 还在冷却时间中，返回
        if now - self.lastTriggered < self.coolDownTime * 100:
            return
        for condition in self.conditionItems:
            # 任何一个条件不满足则返回
            if not condition.match_condition(live_data, transaction_list):
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


# 一只股票的全部监测条件
class StockMonitorData:

    def __init__(self, code):
        self.code = code
        self.matchConditions = []

    # 遍历每条监测条件
    def analyze_stock_data(self, live_data: RealTimeStockData.StockLiveStatus, transaction_list: list):
        for condition in self.matchConditions:
            condition.check_condition_match(live_data, transaction_list)




