import time


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


# 读取股票最近几条交易记录数据
def parse_recent_transactions(data: str, recent_transactions: dict):
    logs = data.split('|')
    for log in logs:
        log_split = log.split('/')
        trade_time = int(log_split[0].replace(':', ''))
        if trade_time in recent_transactions:
            return
        history = RecentTradeHistory()
        history.time = trade_time
        history.price = float(log_split[1])
        history.volume = int(log_split[2])
        history.direction = "买入" if log_split[3] == "B" else "卖出"
        history.amount = int(log_split[4])
        recent_transactions[trade_time] = history
    delete_obsolete_transactions(recent_transactions)


# 删除超过50条的交易数据
def delete_obsolete_transactions(recent_transactions: dict):
    data_count = len(recent_transactions)
    # 不足50条则跳过
    if data_count <= 50:
        return
    # 按照从新到旧排序，删除最新50条以外的
    history = sorted(recent_transactions, reverse=True)
    for i in range(50, data_count):
        trade_time = history[i]
        del recent_transactions[trade_time]


# 获得最新1条交易记录
def fetch_newest_transaction(recent_transactions: dict):
    history = sorted(recent_transactions, reverse=True)
    trade_time = history[0]
    return recent_transactions[trade_time]


# 获得最近N条交易记录
def fetch_recent_transactions_by_count(recent_transactions: dict, count: int):
    history = sorted(recent_transactions, reverse=True)
    selected = []
    # 若交易记录数量不够，则选取全部
    if len(history) < count:
        count = len(history)
    for i in range(count):
        trade_time = history[i]
        selected.append(recent_transactions[trade_time])
    return selected


# 获得最近N分钟的交易记录
def fetch_recent_transactions_by_minute(recent_transactions: dict, minute: int):
    history = sorted(recent_transactions, reverse=True)
    selected = []
    now = int(time.strftime("%H%M%S"))
    for trade_time in history:
        if now - trade_time < minute * 60:
            selected.append(recent_transactions[trade_time])
        else:
            break
    # 若交易记录数量不够，则选取第一条
    if len(selected) == 0:
        return recent_transactions[history[0]]
    return selected


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


class StockLiveStatus:
    # 最新价格
    currentPrice = 0
    # 涨跌幅
    percentChange = 0
    # 昨日收盘价
    previousClose = 0
    # 今日开盘价
    open = 0

    def __init__(self, code, live_info_list):
        self.code = code
        self.currentPrice = float(live_info_list[3])
        self.previousClose = float(live_info_list[4])
        self.percentChange = float(live_info_list[32])
        self.bidInfo = BidInfo(live_info_list)


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
