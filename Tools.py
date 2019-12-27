from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTableWidgetItem, QErrorMessage
import FileManager as FileManager
import Data.TechnicalAnalysis as TechnicalAnalysis
import webbrowser
from datetime import date


# 获取今天日期，格式‘20190101’
def get_today_date():
    today = date.today()
    return today.strftime("%Y%M%D")


# 根据股票代码获取股票交易所信息
def get_trade_center(stock_code: str):
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
def get_stock_name(stock_code: str):
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


# 六位数时间转字符串
def time_int_to_string(time: int):
    time_string = str(time)
    return time_string[:2] + ":" + time_string[2:4] + ":" + time_string[-2:]


# 正数显示红色，负数显示绿色
def get_text_color(number, threshold=0):
    if number > threshold:
        return QColor(200, 0, 0)
    if number < threshold:
        return QColor(0, 128, 0)
    return QColor(0, 0, 0)


# 根据昨日收盘价判定股票价格显示颜色
def get_price_color(price: float, pre_close: float):
    if price > pre_close:
        return QColor(200, 0, 0)
    if price < pre_close:
        return QColor(0, 128, 0)
    return QColor(0, 0, 0)


# 添加带有红绿正负颜色的数据
def add_colored_item(table, value, row: int, column: int, symbol="", threshold=0):
    item = QTableWidgetItem(str(value) + symbol)
    item.setForeground(get_text_color(value, threshold))
    table.setItem(row, column, item)
    return column + 1


# 添加价格数据
def add_price_item(table, price: float, pre_close: float, row: int, column: int):
    item = QTableWidgetItem()
    item.setForeground(get_price_color(price, pre_close))
    percentage = TechnicalAnalysis.get_percentage_from_price(price, pre_close)
    item.setText(str(price) + " " + str(percentage) + "%")
    table.setItem(row, column, item)
    return column + 1


# 在东方财富网站打开股票主页
def open_stock_page(code: str):
    market = get_trade_center(code)
    webbrowser.open("http://quote.eastmoney.com/" + market + code + ".html")


# 显示报错信息
def show_error_dialog(message: str):
    error_dialog = QErrorMessage()
    error_dialog.setWindowTitle("错误")
    error_dialog.showMessage(message)
    error_dialog.exec_()
