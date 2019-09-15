from PyQt5.QtGui import QColor


# 根据股票代码获取股票交易所信息
def get_trade_center(stock_code):
    code = int(stock_code)
    market = ""
    # 深圳主板
    if 0 < code < 100000:
        market = "sz"
    # 创业板
    elif 300000 < code < 400000:
        market = "sz"
    # 上海主板
    elif 600000 < code < 700000:
        market = "sh"
    # 深圳可转债
    elif 128000 <= code <= 129000:
        market = "sz"
    # 上海可转债
    elif 113500 <= code <= 113600:
        market = "sh"
    return market


# 转换时间格式为可读
def reformat_time(time):
    if type(time) == str:
        return time
    time_string = str(time / 10000)
    if len(time_string) < 12:
        return time_string
    year = time_string[2:4]
    month = time_string[4:6]
    day = time_string[6:8]
    hour = time_string[8:10]
    minute = time_string[10:12]
    return year + "/" + month + "/" + day + " " + hour + ":" + minute


# 正数显示红色，负数显示绿色
def get_text_color(number):
    if number > 0:
        return QColor(200, 0, 0)
    if number < 0:
        return QColor(0, 128, 0)
    return QColor(0, 0, 0)


# 根据昨日收盘价判定股票价格显示颜色
def get_price_color(price, pre_close):
    if price > pre_close:
        return QColor(200, 0, 0)
    if price < pre_close:
        return QColor(0, 128, 0)
    return QColor(0, 0, 0)
