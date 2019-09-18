import time


# 获取最近一分钟外盘比例
def get_active_buy_ratio(recent_transactions: dict):
    # 获取当前时间
    now = int(time.strftime("%H%M%S"))
    # 将交易记录字典降序排序
    history = sorted(recent_transactions, reverse=True)
    total_buy = 0
    total_sell = 0
    for key in history:
        if now - key < 60:
            # 主动买单则加入外盘
            if recent_transactions[key].direction == "B":
                total_buy += recent_transactions[key].volume
            # 主动卖单则加入内盘
            else:
                total_sell += recent_transactions[key].volume
        # 丢弃超过1分钟的数据
        else:
            break

    # 不在交易时间
    if total_buy + total_sell == 0:
        return 50
    return round(total_buy / (total_buy + total_sell) * 100, 2)


# 获取最近一分钟成交额
def get_one_minute_worth(recent_transactions: dict):
    # 获取当前时间
    now = int(time.strftime("%H%M%S"))
    # 将交易记录字典降序排序
    history = sorted(recent_transactions, reverse=True)
    total_worth = 0
    for key in history:
        if now - key < 60:
            total_worth += recent_transactions[key].worth
        # 丢弃超过1分钟的数据
        else:
            break
    return round(total_worth / 10000, 2)


# 获取最近一分钟涨跌
def get_one_minute_change(recent_transactions: dict):
    now = int(time.strftime("%H%M%S"))
    history = sorted(recent_transactions, reverse=True)
    now_price = recent_transactions[history[0]].price
    for key in history:
        if now - key >= 60:
            return now_price - recent_transactions[key].price
    return now_price - recent_transactions[history[-1]].price


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
        history.direction = log_split[3]
        history.worth = int(log_split[4])
        recent_transactions[trade_time] = history
    delete_obsolete_transactions(recent_transactions)


# 删除五分钟之前的交易数据
def delete_obsolete_transactions(recent_transactions: dict):
    now = int(time.strftime("%H%M%S"))
    # 收盘时间过后不再更新
    if now > 150000:
        return
    history = sorted(recent_transactions)
    for key in history:
        if now - key > 300:
            del recent_transactions[key]
        else:
            return


# 获得N条最新交易记录
def fetch_newest_transactions(recent_transactions, count: int):
    history = sorted(recent_transactions, reverse=True)
    for i in range(count):
        trade_time = history[i]
        print(str(recent_transactions[trade_time].price) + str(recent_transactions[trade_time].volume))


class RecentTradeHistory:
    # 成交时间（int）
    time = 0
    # 成交均价
    price = 0
    # 成交量
    volume = 0
    # 成交额
    worth = 0
    # 买卖方向
    direction = "B"


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
