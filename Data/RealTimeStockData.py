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
    recentTradeHistory = []


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


class RecentTradeHistory:
    time = ""
    price = 0
    volume = 0
    worth = 0
    direction = "B"
    totalTradeCount = 0
