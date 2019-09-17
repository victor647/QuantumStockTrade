import time


class RecentTradeHistory:
    time = 0
    price = 0
    volume = 0
    worth = 0
    direction = "B"
    totalTradeCount = 0


class RealTimeStockData:
    code = ""
    currentPrice = 0
    percentChange = 0
    previousClose = 0
    open = 0
    totalVolume = 0
    totalBuyVolume = 0
    totalSellVolume = 0
    buySellInfo = None
    recentTradeHistory = dict()

    # 读取股票最近几条交易记录数据
    def parse_recent_history(self, data):
        logs = data.split('|')
        for log in logs:
            log_split = log.split('/')
            history = RecentTradeHistory()
            trade_time = int(log_split[0].replace(':', ''))
            history.time = trade_time
            history.price = float(log_split[1])
            history.volume = int(log_split[2])
            history.direction = log_split[3]
            history.worth = int(log_split[4])
            history.totalTradeCount = int(log_split[5])
            self.recentTradeHistory[trade_time] = history
        self.delete_old_trade_history()

    def delete_old_trade_history(self):
        now = int(time.strftime("%H%M%S"))
        history = sorted(self.recentTradeHistory)
        for key in history:
            # 超过三分钟的交易记录
            if now - key > 300:
                del self.recentTradeHistory[key]
            else:
                return

    def get_most_recent_trade_logs(self, count):
        history = sorted(self.recentTradeHistory, reverse=True)
        for i in range(count):
            trade_time = history[i]
            print(str(self.recentTradeHistory[trade_time].price) + str(self.recentTradeHistory[trade_time].volume))


class BuySellInfo:
    buyPrice1 = 0
    buyVolume1 = 0
    buyPrice2 = 0
    buyVolume2 = 0
    buyPrice3 = 0
    buyVolume3 = 0
    buyPrice4 = 0
    buyVolume4 = 0
    buyPrice5 = 0
    buyVolume5 = 0
    sellPrice1 = 0
    sellVolume1 = 0
    sellPrice2 = 0
    sellVolume2 = 0
    sellPrice3 = 0
    sellVolume3 = 0
    sellPrice4 = 0
    sellVolume4 = 0
    sellPrice5 = 0
    sellVolume5 = 0
