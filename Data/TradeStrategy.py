import math


class TradeStrategy:
    buyPoint = -2
    sellPoint = 2
    baseShare = 2000
    sharePerTrade = 1000
    maxShare = 5000
    minShare = 0
    sameDayProfit = 2
    allowSameDayTrade = True
    averagePricePeriod = 10
    averageVolumePeriod = 5
    volumeWeight = 1.5

    def auto_get_strategy(self, analysis_data):
        self.buyPoint = round(analysis_data.averageLowWhenDown, 1)
        self.sellPoint = round(analysis_data.averageHighWhenUp, 1)
        if analysis_data.averageFullAmp > 2:
            self.allowSameDayTrade = True
            self.sameDayProfit = max(1, round((analysis_data.averageFallback + analysis_data.averageBounce) / 2, 1)) + 0.5
        else:
            self.allowSameDayTrade = False

    @staticmethod
    def short_term_index(stock_data):
        bias_short = stock_data.close / stock_data.averagePriceFive
        bias_long = stock_data.close / stock_data.averagePriceLong
        return bias_short * bias_long

    # 五日均线与长线均线之差除以当日收盘价的平方根，作为次日交易基础价格偏移
    @staticmethod
    def long_term_bias(stock_data):
        price_difference = (stock_data.averagePriceFive - stock_data.averagePriceLong) / stock_data.close
        if price_difference == 0:
            return 0

        sign = -1 if price_difference < 0 else 1
        price_difference = abs(price_difference)
        return round(math.sqrt(price_difference) * sign, 2)


