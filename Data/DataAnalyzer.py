import pandas, talib, math


class AnalysisData:
    # 平均换手率
    averageTurn = 0
    # 平均收盘涨幅
    averageCloseUp = 1
    # 平均收盘跌幅
    averageCloseDown = -1
    # 上涨时平均最高涨幅
    averageHighWhenUp = 3
    # 下跌时平均最高涨幅
    averageHighWhenDown = 1
    # 下跌时平均最低跌幅
    averageLowWhenDown = -3
    # 上涨时平均最低跌幅
    averageLowWhenUp = -1
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


# 计算技术指标
def get_technical_index(stock_data: pandas.DataFrame):
    stock_closes = stock_data['close']

    # 计算KDJ曲线，至少上市13天
    if stock_closes.shape[0] < 13:
        return
    low_list = stock_data['low'].rolling(window=9).min()
    high_list = stock_data['high'].rolling(window=9).max()
    # talib中KD的均线算法和通达信算法不同，手写覆盖
    rsv = (stock_data['close'] - low_list) / (high_list - low_list) * 100
    k = SMA(rsv, 3, 1)
    d = SMA(k, 3, 1)
    j = k * 3 - d * 2
    stock_data['kdj_k'] = k
    stock_data['kdj_d'] = d
    stock_data['kdj_j'] = j

    # 计算BOLL轨道，至少上市20天
    if stock_closes.shape[0] < 20:
        return
    upper, middle, lower = talib.BBANDS(stock_closes, 20, 2, 2)
    stock_data['boll_upper'] = upper
    stock_data['boll_middle'] = middle
    stock_data['boll_lower'] = lower

    # 计算BIAS折线，至少上市24天
    if stock_closes.shape[0] < 24:
        return
    ma_24 = talib.MA(stock_closes, 24)
    stock_data['bias_24'] = (stock_closes - ma_24) / ma_24 * 100

    # 计算MACD图形，至少上市34天
    if stock_closes.shape[0] < 34:
        return
    white, yellow, column = talib.MACD(stock_closes)
    column = column * 2
    stock_data['macd_white'] = white
    stock_data['macd_yellow'] = yellow
    stock_data['macd_column'] = column

    # 计算TRIX曲线，至少上市43天
    if stock_closes.shape[0] < 43:
        return
    white = talib.TRIX(stock_closes, 12)
    yellow = talib.MA(white, 9)
    stock_data['trix_white'] = white
    stock_data['trix_yellow'] = yellow

    # 计算EXPMA曲线，至少上市99天
    if stock_closes.shape[0] < 99:
        return
    stock_data['expma_white'] = talib.EMA(stock_closes, 12)
    stock_data['expma_yellow'] = talib.EMA(stock_closes, 50)


# 计算MA均线
def calculate_ma_curve(stock_data: pandas.DataFrame, period: int):
    key = 'ma_' + str(period)
    stock_data[key] = talib.MA(stock_data['close'], period)
    return key


# 计算通达信版SMA值
def SMA(data: pandas.Series, period: int, weight: int):
    sma = [math.nan]
    for index in range(1, data.shape[0]):
        last_sma = sma[index - 1]
        if math.isnan(last_sma):
            sma.append((data.iloc[index] * weight) / period)
        else:
            sma.append((data.iloc[index] * weight + last_sma * (period - weight)) / period)
    return pandas.Series(sma)


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


# 通过价格计算涨跌幅
def get_percentage_from_price(price: float, pre_close: float):
    return round((price / pre_close - 1) * 100, 2)


# 通过涨跌幅计算价格
def get_price_from_percentage(pre_close: float, percentage: float):
    return round(pre_close * (1 + percentage / 100), 2)


# 计算是否符合MACD图形
def match_macd(stock_data: pandas.DataFrame, days_ahead: int, behaviour: str):
    if 'macd_white' not in stock_data.columns:
        return False
    # 获取MACD指标的三条数据
    white = stock_data['macd_white']
    yellow = stock_data['macd_yellow']

    # 白线上穿黄线
    if behaviour == "金叉":
        return white.iloc[-days_ahead] < yellow.iloc[-days_ahead] and white.iloc[-1] > yellow.iloc[-1]
    # 白线下穿黄线
    elif behaviour == "死叉":
        return white.iloc[-days_ahead] > yellow.iloc[-days_ahead] and white.iloc[-1] < yellow.iloc[-1]
    else:
        column = stock_data['macd_column']
        if behaviour == "翻红":
            return column.iloc[-days_ahead] < 0 < column.iloc[-1]
        elif behaviour == "翻绿":
            return column.iloc[-days_ahead] > 0 > column.iloc[-1]
        elif behaviour == "绿柱缩短":
            return column.iloc[-days_ahead] < column.iloc[-1] < 0
        else:
            return column.iloc[-days_ahead] > column.iloc[-1] > 0


# 计算是否符合BOLL图形
def match_boll(stock_data: pandas.DataFrame, days_ahead: int, track: str, behaviour: str):
    if 'boll_upper' not in stock_data.columns:
        return False
    # 获取布林线的三根轨道
    upper = stock_data['boll_upper']
    middle = stock_data['boll_middle']
    lower = stock_data['boll_lower']
    stock_closes = stock_data['close']

    # 获取对应轨道价格
    if track == "上轨":
        line = upper
    elif track == "中轨":
        line = middle
    else:
        line = lower

    # 获取最近和几日前的价格以及轨道
    ahead_stock = stock_closes.iloc[-days_ahead]
    ahead_line = line.iloc[-days_ahead]
    newest_stock = stock_closes.iloc[-1]
    newest_line = line.iloc[-1]

    if behaviour == "上穿":
        return ahead_stock < ahead_line and newest_stock > newest_line
    elif behaviour == "下穿":
        return ahead_stock > ahead_line and newest_stock < newest_line
    return False


# 计算是否符合EXPMA图形
def match_expma(stock_data: pandas.DataFrame, days_ahead: int, behaviour: str):
    if 'expma_white' not in stock_data.columns:
        return False
    # 获得长短两条EMA均线
    white = stock_data['expma_white']
    yellow = stock_data['expma_yellow']
    stock_closes = stock_data['close']

    # 白线在上为多头排列，否则为空头排列
    if "多头" in behaviour and white.iloc[-1] < yellow.iloc[-1]:
        return False
    elif "空头" in behaviour and white.iloc[-1] > yellow.iloc[-1]:
        return False

    # 获取被比较的两个价格
    first = stock_closes if "穿" in behaviour else white
    second = white if "白线" in behaviour else yellow

    # 获取最近和几日前的价格
    ahead_first = first.iloc[-days_ahead]
    ahead_second = second.iloc[-days_ahead]
    newest_first = first.iloc[-1]
    newest_second = second.iloc[-1]

    if "下" or "金叉" in behaviour:
        return ahead_first > ahead_second and newest_first < newest_second
    if "上" or "死叉" in behaviour:
        return ahead_first < ahead_second and newest_first > newest_second
    return False


# 计算是否符合KDJ图形
def match_kdj(stock_data: pandas.DataFrame, line: str, behaviour: str, threshold: int):
    if 'kdj_k' not in stock_data.columns:
        return False
    # 获取三条线的值
    line_k = stock_data['kdj_k']
    line_d = stock_data['kdj_d']
    line_j = stock_data['kdj_j']

    # 获取用户需要的值
    if "K" in line:
        value = line_k
    elif "D" in line:
        value = line_d
    # 计算J值
    else:
        value = line_j

    if behaviour == "大于":
        return value.iloc[-1] > threshold
    else:
        return value.iloc[-1] < threshold


# 计算是否符合TRIX图形
def match_trix(stock_data: pandas.DataFrame, days_ahead: int, behaviour: str):
    if 'trix_white' not in stock_data.columns:
        return False
    # 获取白线和黄线
    white = stock_data['trix_white']
    yellow = stock_data['trix_yellow']
    # 获取最近和几日前的价格
    ahead_white = white.iloc[-days_ahead]
    ahead_yellow = yellow.iloc[-days_ahead]
    newest_white = white.iloc[-1]
    newest_yellow = yellow.iloc[-1]

    if behaviour == "金叉":
        return ahead_white < ahead_yellow and newest_white > newest_yellow
    else:
        return ahead_white > ahead_yellow and newest_white < newest_yellow
