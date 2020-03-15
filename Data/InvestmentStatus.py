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

    def __init__(self):
        # 当前持仓
        self.currentShare = 0
        # 买入记录
        self.buyTransactions = []
        # 卖出记录
        self.sellTransactions = []
        # 首笔投资
        self.initialAsset = 0.0
        # 总买入花费
        self.totalInvestment = 0.0
        # 总卖出所得
        self.cashValue = 0.0
        # 总手续费
        self.totalFee = 0.0
        # 查询某个日期的持仓情况
        self.shareAtDate = {}

    # 初始建仓
    def initial_invest(self):
        self.initialAsset = self.totalInvestment

    # 模拟买入股票，按照股数
    def buy_stock(self, price: float, share: int, date: str):
        buy_transaction = Transaction('B', price, share, date)
        self.buyTransactions.append(buy_transaction)
        # 余额充足，使用余额购买
        if self.cashValue >= buy_transaction.full_investment():
            self.cashValue -= buy_transaction.full_investment()
        # 余额不足，追加投资
        else:
            self.totalInvestment += buy_transaction.full_investment() - self.cashValue
            self.cashValue = 0
        # 累计手续费
        self.totalFee += buy_transaction.fee
        # 增加持仓股数
        self.currentShare += share
        self.shareAtDate[date] = self.currentShare

    # 模拟买入股票，按照金额
    def buy_stock_by_money(self, price: float, money: int, date: str):
        # 计算买入股数，至少买入100股
        share = max(round(money / (price * 100)), 1) * 100
        self.buy_stock(price, share, date)
        return share

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
        # 增加账上现金价值
        self.cashValue += sell_transaction.full_return()
        # 累计手续费
        self.totalFee += sell_transaction.fee
        # 减少持仓股数
        self.currentShare -= share
        self.shareAtDate[date] = self.currentShare
        return True

    # 模拟卖出股票，按照金额
    def sell_stock_by_money(self, price: float, money: int, date: str):
        # 计算卖出股数，至少买入100股
        share = max(round(money / (price * 100)), 1) * 100
        self.sell_stock(price, share, date)
        return share

    # 清仓卖出可卖出部分
    def sell_all(self, price: float, date: str):
        self.sell_stock(price, self.currentShare, date)

    # 股票价值，持有股数*当前股价
    def stock_value(self, current_price: float):
        return round(self.currentShare * current_price, 2)

    # 累计利润：股票价值+现金价值
    def net_profit(self, current_price: float):
        return round(self.cashValue + self.stock_value(current_price) - self.totalInvestment, 2)

    # 总资产：累计利润+初始投入
    def net_worth(self, current_price: float):
        return round(self.stock_value(current_price) + self.cashValue, 2)

    # 持仓平均成本
    def average_cost(self, current_price: float):
        if self.currentShare == 0:
            return 0.00
        return round(self.stock_value(current_price) - self.net_profit(current_price) / self.currentShare, 2)

    # 盈亏一定数额时的价格
    def threshold_price(self, profit: float):
        return round((self.totalInvestment - self.cashValue + profit) / self.currentShare, 2)

    # 卖出全部后最终盈利
    def final_profit(self):
        return round(self.cashValue - self.totalInvestment, 2)

    # 获利百分比（按照当前价格计算）
    def profit_percentage(self, current_price: float):
        if self.stock_value(current_price) == 0:
            return 0.00
        return round(self.net_profit(current_price) / self.stock_value(current_price) * 100, 2)

    # 获利百分比（按照初始投入计算）
    def profit_percentage_from_init(self, current_price: float):
        if self.initialAsset == 0:
            return 0.00
        return round(self.net_profit(current_price) / self.initialAsset * 100, 2)

    # 获利百分比(按照最终价格计算）
    def final_profit_percentage(self):
        return round(self.final_profit() / self.totalInvestment * 100, 2)

