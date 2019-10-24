class TradeStrategy:
    # 买点跌幅
    buyPointBase = -2
    # 卖点涨幅
    sellPointBase = 2
    # 买点趋势偏移
    buyPointTrendBias = 1
    # 卖点趋势偏移
    sellPointTrendBias = 1
    # 每次买入间隔
    buyPointStep = 2
    # 每次卖出间隔
    sellPointStep = 2
    # 底仓股数
    initialShare = 2000
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
    # 多空信号出现时交易股数
    signalTradeShare = 1000
    # 趋势扭转时交易股数
    trendChangeTradeShare = 1000
    # BIAS指标阈值
    biasThreshold = 10

    def auto_get_strategy(self, analysis_data):
        # 根据平均最低价获取买点
        self.buyPointBase = round((analysis_data.averageLowWhenUp + analysis_data.averageLowWhenDown) / 2, 1)
        self.buyPointTrendBias = round((analysis_data.averageLowWhenUp - analysis_data.averageLowWhenDown) / 2, 1)
        # 根据平均最高价获取卖点
        self.sellPointBase = round((analysis_data.averageHighWhenUp + analysis_data.averageHighWhenDown) / 2, 1)
        self.sellPointTrendBias = round((analysis_data.averageHighWhenUp - analysis_data.averageHighWhenDown) / 2, 1)
        # 平均振幅超过2%的股票才适合做T
        if analysis_data.averageFullAmp > 2:
            self.allowSameDayTrade = True
            # 做T盈利预期为平均回撤/反弹幅度+0.5%
            self.sameDayProfit = max(1, round((analysis_data.averageFallback + analysis_data.averageBounce) / 2, 1)) + 0.5
        else:
            self.allowSameDayTrade = False




