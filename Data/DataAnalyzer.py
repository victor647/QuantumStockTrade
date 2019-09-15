class AnalysisData:
    averageTurn = 0
    averageCloseUp = 1
    averageCloseDown = -1
    averageHigh = 2
    averageLow = -2
    averageHighWhenUp = 3
    averageLowWhenDown = -3
    averageFullAmp = 4
    averageFallback = 1
    averageBounce = 1


# 分析价格获得涨跌幅百分比数据
def analyze_database(database):
    database['open_pct'] = round((database['open'] / database['preclose'] - 1) * 100, 2)
    database['high_pct'] = round((database['high'] / database['preclose'] - 1) * 100, 2)
    database['low_pct'] = round((database['low'] / database['preclose'] - 1) * 100, 2)
    database['close_pct'] = round((database['close'] / database['preclose'] - 1) * 100, 2)
    database['amplitude'] = database['high_pct'] + abs(database['low_pct'])


# 上涨概率
def close_price_up(database):
    selected = database[database['close_pct'] > 0]
    return round(selected.shape[0] / database.shape[0] * 100, 2)


# 低开高走概率
def low_open_high_close(database):
    selected = database[(database['open_pct'] < 0) & (database['close_pct'] > database['open_pct'])]
    return round(selected.shape[0] / database.shape[0] * 100, 2)


# 低开低走概率
def low_open_low_close(database):
    selected = database[(database['close_pct'] < database['open_pct']) & (database['open_pct'] < 0)]
    return round(selected.shape[0] / database.shape[0] * 100, 2)


# 高开高走概率
def high_open_high_close(database):
    selected = database[(database['close_pct'] > database['open_pct']) & (database['open_pct'] > 0)]
    return round(selected.shape[0] / database.shape[0] * 100, 2)


# 高开低走概率
def high_open_low_close(database):
    selected = database[(database['open_pct'] > 0) & database['close_pct'] < (database['open_pct'])]
    return round(selected.shape[0] / database.shape[0] * 100, 2)


# 最高价涨停概率
def reach_max_limit(database):
    selected = database[database['high_pct'] > 9.8]
    return round(selected.shape[0] / database.shape[0] * 100, 2)


# 收盘价涨停概率
def stay_max_limit(database):
    selected = database[database['close_pct'] > 9.8]
    return round(selected.shape[0] / database.shape[0] * 100, 2)


# 最低价跌停概率
def reach_min_limit(database):
    selected = database[database['low_pct'] < -9.8]
    return round(selected.shape[0] / database.shape[0] * 100, 2)


# 收盘价跌停概率
def stay_min_limit(database):
    selected = database[database['close_pct'] < -9.8]
    return round(selected.shape[0] / database.shape[0] * 100, 2)


# 平均振幅
def average_amplitude(database):
    return round(database['amplitude'].mean(), 2)


# 平均最高价回撤幅度
def average_fallback(database):
    return round((database['high_pct'] - database['close_pct']).mean(), 2)


# 平均最低价反弹幅度
def average_bounce(database):
    return round((database['close_pct'] - database['low_pct']).mean(), 2)


# 整体平均最高价涨幅
def average_high(database):
    return round(database['high_pct'].mean(), 2)


# 上涨时平均最高价涨幅
def average_high_when_up(database):
    selected = database[database['close_pct'] > 0]
    return round(selected['high_pct'].mean(), 2)


# 下跌时平均最高价涨跌幅
def average_high_when_down(database):
    selected = database[database['close_pct'] < 0]
    return round(selected['high_pct'].mean(), 2)


# 整体平均最低价跌幅
def average_low(database):
    return round(database['low_pct'].mean(), 2)


# 下跌时平均最低价跌幅
def average_low_when_down(database):
    selected = database[database['close_pct'] < 0]
    return round(selected['low_pct'].mean(), 2)


# 上涨时平均最低价涨跌幅
def average_low_when_up(database):
    selected = database[database['close_pct'] > 0]
    return round(selected['low_pct'].mean(), 2)


# 上涨时平均收盘涨幅
def average_close_when_up(database):
    selected = database[database['close_pct'] > 0]
    return round(selected['close_pct'].mean(), 2)


# 下跌时平均收盘跌幅
def average_close_when_down(database):
    selected = database[database['close_pct'] < 0]
    return round(selected['close_pct'].mean(), 2)


# 平均换手率
def average_turn(database):
    return round(database['turn'].mean(), 2)


# 区间开盘价
def interval_open_price(database):
    return round(database.iloc[0]['open'], 2)


# 区间收盘价
def interval_close_price(database):
    return round(database.iloc[-1]['close'], 2)


# 区间最高价
def interval_highest_price(database):
    return round(database['high'].max(), 2)


# 区间最低价
def interval_lowest_price(database):
    return round(database['low'].min(), 2)


# 区间均价
def interval_average_price(database):
    return round(database['close'].mean(), 2)


# 区间总涨幅
def interval_total_performance(database):
    return round((interval_close_price(database) / interval_open_price(database) - 1) * 100, 2)


# 区间每日平均涨幅
def interval_average_performance(database):
    return round(interval_total_performance(database) / database.shape[0], 2)


# 跑赢大盘概率
def win_market(stock_database, market_database):
    count = 0
    for i, row in stock_database.iterrows():
        if row['close_pct'] > market_database.loc[i, 'close_pct']:
            count += 1
    return round(count / stock_database.shape[0] * 100, 2)


# 逆势上涨概率
def inverse_market_up(stock_database, market_database):
    count = 0
    for i, row in stock_database.iterrows():
        if row['close_pct'] > 0 > market_database.loc[i, 'close_pct']:
            count += 1
    return round(count / stock_database.shape[0] * 100, 2)


# 逆市下跌概率
def inverse_market_down(stock_database, market_database):
    count = 0
    for i, row in stock_database.iterrows():
        if row['close_pct'] < 0 < market_database.loc[i, 'close_pct']:
            count += 1
    return round(count / stock_database.shape[0] * 100, 2)


# 计算股票均线与平均换手率
def get_average_price(database, price_period, volume_period):
    rows = database.shape[0]
    for i in range(rows - 1, -1, -1):
        min_index = max(0, i - 5)
        database.loc[i, 'avg_price_five'] = round(database.loc[min_index:i, 'close'].mean(), 2)

        min_index = max(0, i - price_period)
        database.loc[i, 'avg_price_long'] = round(database.loc[min_index:i, 'close'].mean(), 2)

        min_index = max(0, i - volume_period)
        database.loc[i, 'avg_turn'] = round(database.loc[min_index:i, 'turn'].mean(), 2)


# 通过价格计算涨跌幅
def get_percentage_from_price(price, pre_close):
    return round((price / pre_close - 1) * 100, 2)


# 通过涨跌幅计算价格
def get_price_from_percentage(pre_close, percentage):
    return round(pre_close * (1 + percentage / 100), 2)
