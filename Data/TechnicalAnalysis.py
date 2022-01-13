import pandas, talib, math
import Tools.FileManager as FileManager


# 计算技术指标
def get_technical_index(stock_data: pandas.DataFrame):
    stock_closes = stock_data['close']
    # 将价格数据转换为涨跌幅数据
    get_percentage_data(stock_data)

    # 计算BOLL轨道，至少上市20天
    if stock_closes.shape[0] < 20:
        return
    upper, middle, lower = talib.BBANDS(stock_closes, 20, 2, 2)
    stock_data['boll_upper'] = upper
    stock_data['boll_middle'] = middle
    stock_data['boll_lower'] = lower

    # 计算MACD图形，至少上市34天
    if stock_closes.shape[0] < 34:
        return
    white, yellow, column = talib.MACD(stock_closes)
    column = column * 2
    stock_data['macd_white'] = white
    stock_data['macd_yellow'] = yellow
    stock_data['macd_column'] = column


# 分析价格获得涨跌幅百分比数据
def get_percentage_data(database: pandas.DataFrame):
    database['open_pct'] = get_percent_change_from_price(database['open'], database['preclose'])
    database['high_pct'] = get_percent_change_from_price(database['high'], database['preclose'])
    database['low_pct'] = get_percent_change_from_price(database['low'], database['preclose'])
    database['close_pct'] = get_percent_change_from_price(database['close'], database['preclose'])
    database['daily_pct'] = get_percent_change_from_price(database['close'], database['open'])
    database['amplitude'] = database['high_pct'] - database['low_pct']


# 计算BIAS折线，至少上市24天
def get_bias_index(stock_data: pandas.DataFrame):
    if stock_data['close'].shape[0] < 24:
        return
    ma_24 = talib.SMA(stock_data['close'], 24)
    stock_data['bias_24'] = (stock_data['close'] - ma_24) / ma_24 * 100


# 计算KDJ曲线，至少上市13天
def get_kdj_index(stock_data: pandas.DataFrame):
    if stock_data['close'].shape[0] < 13:
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


# 计算所有MA均线
def calculate_all_ma_curves(stock_data: pandas.DataFrame):
    calculate_ma_curve(stock_data, 5)
    calculate_ma_curve(stock_data, 10)
    calculate_ma_curve(stock_data, 20)
    calculate_ma_curve(stock_data, 30)
    calculate_ma_curve(stock_data, 60)


# 计算股池需要的MA均线
def calculate_pool_ma_curves(stock_data: pandas.DataFrame):
    calculate_ma_curve(stock_data, 5)
    calculate_ma_curve(stock_data, 20)
    calculate_ma_curve(stock_data, 60)
    calculate_ma_curve(stock_data, 120)
    calculate_ma_curve(stock_data, 250)


# 计算MA均线
def calculate_ma_curve(stock_data: pandas.DataFrame, period: int):
    # 数据数量不够，跳过
    if stock_data.shape[0] <= period:
        return ''
    key = 'ma_' + str(period)
    if key in stock_data:
        return ''
    stock_data[key] = talib.SMA(stock_data['close'], period)
    # 解决最前端数据不够的问题
    for i in range(period):
        if math.isnan(stock_data[key].iloc[i]):
            stock_data[key].iloc[i] = stock_data['close'].iloc[:i + 1].mean()
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
    return get_percent_change_from_price(interval_close_price(database), interval_open_price(database))


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
def get_percent_change_from_price(price: float, base_price: float):
    return round((price / base_price - 1) * 100, 2)


# 通过涨跌幅计算价格
def get_price_from_percent_change(base_price: float, percentage: float):
    return round(base_price * (1 + percentage / 100), 2)


# 通过盈利和本金计算收益率
def get_profit_percentage(profit: float, investment: float):
    return round(profit / investment * 100, 2)


# 计算是否符合均线图形
def match_ma(stock_data: pandas.DataFrame, days_ahead: int, period_short: int, period_long: int):
    key_short = calculate_ma_curve(stock_data, period_short)
    key_long = calculate_ma_curve(stock_data, period_long)
    if key_short == '' or key_long == '':
        return False

    # 获取短线和长线
    short = stock_data[key_short]
    long = stock_data[key_long]
    # 获取最近和几日前的均价
    ahead_short = short.iloc[-days_ahead]
    ahead_long = long.iloc[-days_ahead]
    newest_short = short.iloc[-1]
    newest_long = long.iloc[-1]
    return ahead_short < ahead_long and newest_short > newest_long


# 计算是否符合MACD图形
def match_macd(stock_data: pandas.DataFrame, days_ahead: int, behaviour: str):
    if 'macd_white' not in stock_data.columns:
        return False
    # 获取MACD指标的三条数据
    white = stock_data['macd_white']
    yellow = stock_data['macd_yellow']

    # 白线上穿黄线
    if behaviour == '金叉':
        return white.iloc[-days_ahead] < yellow.iloc[-days_ahead] and white.iloc[-1] > yellow.iloc[-1]
    # 白线下穿黄线
    elif behaviour == '死叉':
        return white.iloc[-days_ahead] > yellow.iloc[-days_ahead] and white.iloc[-1] < yellow.iloc[-1]
    else:
        column = stock_data['macd_column']
        if behaviour == '翻红':
            return column.iloc[-days_ahead] < 0 < column.iloc[-1]
        elif behaviour == '翻绿':
            return column.iloc[-days_ahead] > 0 > column.iloc[-1]
        elif behaviour == '绿柱缩短':
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
    if track == '上轨':
        line = upper
    elif track == '中轨':
        line = middle
    else:
        line = lower

    # 获取最近和几日前的价格以及轨道
    ahead_stock = stock_closes.iloc[-days_ahead]
    ahead_line = line.iloc[-days_ahead]
    newest_stock = stock_closes.iloc[-1]
    newest_line = line.iloc[-1]

    if behaviour == '上穿':
        return ahead_stock < ahead_line and newest_stock > newest_line
    elif behaviour == '下穿':
        return ahead_stock > ahead_line and newest_stock < newest_line
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
    if 'K' in line:
        value = line_k
    elif 'D' in line:
        value = line_d
    # 计算J值
    else:
        value = line_j

    if behaviour == '大于':
        return value.iloc[-1] > threshold
    else:
        return value.iloc[-1] < threshold


# 剪去股票在某个日期之前的K线数据
def get_stock_data_before_date(data: pandas.DataFrame, date: str, days=0):
    trimmed_data = data[:date]
    # 保留选定日数
    if days == 0:
        return trimmed_data
    else:
        return trimmed_data.tail(days)


# 剪去股票在某个日期之后的K线数据
def get_stock_data_after_date(data: pandas.DataFrame, date: str, days=0):
    # 选股日期发生了交易
    if date in data.index:
        trimmed_data = data[date:].iloc[1:]
    else:
        trimmed_data = data[date:]
    # 保留选定日数
    if days == 0:
        return trimmed_data
    else:
        return trimmed_data.head(days)


# 获取股票X日后的收盘涨跌幅
def get_stock_performance_after_days(data: pandas.DataFrame, pre_close: float, days: int, key: str):
    # 选股日期为今天，无效
    if data.empty:
        return 0
    if data.shape[0] >= days:
        end_price = data.iloc[days - 1][key]
    else:
        end_price = data.iloc[-1][key]
    return get_percent_change_from_price(end_price, pre_close)


# 计算某个日期后一段时间内的股价极值
def get_stock_extremes_in_day_range(data: pandas.DataFrame, pre_close: float, start_days: int, end_days: int, key: str):
    # 选股日期为今天，无效
    if data.empty:
        return 0
    if data.shape[0] >= end_days:
        end_price_set = data.iloc[start_days - 1:end_days][key]
    else:
        end_price_set = data.iloc[start_days - 1:][key]
    # 判定寻找最高价还是最低价
    if key == 'high':
        end_price = end_price_set.max()
    else:
        end_price = end_price_set.min()
    return get_percent_change_from_price(end_price, pre_close)


# 获取同期大盘表现
def market_performance_by_days(market_code: str, start_date: str, days: int):
    market_data = FileManager.read_stock_history_data(market_code, True)
    data_before = get_stock_data_before_date(market_data, start_date)
    data_after = get_stock_data_after_date(market_data, start_date)
    pre_close = round(data_before.iloc[-1]['close'], 2)
    return get_stock_performance_after_days(data_after, pre_close, days, 'close')


# 获得K线图形分类
def candlestick_shape(daily_data: pandas.DataFrame):
    needle_up = daily_data['high_pct'] - max(daily_data['open_pct'], daily_data['close_pct'])
    needle_down = min(daily_data['open_pct'], daily_data['close_pct']) - daily_data['low_pct']
    body_length = abs(daily_data['open_pct'] - daily_data['close_pct'])
    # 实体部分高度
    if body_length > 6:
        body_height = '大'
    elif 3 < body_length <= 6:
        body_height = '中'
    elif 0.5 < body_length <= 3:
        body_height = '小'
    else:
        body_height = '十字'
    # 上下影线情况
    if needle_up < 0.5 and needle_down < 0.5:
        needle_shape = '实体'
    elif needle_up < 0.5 <= needle_down:
        needle_shape = '光头'
    elif needle_up >= 0.5 > needle_down:
        needle_shape = '赤脚'
    elif needle_up - needle_down >= 1:
        needle_shape = '上影长'
    elif needle_down - needle_up >= 1:
        needle_shape = '下影长'
    else:
        needle_shape = '影等长'
    # 开盘价位
    if daily_data['open_pct'] < -2:
        open_position = '低开'
    elif daily_data['open_pct'] > 2:
        open_position = '高开'
    else:
        open_position = '平开'
    # 收盘表现
    if daily_data['close'] > daily_data['open']:
        candle_color = '阳线'
    elif daily_data['close'] < daily_data['open']:
        candle_color = '阴线'
    else:
        candle_color = '白线'

    return open_position + needle_shape + body_height + candle_color

# 特殊K线图形
def match_special_shape(stock_data: pandas.DataFrame, period: int, shape: str):
    if shape == '对数底':
        pass

