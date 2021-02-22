import os, json, pandas, tushare
from pathlib import Path
from PyQt5.QtWidgets import QFileDialog, QTableWidget
import Data.TechnicalAnalysis as TechnicalAnalysis


# 选取自动选股结果输出文件夹
def select_folder():
    return str(QFileDialog.getExistingDirectory(directory=selected_stock_list_path()))


# 默认全部股票列表存放路径
def full_stock_info_path():
    base_path = os.path.join(os.path.curdir, 'StockData')
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    file_path = os.path.join(base_path, 'full_stock_info.csv')
    return file_path


# 选股器导出的股票列表文件夹
def selected_stock_list_path():
    return stock_data_path('SelectedStocks')


# 选股条件储存路径
def search_config_path():
    return stock_data_path('SearchConfigs')


# 交易策略储存路径
def trade_strategy_path():
    return stock_data_path('TradeStrategyConfigs')


# 定投组合储存路径
def investment_plan_path():
    return stock_data_path('InvestmentPlans')


# 股票数据文件夹下的子文件夹
def stock_data_path(folder: str):
    base_path = os.path.join(os.path.curdir, 'StockData', folder)
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    return base_path


# 默认股票历史数据存放路径
def stock_history_path(stock_code: str):
    base_path = os.path.join(os.path.curdir, 'StockData', 'StockHistory')
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    file_path = os.path.join(base_path, stock_code + '.csv')
    return file_path


# 盯盘指标存储文件夹
def monitor_config_path():
    base_path = os.path.join(os.path.curdir, 'StockData', 'MonitorConfigs')
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    return base_path


# 导出找到的股票列表到txt文件
def export_stock_list(stock_table: QTableWidget, date=''):
    file_path = QFileDialog.getSaveFileName(directory=selected_stock_list_path() + '/' + date, filter='TXT(*.txt)')
    if file_path[0] == '':
        return
    file = open(file_path[0], 'w')
    for i in range(stock_table.rowCount()):
        text = stock_table.item(i, 0).text()
        file.write(text + '\n')
    file.close()


# 导出自动选股找到的股票列表到txt文件
def export_auto_search_stock_list(stock_list: list, name: str, date: str):
    # 如果没有找到股票则跳过
    if len(stock_list) == 0:
        return
    # 通过条件组名称新建文件夹存放选股列表
    folder = os.path.join(selected_stock_list_path(), name)
    if not os.path.exists(folder):
        os.makedirs(folder)
    # 以日期为名称命名选股列表
    file_path = os.path.join(folder, date + '.txt')
    file = open(file_path, 'w')
    file.write(date + '\n')
    for stock in stock_list:
        file.write(stock + '\n')
    file.close()


# 导出定投股票列表到txt文件
def export_scheduled_investment_stocks(stock_table: QTableWidget):
    file_path = QFileDialog.getSaveFileName(directory=investment_plan_path(), filter='TXT(*.txt)')
    if file_path[0] == '':
        return
    file = open(file_path[0], 'w')
    for i in range(stock_table.rowCount()):
        code = stock_table.item(i, 0).text()
        share = stock_table.item(i, 2).text()
        file.write(code + '\t' + share + '\n')
    file.close()


# 从txt文件导入股票列表
def import_stock_list(import_func):
    file_path = QFileDialog.getOpenFileName(directory=selected_stock_list_path(), filter='TXT(*.txt)')
    if file_path[0] == '':
        return
    file = open(file_path[0], 'r')
    for line in file:
        code = line.rstrip('\n')
        import_func(code)
    file.close()


# 从txt文件导入股票列表并读取日期信息
def import_multiple_stock_lists():
    files = QFileDialog.getOpenFileNames(directory=selected_stock_list_path(), filter='TXT(*.txt)')
    full_data = {}
    for file_path in files[0]:
        file = open(file_path, 'r')
        lines = file.readlines()
        date = Path(file_path).stem
        codes = []
        for line in lines:
            codes.append(line.rstrip('\n'))
        full_data[date] = codes
        file.close()
    return full_data


# 从txt文件导入定投组合股票列表
def import_scheduled_investment_stock_list():
    file_path = QFileDialog.getOpenFileName(directory=investment_plan_path(), filter='TXT(*.txt)')
    if file_path[0] == '':
        return
    file = open(file_path[0], 'r')
    lines = file.readlines()
    data = []
    for line in lines:
        items = line.rstrip('\n').split('\t')
        code = items[0]
        # 格式错误，跳过
        if len(code) != 6:
            continue
        # 若没有持仓信息则默认为0
        share = items[1] if len(items) > 1 else '0'
        data.append((code, share))
    file.close()
    return data


# 导出全部股票信息列表
def save_stock_list_file():
    # stock_list = tushare.pro_api().stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    stock_list = tushare.get_stock_basics()
    stock_list.to_csv(full_stock_info_path())
    return stock_list


# 导入全部股票信息列表
def read_stock_list_file():
    return pandas.read_csv(full_stock_info_path())


# 导出盯盘指标
def export_monitor_conditions(groups: list):
    file_path = QFileDialog.getSaveFileName(directory=monitor_config_path(), filter='JSON(*.json)')
    if file_path[0] != '':
        export_config_as_json(groups, file_path[0])


# 导入盯盘指标
def import_monitor_conditions():
    file_path = QFileDialog.getOpenFileName(directory=monitor_config_path(), filter='JSON(*.json)')
    if file_path[0] != '':
        return import_json_config(file_path[0])
    return None


# 导出数据为json文件
def export_config_as_json(export_object, file_path: str):
    with open(file_path, 'w') as file:
        json.dump(obj=export_object, fp=file, default=lambda obj: obj.__dict__, indent=4)


# 导入json数据
def import_json_config(file_path: str, object_hook=None):
    with open(file_path, 'r') as file:
        if object_hook is None:
            data = json.load(fp=file)
        else:
            data = json.load(fp=file, object_hook=object_hook)
    return data


# 从csv文件读取单只股票历史数据
def read_stock_history_data(stock_code: str, set_date_index: bool):
    data = pandas.read_csv(stock_history_path(stock_code))
    # 以日期为键
    if set_date_index:
        data.set_index('date', inplace=True)
    return data


# 保存单只股票历史数据到csv文件
def save_stock_history_data(bs_result, stock_code: str):
    data = pandas.DataFrame(bs_result.data, columns=bs_result.fields, dtype=float)
    TechnicalAnalysis.get_technical_index(data)
    data.to_csv(stock_history_path(stock_code))


# 导入选股器找到的股票列表
def import_selected_stock_list():
    return QFileDialog.getOpenFileName(directory=selected_stock_list_path(), filter='TXT(*.txt)')



