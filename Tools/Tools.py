from PyQt5.QtGui import QColor
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QErrorMessage, QLineEdit, QTableWidget
from Tools import FileManager as FileManager
import Data.TechnicalAnalysis as TechnicalAnalysis
from Data.CustomSortingTableData import CustomSortingTableData
import webbrowser
from datetime import date


# 获取今天日期，格式‘20190101’
def get_today_date():
    today = date.today()
    return today.strftime('%Y%M%D')


# 获取离今天最近的交易日
def get_nearest_trade_date(qdate: QDate):
    while qdate.dayOfWeek() > 5:
        qdate = qdate.addDays(-1)
    return qdate


# 根据股票代码获取股票交易所信息和指数代码
def get_trade_center_and_index(stock_code: str):
    code = int(stock_code)
    # 深圳主板
    if 0 < code < 100000:
        market = 'sz'
        index = '399001'
    # 创业板
    elif 300000 < code < 400000:
        market = 'sz'
        index = '399006'
    # 上海主板以及科创板
    elif 600000 <= code < 700000:
        market = 'sh'
        index = '000001'
    # 深圳可转债
    elif 128000 <= code <= 129000:
        market = 'sz'
        index = '000000'
    # 上海可转债
    elif 113500 <= code <= 113600:
        market = 'sh'
        index = '000000'
    # 无效股票代码
    else:
        return '', ''
    return market, index


# 通过股票代码获取股票名称
def get_stock_name_from_code(stock_code: str):
    table = FileManager.read_stock_list_file()
    row = table[table['code'] == int(stock_code)]
    name = row.iloc[0]['name']
    return name


# 通过股票代码获取股票名称
def get_stock_code_from_name(stock_name: str):
    table = FileManager.read_stock_list_file()
    row = table[table['name'] == stock_name]
    # 如果搜不到股票名称
    if row.empty:
        return ''
    code = row.iloc[0]['code']
    # 将深圳代码添加0
    return str(code).zfill(6)


# 从文本输入框获取股票代码
def get_stock_code(input_field: QLineEdit):
    # 获取股票代码
    if input_field.text().isdigit():
        return input_field.text()
    else:
        return get_stock_code_from_name(input_field.text())


# 转换时间格式为可读
def reformat_time(time):
    if type(time) == str:
        return time
    time_string = str(time / 10000)
    if len(time_string) < 12:
        return time_string
    year = time_string[:4]
    month = time_string[4:6]
    day = time_string[6:8]
    hour = time_string[8:10]
    minute = time_string[10:12]
    return year + '-' + month + '-' + day + ' ' + hour + ':' + minute


# 六位数时间转字符串
def time_int_to_string(time: int):
    time_string = str(time)
    return time_string[:2] + ':' + time_string[2:4] + ':' + time_string[-2:]


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
def add_colored_item(table: QTableWidget, row: int, column: int, value: float, symbol='', threshold=0):
    item = CustomSortingTableData(str(value) + symbol)
    # 以数字作为隐藏排序值
    item.set_sorting_data(value)
    item.setForeground(get_text_color(value, threshold))
    table.setItem(row, column, item)
    return column + 1


# 添加可排序的数据
def add_sortable_item(table: QTableWidget, row: int, column: int, value: float, text=''):
    item = CustomSortingTableData(text if text != '' else str(value))
    item.set_sorting_data(value)
    table.setItem(row, column, item)
    return column + 1


# 添加价格数据
def add_price_item(table: QTableWidget, row: int, column: int, price: float, pre_close: float):
    item = CustomSortingTableData()
    item.setForeground(get_price_color(price, pre_close))
    percentage = TechnicalAnalysis.get_percentage_from_price(price, pre_close)
    # 显示全部数据
    item.setText(str(price) + ' ' + str(percentage) + '%')
    # 以百分比数据作为隐藏排序值
    item.set_sorting_data(percentage)
    table.setItem(row, column, item)
    return column + 1


# 在东方财富网站打开股票主页
def open_stock_page(code: str):
    market, index_code = get_trade_center_and_index(code)
    webbrowser.open('http://quote.eastmoney.com/' + market + code + '.html')


# 显示报错信息
def show_error_dialog(message: str):
    error_dialog = QErrorMessage()
    error_dialog.setWindowTitle('错误')
    error_dialog.showMessage(message)
    error_dialog.exec_()
