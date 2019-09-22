import RealTimeMonitor.MonitorCondition as MonitorCondition
from PyQt5.QtWidgets import QTreeWidgetItem
import time


# 交易记录基本单位
class RecentTradeHistory:
    # 成交时间（int）
    time = 0
    # 成交均价
    price = 0
    # 成交量
    volume = 0
    # 成交额
    amount = 0
    # 买卖方向
    direction = "买入"


# 挂单信息
class BidInfo:

    def __init__(self, live_info_list):
        self.buyPrice = [0.0] * 5
        self.buyVolume = [0] * 5
        self.sellPrice = [0.0] * 5
        self.sellVolume = [0] * 5
        for i in range(5):
            self.buyPrice[i] = float(live_info_list[9 + i * 2])
            self.buyVolume[i] = int(live_info_list[10 + i * 2])
            self.sellPrice[i] = float(live_info_list[19 + i * 2])
            self.sellVolume[i] = int(live_info_list[20 + i * 2])

    # 计算委比数据
    def get_bid_ratio(self):
        total_buy = sum(self.buyVolume)
        total_sell = sum(self.sellVolume)
        return round((total_buy - total_sell) / (total_buy + total_sell) * 100, 2)


class StockMonitorData:
    # 股票代码
    code = ""
    # 当前价格
    currentPrice = 0.0
    # 昨日收盘价
    previousClose = 0.0
    # 涨跌幅
    percentChange = 0.0

    # 初始化新增盯盘指标根节点
    def __init__(self, item_node: QTreeWidgetItem):
        self.monitorCodeNode = item_node
        self.recentTransactions = dict()
        self.monitorConditionGroups = []
        self.bidInfo = None

    # 删除时一并删除盯盘指标根节点
    def __del__(self):
        del self.monitorCodeNode

    # 新增盯盘条件组
    def add_monitor_condition_group(self):
        count = len(self.monitorConditionGroups)
        new_item = QTreeWidgetItem(["指标组" + str(count + 1)])
        self.monitorCodeNode.addChild(new_item)
        self.monitorConditionGroups.append(MonitorCondition.ConditionItemGroup(new_item))

    # 删除盯盘条件组
    def remove_monitor_condition_group(self, selection: QTreeWidgetItem):
        index = self.monitorCodeNode.indexOfChild(selection)
        self.monitorCodeNode.removeChild(selection)
        self.monitorConditionGroups.pop(index)

    # 更新股票实时信息
    def update_stock_data(self, live_info: list):
        self.code = live_info[2]
        self.currentPrice = float(live_info[3])
        self.previousClose = float(live_info[4])
        self.percentChange = float(live_info[32])
        self.bidInfo = BidInfo(live_info)
        self.parse_recent_transactions(live_info[29])

    # 遍历每条监测条件
    def analyze_stock_data(self, recent_transactions: list):
        for condition_group in self.monitorConditionGroups:
            condition_group.check_condition_match(self, recent_transactions)

    # 读取股票最近几条交易记录数据
    def parse_recent_transactions(self, data: str):
        logs = data.split('|')
        for log in logs:
            log_split = log.split('/')
            trade_time = int(log_split[0].replace(':', ''))
            # 如果交易记录没有更新则跳过
            if trade_time in self.recentTransactions:
                return
            history = RecentTradeHistory()
            history.time = trade_time
            history.price = float(log_split[1])
            history.volume = int(log_split[2])
            history.direction = "买入" if log_split[3] == "B" else "卖出"
            history.amount = int(log_split[4])
            self.recentTransactions[trade_time] = history
        self.delete_obsolete_transactions()

    # 删除超过50条的交易数据
    def delete_obsolete_transactions(self):
        data_count = len(self.recentTransactions)
        # 不足50条则跳过
        if data_count <= 50:
            return
        # 按照从新到旧排序，删除最新50条以外的
        history = sorted(self.recentTransactions, reverse=True)
        for i in range(50, data_count):
            trade_time = history[i]
            del self.recentTransactions[trade_time]

    # 获得最新1条交易记录
    def fetch_newest_transaction(self):
        history = sorted(self.recentTransactions, reverse=True)
        trade_time = history[0]
        return self.recentTransactions[trade_time]

    # 获得最近N条交易记录
    def fetch_recent_transactions_by_count(self, count: int):
        history = sorted(self.recentTransactions, reverse=True)
        selected = []
        # 若交易记录数量不够，则选取全部
        if len(history) < count:
            count = len(history)
        for i in range(count):
            trade_time = history[i]
            selected.append(self.recentTransactions[trade_time])
        return selected

    # 获得最近N分钟的交易记录
    def fetch_recent_transactions_by_minute(self, minute: int):
        history = sorted(self.recentTransactions, reverse=True)
        selected = []
        now = int(time.strftime("%H%M%S"))
        for trade_time in history:
            if now - trade_time < minute * 60:
                selected.append(self.recentTransactions[trade_time])
            else:
                break
        # 若交易记录数量不够，则选取第一条
        if len(selected) == 0:
            return self.recentTransactions[history[0]]
        return selected


# 获取最近交易记录中的外盘比例
def get_active_buy_ratio(transactions: list):
    total_buy = 0
    total_sell = 0
    for transaction in transactions:
        # 主动买单则加入外盘
        if transaction.direction == "买入":
            total_buy += transaction.volume
        # 主动卖单则加入内盘
        else:
            total_sell += transaction.volume
    return round(total_buy / (total_buy + total_sell) * 100, 2)


# 获取最近交易记录的总成交额
def get_total_amount(transactions: list):
    total_amount = 0
    for transaction in transactions:
        total_amount += transaction.amount
    return round(total_amount / 10000, 2)


# 获取最近交易记录的涨跌幅
def get_recent_change(transactions: list):
    return transactions[0].price - transactions[-1].price
