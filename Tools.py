from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTableWidgetItem
import Data.FileManager as FileManager
import Data.DataAnalyzer as DataAnalyzer


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
    elif 600000 <= code < 700000:
        market = "sh"
    # 深圳可转债
    elif 128000 <= code <= 129000:
        market = "sz"
    # 上海可转债
    elif 113500 <= code <= 113600:
        market = "sh"
    return market


# 通过股票代码获取股票名称
def get_stock_name(stock_code):
    table = FileManager.read_stock_list_file()
    row = table[table['code'] == int(stock_code)]
    name = row.iloc[0]['name']
    return name


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


# 添加带有红绿正负颜色的数据
def add_colored_item(table, text, row_count, column, symbol=""):
    item = QTableWidgetItem(str(text) + symbol)
    item.setForeground(get_text_color(text))
    table.setItem(row_count, column, item)


# 添加价格数据
def add_price_item(table, price, pre_close, row_count, column):
    item = QTableWidgetItem()
    item.setForeground(get_price_color(price, pre_close))
    item.setText(str(price) + " " + str(DataAnalyzer.get_percentage_from_price(price, pre_close)) + "%")
    table.setItem(row_count, column, item)
