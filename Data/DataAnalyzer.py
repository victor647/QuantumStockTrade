import pandas
import talib
import math


class AnalysisData:
    # 平均换手率
    averageTurn = 0
    # 平均收盘涨幅
    averageCloseUp = 1
    # 平均收盘跌幅
    averageCloseDown = -1
    # 平均最高涨幅
    averageHigh = 2
    # 平均最低跌幅
    averageLow = -2
    # 上涨时平均最高涨幅
    averageHighWhenUp = 3
    # 下跌时平均最低跌幅
    averageLowWhenDown = -3
    # 平均振幅
    averageFullAmp = 4
    # 平均最高涨幅回撤
    averageFallback = 1
    # 平均最低跌幅反弹
    averageBounce = 1


# 分析价格获得涨跌幅百分比数据
def analyze_database(database: pandas.DataFrame):
    database['open_pct'] = round((database['open'] / database['preclose'] - 1) * 100, 2)
    database['high_pct'] = round((database['high'] / database['preclose'] - 1) * 100, 2)
    database['low_pct'] = round((database['low'] / database['preclose'] - 1) * 100, 2)
    database['close_pct'] = round((database['close'] / database['preclose'] - 1) * 100, 2)
    database['amplitude'] = database['high_pct'] + abs(database['low_pct'])


# 区间内每日上涨概率
def close_price_up(database: pandas.DataFrame):
    selected = database[database['close_pct'] > 0]
    return round(selected.shape[0] / database.shape[0] * 100, 2)


# 低开高走概率
def low_open_high_close(database: pandas.DataFrame):
    low_open = database[database['open_pct'] < 0]
    high_close = low_open[low_open['close_pct'] > low_open['open_pct']]
    return round(high_close.shape[0] / low_open.shape[0] * 100, 2)


# 低开低走概率
def low_open_low_close(database: pandas.DataFrame):
    low_open = database[database['open_pct'] < 0]
    low_close = low_open[low_open['close_pct'] < low_open['open_pct']]
    return round(low_close.shape[0] / low_open.shape[0] * 100, 2)


# 高开高走概率
def high_open_high_close(database: pandas.DataFrame):
    high_open = database[database['open_pct'] > 0]
    high_close = high_open[high_open['close_pct'] > high_open['open_pct']]
    return round(high_close.shape[0] / high_open.shape[0] * 100, 2)


# 高开低走概率
def high_open_low_close(database: pandas.DataFrame):
    high_open = database[database['open_pct'] > 0]
    low_close = high_open[high_open['close_pct'] < high_open['open_pct']]
    return round(low_close.shape[0] / high_open.shape[0] * 100, 2)


# 最高价涨停概率
def reach_max_limit(database: pandas.DataFrame):
    selected = database[database['high_pct'] > 9.8]
    return round(selected.shape[0] / database.shape[0] * 100, 2)


# 收盘价涨停概率
def stay_max_limit(database: pandas.DataFrame):
    selected = database[database['close_pct'] > 9.8]
    return round(selected.shape[0] / database.shape[0] * 100, 2)


# 最低价跌停概率
def reach_min_limit(database: pandas.DataFrame):
    selected = database[database['low_pct'] < -9.8]
    return round(selected.shape[0] / database.shape[0] * 100, 2)


# 收盘价跌停概率
def stay_min_limit(database: pandas.DataFrame):
    selected = database[database['close_pct'] < -9.8]
    return round(selected.shape[0] / database.shape[0] * 100, 2)


# 平均振幅
def average_amplitude(database: pandas.DataFrame):
    return round(database['amplitude'].mean(), 2)


# 平均最高价回撤幅度
def average_fallback(database: pandas.DataFrame):
    return round((database['high_pct'] - database['close_pct']).mean(), 2)


# 平均最低价反弹幅度
def average_bounce(database: pandas.DataFrame):
    return round((database['close_pct'] - database['low_pct']).mean(), 2)


# 整体平均最高价涨幅
def average_high(database: pandas.DataFrame):
    return round(database['high_pct'].mean(), 2)


# 上涨时平均最高价涨幅
def average_high_when_up(database: pandas.DataFrame):
    selected = database[database['close_pct'] > 0]
    return round(selected['high_pct'].mean(), 2)


# 下跌时平均最高价涨跌幅
def average_high_when_down(database: pandas.DataFrame):
    selected = database[database['close_pct'] < 0]
    return round(selected['high_pct'].mean(), 2)


# 整体平均最低价跌幅
def average_low(database: pandas.DataFrame):
    return round(database['low_pct'].mean(), 2)


# 下跌时平均最低价跌幅
def average_low_when_down(database: pandas.DataFrame):
    selected = database[database['close_pct'] < 0]
    return round(selected['low_pct'].mean(), 2)


# 上涨时平均最低价涨跌幅
def average_low_when_up(database: pandas.DataFrame):
    selected = database[database['close_pct'] > 0]
    return round(selected['low_pct'].mean(), 2)


# 上涨时平均收盘涨幅
def average_close_when_up(database: pandas.DataFrame):
    selected = database[database['close_pct'] > 0]
    return round(selected['close_pct'].mean(), 2)


# 下跌时平均收盘跌幅
def average_close_when_down(database: pandas.DataFrame):
    selected = database[database['close_pct'] < 0]
    return round(selected['close_pct'].mean(), 2)


# 平均换手率
def average_turn(database: pandas.DataFrame):
    return round(database['turn'].mean(), 2)


# 区间开盘价
def interval_open_price(database: pandas.DataFrame):
    return round(database.iloc[0]['open'], 2)


# 区间收盘价
def interval_close_price(database: pandas.DataFrame):
    return round(database.iloc[-1]['close'], 2)


# 区间最高价
def interval_highest_price(database: pandas.DataFrame):
    return round(database['high'].max(), 2)


# 区间最低价
def interval_lowest_price(database: pandas.DataFrame):
    return round(database['low'].min(), 2)


# 区间均价
def interval_average_price(database: pandas.DataFrame):
    return round(database['close'].mean(), 2)


# 区间总涨幅
def interval_total_performance(database: pandas.DataFrame):
    return round((interval_close_price(database) / interval_open_price(database) - 1) * 100, 2)


# 区间每日平均涨幅
def interval_average_performance(database: pandas.DataFrame):
    return round(interval_total_performance(database) / database.shape[0], 2)


# 跑赢大盘概率
def win_market(stock_database: pandas.DataFrame, market_database: pandas.DataFrame):
    count = 0
    for i, row in stock_database.iterrows():
        if row['close_pct'] > market_database.loc[i, 'close_pct']:
            count += 1
    return round(count / stock_database.shape[0] * 100, 2)


# 逆势上涨概率
def inverse_market_up(stock_database: pandas.DataFrame, market_database: pandas.DataFrame):
    count = 0
    for i, row in stock_database.iterrows():
        if row['close_pct'] > 0 > market_database.loc[i, 'close_pct']:
            count += 1
    return round(count / stock_database.shape[0] * 100, 2)


# 逆市下跌概率
def inverse_market_down(stock_database: pandas.DataFrame, market_database: pandas.DataFrame):
    count = 0
    for i, row in stock_database.iterrows():
        if row['close_pct'] < 0 < market_database.loc[i, 'close_pct']:
            count += 1
    return round(count / stock_database.shape[0] * 100, 2)


# 计算股票均线与平均换手率
def get_average_price(database: pandas.DataFrame, price_period: int, volume_period: int):
    rows = database.shape[0]
    for i in range(rows - 1, -1, -1):
        min_index = max(0, i - 5)
        database.loc[i, 'avg_price_five'] = round(database.loc[min_index:i, 'close'].mean(), 2)

        min_index = max(0, i - price_period)
        database.loc[i, 'avg_price_long'] = round(database.loc[min_index:i, 'close'].mean(), 2)

        min_index = max(0, i - volume_period)
        database.loc[i, 'avg_turn'] = round(database.loc[min_index:i, 'turn'].mean(), 2)


# 通过价格计算涨跌幅
def get_percentage_from_price(price: float, pre_close: float):
    return round((price / pre_close - 1) * 100, 2)


# 通过涨跌幅计算价格
def get_price_from_percentage(pre_close: float, percentage: float):
    return round(pre_close * (1 + percentage / 100), 2)


# 计算是否符合MACD图形
def match_macd(stock_closes: pandas.Series, days_ahead: int, position: str, behaviour: str):
    # 获取MACD指标的三条数据
    white, yellow, column = talib.MACD(stock_closes)
    # 上市一个月内新股数据太少跳过
    if math.isnan(white.iloc[-days_ahead]):
        return False

    if behaviour == "金叉":
        # 白线上穿黄线
        if white.iloc[-days_ahead] > yellow.iloc[-days_ahead] or white.iloc[-1] < yellow.iloc[-1]:
            return False
    elif behaviour == "死叉":
        # 白线下穿黄线
        if white.iloc[-days_ahead] < yellow.iloc[-days_ahead] or white.iloc[-1] > yellow.iloc[-1]:
            return False
    elif behaviour == "翻红":
        # 绿柱缩短变红
        if column.iloc[-days_ahead] > 0 or column.iloc[-1] < 0:
            return False
    elif behaviour == "翻绿":
        # 红柱缩短变绿
        if column.iloc[-days_ahead] < 0 or column.iloc[-1] > 0:
            return False

    # 交汇点与零轴相对位置
    if position == "零轴下方" and white.iloc[-1] > 0:
        return False
    if position == "零轴上方" and white.iloc[-1] < 0:
        return False
    return True


# 计算是否符合BOLL图形
def match_boll(stock_closes: pandas.Series, days_ahead: int, track: str, behaviour: str):
    # 获取布林线的三根轨道
    upper, middle, lower = talib.BBANDS(stock_closes)
    # 上市一个月内新股数据太少跳过
    if math.isnan(upper.iloc[-days_ahead]):
        return False

    # 获取对应轨道价格，默认为上轨
    threshold_price = upper
    if track == "中轨":
        threshold_price = middle
    if track == "下轨":
        threshold_price = lower

    if behaviour == "上穿":
        if stock_closes.iloc[-days_ahead] > threshold_price.iloc[-days_ahead] or stock_closes.iloc[-1] < threshold_price.iloc[-1]:
            return False
    elif behaviour == "下穿":
        if stock_closes.iloc[-days_ahead] < threshold_price.iloc[-days_ahead] or stock_closes.iloc[-1] > threshold_price.iloc[-1]:
            return False
    return True


# 计算是否符合EXPMA图形
def match_expma(stock_closes: pandas.Series, days_ahead: int, behaviour: str):
    return True


# 计算是否符合KDJ图形
def match_kdj(stock_closes: pandas.Series, days_ahead: int, line: str, behaviour: str, threshold: int):
    return True


# 计算是否符合TRIX图形
def match_trix(stock_closes: pandas.Series, days_ahead: int, behaviour: str):
    return True
