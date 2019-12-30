import os, json, pandas, tushare, baostock
import Tools
from PyQt5.QtCore import QDate, QThread, pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QTableWidget
from Windows.ProgressBar import ProgressBar
import Data.TechnicalAnalysis as TechnicalAnalysis


# 选取自动选股结果输出文件夹
def select_folder():
    return str(QFileDialog.getExistingDirectory(directory=selected_stock_list_path()))


# 默认全部股票列表存放路径
def full_stock_info_path():
    base_path = os.path.join(os.path.curdir, "StockData")
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    file_path = os.path.join(base_path, "full_stock_info.csv")
    return file_path


# 选股器导出的股票列表文件夹
def selected_stock_list_path():
    base_path = os.path.join(os.path.curdir, "StockData", "SelectedStocks")
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    return base_path


# 选股条件储存路径
def search_config_path():
    base_path = os.path.join(os.path.curdir, "StockData", "SearchConfigs")
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    return base_path


# 默认股票历史数据存放路径
def stock_history_path(stock_code: str):
    base_path = os.path.join(os.path.curdir, "StockData", "StockHistory")
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    file_path = os.path.join(base_path, stock_code + ".csv")
    return file_path


# 盯盘指标存储文件夹
def monitor_config_path():
    base_path = os.path.join(os.path.curdir, "StockData", "MonitorConfigs")
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    return base_path


# 导出找到的股票列表到txt文件
def export_stock_list(stock_table: QTableWidget, date=""):
    file_path = QFileDialog.getSaveFileName(directory=selected_stock_list_path(), filter='TXT(*.txt)')
    if file_path[0] != "":
        file = open(file_path[0], "w")
        if date != "":
            file.write(date + "\n")
        for i in range(stock_table.rowCount()):
            text = stock_table.item(i, 0).text()
            file.write(text + "\n")
        file.close()


# 导出自动选股找到的股票列表到txt文件
def export_auto_search_stock_list(stock_list: list, directory: str, name: str, date: str, callback_func):
    file_path = os.path.join(directory, name + date + ".txt")
    file = open(file_path, "w")
    file.write(date + "\n")
    for stock in stock_list:
        file.write(stock + "\n")
    file.close()
    # 搜索结束后进入下一步
    callback_func()


# 从txt文件导入股票列表
def import_stock_list(import_func):
    file_path = QFileDialog.getOpenFileName(directory=selected_stock_list_path(), filter='TXT(*.txt)')
    if file_path[0] != "":
        file = open(file_path[0], "r")
        for line in file:
            code = line.rstrip('\n')
            import_func(code)
        file.close()


# 从txt文件导入股票列表并读取日期信息
def import_stock_list_with_date(import_func):
    file_path = QFileDialog.getOpenFileName(directory=selected_stock_list_path(), filter='TXT(*.txt)')
    date = QDate.currentDate().toString('yyyy-MM-dd')
    if file_path[0] != "":
        file = open(file_path[0], "r")
        lines = file.readlines()
        date = lines[0].rstrip('\n')
        for line in lines[1:]:
            code = line.rstrip('\n')
            import_func(code)
        file.close()
    return file_path[0], date


# 从txt文件导入股票列表并读取日期信息
def import_multiple_stock_lists():
    files = QFileDialog.getOpenFileNames(directory=selected_stock_list_path(), filter='TXT(*.txt)')
    full_data = {}
    for file_path in files[0]:
        file = open(file_path, "r")
        lines = file.readlines()
        date = lines[0].rstrip('\n')
        codes = []
        for line in lines[1:]:
            codes.append(line.rstrip('\n'))
        full_data[date] = codes
        file.close()
    return full_data




# 导出全部股票信息列表
def save_stock_list_file():
    stock_list = tushare.get_stock_basics()
    stock_list.to_csv(full_stock_info_path())
    return stock_list


# 导入全部股票信息列表
def read_stock_list_file():
    return pandas.read_csv(full_stock_info_path())


# 导出盯盘指标
def export_monitor_conditions(groups: list):
    file_path = QFileDialog.getSaveFileName(directory=monitor_config_path(), filter='JSON(*.json)')
    if file_path[0] != "":
        export_config_as_json(groups, file_path[0])


# 导入盯盘指标
def import_monitor_conditions():
    file_path = QFileDialog.getOpenFileName(directory=monitor_config_path(), filter='JSON(*.json)')
    if file_path[0] != "":
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


# 获取最新全部股票数据
def export_all_stock_data():
    stock_list = read_stock_list_file()
    exporter = StockDataExporter()
    progress = ProgressBar(stock_list.shape[0], "正在爬取股票历史数据", exporter)
    progress.show()
    exporter.progressBarCallback.connect(progress.update_search_progress)
    exporter.finishedCallback.connect(progress.finish_progress)
    exporter.start()
    progress.exec()


# 导入选股器找到的股票列表
def import_selected_stock_list():
    return QFileDialog.getOpenFileName(directory=selected_stock_list_path(), filter='TXT(*.txt)')


class StockDataExporter(QThread):
    progressBarCallback = pyqtSignal(int, str, str)
    finishedCallback = pyqtSignal()

    def __init__(self):
        super().__init__()
        now = QDate.currentDate()
        start_date = now.addYears(-1)
        self.today = now.toString('yyyy-MM-dd')
        self.startDate = start_date.toString('yyyy-MM-dd')
        self.stockList = read_stock_list_file()

    def run(self):
        for index, row in self.stockList.iterrows():
            code_num = row['code']
            # 将股票代码固定为6位数
            code = str(code_num).zfill(6)
            # 获得股票中文名称
            name = row['name']
            # 获取股票交易所
            market = Tools.get_trade_center(code)
            # 获取股票历史数据
            result = baostock.query_history_k_data_plus(code=market + "." + code, fields="date,open,high,low,close,preclose,turn,tradestatus,isST",
                                                        start_date=self.startDate, end_date=self.today, frequency="d", adjustflag="2")
            save_stock_history_data(result, code)
            self.progressBarCallback.emit(index + 1, code, name)
        self.finishedCallback.emit()
