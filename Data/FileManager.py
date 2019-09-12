import os.path as path
import pandas
import tushare
import baostock
import Tools
from PyQt5.QtCore import QDate, QThread, pyqtSignal
from Windows.ProgressBar import ProgressBar


def stock_list_path():
    return path.join(path.pardir, "Data", "stock_list.csv")


def read_stock_list_file():
    return pandas.read_csv(stock_list_path())


def save_stock_list_file():
    stock_list = tushare.get_stock_basics()
    stock_list.to_csv(stock_list_path())
    return stock_list


def stock_history_path(stock_code):
    return path.join(path.pardir, "Data\\StockHistory", stock_code + ".csv")


def read_stock_history_data(stock_code):
    return pandas.read_csv(stock_history_path(stock_code))


def save_stock_history_data(bs_result, stock_code):
    data = pandas.DataFrame(bs_result.data, columns=bs_result.fields)
    data.to_csv(stock_history_path(stock_code))


def export_all_stock_data():
    stock_list = save_stock_list_file()
    progress = ProgressBar(stock_list.shape[0])
    progress.show()
    exporter = StockDataExporter()
    exporter.progressBarCallback.connect(progress.update_search_progress)
    exporter.start()


class StockDataExporter(QThread):
    progressBarCallback = pyqtSignal(int, str, str)

    def __init__(self):
        super().__init__()
        now = QDate.currentDate()
        start_date = now.addMonths(-1)
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
            market = Tools.get_trade_center(code)
            result = baostock.query_history_k_data_plus(code=market + "." + code, fields="date,open,high,low,close,preclose,pctChg,turn,tradestatus,isST",
                                                        start_date=self.startDate, end_date=self.today, frequency="d", adjustflag="2")
            save_stock_history_data(result, code)
            self.progressBarCallback.emit(index + 1, code, name)
