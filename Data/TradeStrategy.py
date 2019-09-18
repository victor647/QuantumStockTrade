import math


# 短线股价与均线的偏离指标
def short_term_index(stock_data):
    # 与五日均线的偏离
    bias_short = stock_data['close'] / stock_data['avg_price_five']
    # 与自定义长线均线的偏离
    bias_long = stock_data['close'] / stock_data['avg_price_long']
    return bias_short * bias_long


# 五日均线与长线均线之差除以当日收盘价的平方根，作为次日交易基础价格偏移
def long_term_bias(stock_data):
    price_difference = (stock_data['avg_price_five'] - stock_data['avg_price_long']) / stock_data['close']
    if price_difference == 0:
        return 0

    sign = -1 if price_difference < 0 else 1
    price_difference = abs(price_difference)
    return round(math.sqrt(price_difference) * sign, 2)


class TradeStrategy:
    # 买点跌幅
    buyPoint = -2
    # 卖点涨幅
    sellPoint = 2
    # 底仓股数
    baseShare = 2000
    # 每笔交易股数
    sharePerTrade = 1000
    # 满仓股数
    maxShare = 5000
    # 空仓股数
    minShare = 0
    # 做T单次利润
    sameDayProfit = 2
    # 允许做T
    allowSameDayTrade = True
    # 长线价格均线日数
    averagePricePeriod = 10
    # 成交量均线日数
    averageVolumePeriod = 5
    # 成交量乘数
    volumeWeight = 1.5

    def auto_get_strategy(self, analysis_data):
        # 根据平均最低价获取买点
        self.buyPoint = round(analysis_data.averageLowWhenDown, 1)
        # 根据平均最高价获取卖点
        self.sellPoint = round(analysis_data.averageHighWhenUp, 1)
        # 平均振幅超过2%的股票才适合做T
        if analysis_data.averageFullAmp > 2:
            self.allowSameDayTrade = True
            # 做T盈利预期为平均回撤/反弹幅度+0.5%
            self.sameDayProfit = max(1, round((analysis_data.averageFallback + analysis_data.averageBounce) / 2, 1)) + 0.5
        else:
            self.allowSameDayTrade = False




