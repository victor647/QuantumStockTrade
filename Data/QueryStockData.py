import baostock, pandas, math
from PyQt5.QtCore import QDate, QThread, pyqtSignal
from Tools import Tools, ProgressBar, FileManager


# 获取最新全部股票数据
def query_all_stock_daily_data():
    stock_list = FileManager.read_stock_list_file()
    exporter = QueryStockDailyData(stock_list)
    progress = ProgressBar.ProgressBar(stock_list.shape[0], '正在爬取股票历史数据', exporter)
    progress.show()
    exporter.progressBarCallback.connect(progress.update_search_progress)
    exporter.finishedCallback.connect(progress.finish_progress)
    exporter.start()
    progress.exec()


# 获取股票日线图
class QueryStockDailyData(QThread):
    progressBarCallback = pyqtSignal(int, str, str)
    finishedCallback = pyqtSignal()

    def __init__(self, stock_list: pandas.DataFrame):
        super().__init__()
        now = QDate.currentDate()
        start_date = now.addYears(-1)
        self.today = now.toString('yyyy-MM-dd')
        self.startDate = start_date.toString('yyyy-MM-dd')
        self.stockList = stock_list

    def run(self):
        # 获取上证综指
        self.fetch_stock_data('sh', '000001', True)
        # 获取深证成指
        self.fetch_stock_data('sz', '399001', True)
        # 获取创业板指
        self.fetch_stock_data('sz', '399006', True)
        for index, row in self.stockList.iterrows():
            code_num = row['code']
            # 将股票代码固定为6位数
            code = str(code_num).zfill(6)
            # 获得股票中文名称
            name = row['name']
            # 跳过无效数据
            if type(name) != str:
                continue
            # 获取股票交易所
            market, index_code = Tools.get_trade_center_and_index(code)
            # 获取股票历史数据
            if index_code != '000000':
                self.fetch_stock_data(market, code)
            self.progressBarCallback.emit(index + 1, code, name)
        self.finishedCallback.emit()

    # 向服务器请求股票数据
    def fetch_stock_data(self, market: str, code: str, is_market=False):
        result = baostock.query_history_k_data_plus(code=market + '.' + code, fields='date,open,high,low,close,preclose,turn,amount,peTTM,pbMRQ,psTTM,tradestatus,isST',
                                                    start_date=self.startDate, end_date=self.today, frequency='d', adjustflag='2')
        FileManager.save_stock_history_data(result, code if not is_market else market + code)


# 获取列表股票15分钟K线数据
def query_stocks_15min_data(stock_list: list, parser):
    searcher = QueryStockFifteenMinData(stock_list, parser)
    progress = ProgressBar.ProgressBar(len(stock_list), '正在爬取股票15分钟K线', searcher)
    progress.show()
    searcher.progressBarCallback.connect(progress.update_search_progress)
    searcher.finishedCallback.connect(progress.finish_progress)
    searcher.start()
    progress.exec()


# 获取股票15分钟线图
class QueryStockFifteenMinData(QThread):
    progressBarCallback = pyqtSignal(int, str, str)
    finishedCallback = pyqtSignal()

    def __init__(self, stock_list: list, parser):
        super().__init__()
        now = QDate.currentDate()
        start_date = now.addMonths(-1)
        self.today = now.toString('yyyy-MM-dd')
        self.startDate = start_date.toString('yyyy-MM-dd')
        self.stockList = stock_list
        self.parser = parser

    def run(self):
        i = 0
        for stock_code in self.stockList:
            i += 1
            market, index_code = Tools.get_trade_center_and_index(stock_code)
            # 获取股票历史数据
            if index_code != '000000':
                self.parser(stock_code, self.query_fifteen_min_data(market, stock_code))
            self.progressBarCallback.emit(i, stock_code, '')
        self.finishedCallback.emit()

    # 获取15分钟K线数据
    def query_fifteen_min_data(self, market: str, code: str):
        bs_result = baostock.query_history_k_data_plus(code=market + '.' + code, fields='open,high,low,close',
                                                    start_date=self.startDate, end_date=self.today, frequency='15', adjustflag='2')
        data = pandas.DataFrame(bs_result.data, columns=bs_result.fields, dtype=float)
        return data
