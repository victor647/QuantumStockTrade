import baostock, pandas, math
from PyQt5.QtCore import QDate, QThread, pyqtSignal
from Tools import Tools, ProgressBar, FileManager


# 获取最新全部股票数据
def query_all_stock_data():
    stock_list = FileManager.read_stock_list_file()
    exporter = QueryStockData(stock_list)
    progress = ProgressBar.ProgressBar(stock_list.shape[0], '正在爬取股票历史数据', exporter)
    progress.show()
    exporter.progressBarCallback.connect(progress.update_search_progress)
    exporter.finishedCallback.connect(progress.finish_progress)
    exporter.start()
    progress.exec()


class QueryStockData(QThread):
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
        result = baostock.query_history_k_data_plus(code=market + '.' + code, fields='date,open,high,low,close,preclose,turn,peTTM,pbMRQ,psTTM,tradestatus,isST',
                                                    start_date=self.startDate, end_date=self.today, frequency='d', adjustflag='2')
        FileManager.save_stock_history_data(result, code if not is_market else market + code)
