import os
import pandas
import tushare
import baostock
import Tools
from PyQt5.QtCore import QDate, QThread, pyqtSignal
from PyQt5.QtWidgets import QFileDialog
from Windows.ProgressBar import ProgressBar
import json
import Windows.SearchCriteria as SearchCriteria


# 默认全部股票列表存放路径
def full_stock_info_path():
    return os.path.join(os.path.pardir, "StockData", "full_stock_info.csv")


# 选股器导出的股票列表文件夹
def selected_stock_list_path():
    return os.path.join(os.path.pardir, "StockData", "SelectedStocks")


# 导入全部股票信息列表
def read_stock_list_file():
    return pandas.read_csv(full_stock_info_path())


# 导出全部股票信息列表
def save_stock_list_file():
    stock_list = tushare.get_stock_basics()
    stock_list.to_csv(full_stock_info_path())
    return stock_list


# 导出数据为json文件
def export_config_as_json(criteria_list: list, file_path: str):
    with open(file_path, 'w') as file:
        json.dump(obj=criteria_list, fp=file, default=lambda obj: obj.__dict__, indent=4)


# 导入选股器搜索条件
def import_search_config(file_path: str):
    with open(file_path, 'r') as file:
        criteria_list = json.load(fp=file, object_hook=SearchCriteria.import_criteria_item)
    return criteria_list


# 默认股票历史数据存放路径
def stock_history_path(stock_code: str):
    base_path = os.path.join(os.path.pardir, "StockData\\StockHistory")
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    file_path = os.path.join(base_path, stock_code + ".csv")
    return file_path


# 从csv文件读取单只股票历史数据
def read_stock_history_data(stock_code: str):
    return pandas.read_csv(stock_history_path(stock_code))


# 保存单只股票历史数据到csv文件
def save_stock_history_data(bs_result, stock_code: str):
    data = pandas.DataFrame(bs_result.data, columns=bs_result.fields, dtype=float)
    data.to_csv(stock_history_path(stock_code))


# 获取最新全部股票数据
def export_all_stock_data():
    stock_list = save_stock_list_file()
    progress = ProgressBar(stock_list.shape[0])
    progress.show()
    exporter = StockDataExporter()
    exporter.progressBarCallback.connect(progress.update_search_progress)
    exporter.finishedCallback.connect(progress.finish_progress)
    exporter.start()
    progress.exec()


# 导出选股器找到的股票列表
def export_selected_stock_list():
    return QFileDialog.getSaveFileName(directory=selected_stock_list_path(), filter='TXT(*.txt)')


# 导入选股器找到的股票列表
def import_selected_stock_list():
    return QFileDialog.getOpenFileName(directory=selected_stock_list_path(), filter='TXT(*.txt)')


class StockDataExporter(QThread):
    progressBarCallback = pyqtSignal(int, str, str)
    finishedCallback = pyqtSignal()

    def __init__(self):
        super().__init__()
        now = QDate.currentDate()
        start_date = now.addMonths(-3)
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
            result = baostock.query_history_k_data_plus(code=market + "." + code, fields="date,open,high,low,close,preclose,pctChg,turn,tradestatus,isST",
                                                        start_date=self.startDate, end_date=self.today, frequency="d", adjustflag="2")
            save_stock_history_data(result, code)
            self.progressBarCallback.emit(index + 1, code, name)
        self.finishedCallback.emit()
