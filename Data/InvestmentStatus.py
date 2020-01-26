import Tools.TradeSettings as TradeSettings


# 单次交易记录
class Transaction:

    def __init__(self, direction: str, price: float, share: int, date: str):
        self.__direction = direction
        self.price = round(price, 2)
        self.share = share
        self.__value = self.price * share
        self.fee = self.transaction_fee()
        self.date = date

    # 包含交易税费的买入本金
    def full_investment(self):
        return self.__value + self.fee

    # 扣除交易税费的卖出所得
    def full_return(self):
        return self.__value - self.fee

    # 交易税费成本
    def transaction_fee(self):
        # 买入只计算券商佣金
        if self.__direction == 'B':
            return self.broker_fee()
        # 卖出需要缴纳印花税
        else:
            printing_tax = round(self.__value * TradeSettings.stampDuty, 2)
            return self.broker_fee() + printing_tax

    # 券商佣金
    def broker_fee(self):
        return round(max(self.__value * TradeSettings.brokerFeePercentage, TradeSettings.minBrokerFee), 2)


# 某只股票所有交易记录
class StockInvestment:

    def __init__(self, stock_code: str):
        self.stockCode = stock_code
        self.currentShare = 0
        self.buyTransactions = []
        self.sellTransactions = []
        self.initialAsset = 0.0
        self.totalInvestment = 0.0
        self.totalReturn = 0.0
        self.totalFee = 0.0

    # 初始建仓
    def initial_invest(self):
        self.initialAsset = self.totalInvestment

    # 模拟买入股票
    def buy_stock(self, price: float, share: int, date: str):
        buy_transaction = Transaction('B', price, share, date)
        self.buyTransactions.append(buy_transaction)
        self.totalInvestment += buy_transaction.full_investment()
        self.totalFee += buy_transaction.fee
        self.currentShare += share

    # 模拟卖出股票
    def sell_stock(self, price: float, share: int, date: str):
        # 获得可卖出股票数量
        available_share = self.currentShare
        for t in reversed(self.buyTransactions):
            if t.date == date:
                available_share -= t.share
            else:
                break
        # 无可卖股份
        if available_share == 0:
            return False
        # 只可卖出部分
        if share > available_share:
            share = available_share

        sell_transaction = Transaction('S', price, share, date)
        self.sellTransactions.append(sell_transaction)
        self.totalReturn += sell_transaction.full_investment()
        self.totalFee += sell_transaction.fee
        self.currentShare -= share
        return True

    # 现金价值，未卖出则为负
    def cash_worth(self):
        return round(self.totalReturn - self.totalInvestment, 2)

    # 股票价值，卖出则为零
    def stock_worth(self, current_price: float):
        return round(self.currentShare * current_price, 2)

    # 累计利润：股票价值+现金价值
    def net_profit(self, current_price: float):
        return round(self.cash_worth() + self.stock_worth(current_price), 2)

    # 累计获利百分比
    def profit_percentage(self, current_price: float):
        if self.initialAsset == 0:
            return 0.00
        return round(self.net_profit(current_price) / self.initialAsset * 100, 2)

    # 总资产：累计利润+初始投入
    def net_worth(self, current_price: float):
        return round(self.net_profit(current_price) + self.initialAsset, 2)

    # 持仓平均成本
    def average_cost(self, current_price: float):
        if self.currentShare == 0:
            return 0.00
        return round(current_price - self.net_profit(current_price) / self.currentShare, 2)

