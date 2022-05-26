from PyQt5.QtCore import pyqtSignal, QThread
from Tools import FileManager, Tools
from Tools.ProgressBar import ProgressBar
import ShortTermTrading.StockFinder as StockFinder
import ShortTermTrading.FiveDayFinder as FiveDayFinder
import Data.TechnicalAnalysis as TA
import baostock, pandas


# 选股算法基类
class StockSearcher(QThread):
    addItemCallback = pyqtSignal(list)
    progressBarCallback = pyqtSignal(int, str, str)
    finishedCallback = pyqtSignal()

    def __del__(self):
        self.work = False
        self.terminate()


# 多线程股票搜索算法
class StandardStockSearcher(StockSearcher):

    def __init__(self, search_date: str, export_to_file: bool, folder_name=''):
        super().__init__()
        self.stockList = FileManager.read_stock_list_file()
        self.selectedStocks = []
        self.searchDate = search_date
        # 弹出选股进度条
        progress_bar = ProgressBar(self.stockList.shape[0], search_date + '选股', self)
        progress_bar.show()
        self.progressBarCallback.connect(progress_bar.update_search_progress)
        self.finishedCallback.connect(progress_bar.destroy)
        if export_to_file:
            self.finishedCallback.connect(lambda: FileManager.export_auto_search_stock_list(self.selectedStocks, folder_name, self.searchDate))

    def run(self):
        # 获取大盘数据
        index_shanghai_performance = TA.market_performance_by_days('sh000001', self.searchDate, 5)
        index_shenzhen_performance = TA.market_performance_by_days('sz399001', self.searchDate, 5)
        index_startup_performance = TA.market_performance_by_days('sz399006', self.searchDate, 5)
        for index, row in self.stockList.iterrows():
            code_num = row['code']
            # 将股票代码固定为6位数
            stock_code = str(code_num).zfill(6)
            # 获得股票中文名称
            name = row['name']
            # 更新窗口进度条
            self.progressBarCallback.emit(index, stock_code, name)
            # 判断股票是否在选中的交易所中
            if not StockFinder.Instance.code_in_search_range(code_num):
                continue
            # 获得股票历史数据
            stock_data = FileManager.read_stock_history_data(stock_code, True)
            # 选股日期之前和之后的数据
            data_before_search = TA.get_stock_data_before_date(stock_data, self.searchDate)
            # 新股还没上市
            if data_before_search.empty:
                continue
            # 技术面指标考察
            if not StockFinder.Instance.match_technical_criterias(data_before_search):
                continue
            # 自定义指标考察
            if not StockFinder.Instance.match_custom_criterias(data_before_search):
                continue
            # 基本面指标考察
            data_today = data_before_search.iloc[-1]
            date = data_today.name
            code_with_market = row['market'] + '.' + stock_code
            bs_result = baostock.query_history_k_data_plus(code=code_with_market, fields='isST,peTTM,pbMRQ,psTTM', frequency='d', start_date=date)
            if len(bs_result.data) == 0:
                continue
            basic_data = pandas.DataFrame(bs_result.data, columns=bs_result.fields, dtype=float).iloc[0]
            data_today['isST'] = basic_data['isST']
            data_today['peTTM'] = basic_data['peTTM']
            data_today['pbMRQ'] = basic_data['pbMRQ']
            data_today['psTTM'] = basic_data['psTTM']
            if not StockFinder.Instance.match_basic_criterias(data_today):
                continue

            data_after_search = TA.get_stock_data_after_date(stock_data, self.searchDate)
            # 选股日收盘价
            pre_close = round(data_today['close'], 2)
            # 跑赢大盘
            # market, index_code = Tools.get_trade_center_and_index(stock_code)
            # if index_code == '000001':
            #     index_performance = index_shanghai_performance
            # elif index_code == '399001':
            #     index_performance = index_shenzhen_performance
            # else:
            #     index_performance = index_startup_performance
            # market_difference = round(five_day_close - index_performance, 2)
            # 次日最高
            next_day_high = TA.get_stock_extremes_in_day_range(data_after_search, pre_close, 1, 1, 'high')
            # 次日最低
            next_day_low = TA.get_stock_extremes_in_day_range(data_after_search, pre_close, 1, 1, 'low')
            # 五日最高
            five_day_high = TA.get_stock_extremes_in_day_range(data_after_search, pre_close, 1, 5, 'high')
            # 五日最低
            five_day_low = TA.get_stock_extremes_in_day_range(data_after_search, pre_close, 1, 5, 'low')
            # 最高收益
            max_profit = TA.get_percent_change_from_price(TA.get_price_from_percent_change(pre_close, five_day_high),
                                                          TA.get_price_from_percent_change(pre_close, five_day_low))
            pe = round(data_today['peTTM'], 2)
            pb = round(data_today['pbMRQ'], 2)
            ps = round(data_today['psTTM'], 2)
            industry_info = baostock.query_stock_industry(code=code_with_market, date=date).data
            industry = industry_info[0][3] if len(industry_info) > 0 else ''
            # 将符合要求的股票信息打包
            items = [stock_code, name, industry, pre_close, next_day_high, next_day_low, five_day_high, five_day_low, pe, pb, ps]
            # 添加股票信息至列表
            self.addItemCallback.emit(items)
            self.selectedStocks.append(stock_code)
        # 搜索结束回调
        self.finishedCallback.emit()


# 五日图形分析算法
class FiveDaySearcher(StockSearcher):
    _stockData = None
    _maxDaysUsed = 1

    # 计算图形出现后x日的股价表现
    def get_day_performance(self, shape_start_date: int, days: int):
        shape_end_day_index = shape_start_date + self._maxDaysUsed
        period_end_day_index = shape_end_day_index + days
        # 若距今日期不够，则按照最后一日价格计算
        if period_end_day_index >= self._stockData.shape[0]:
            period_end_day_index = -1
        # 获得图形出现时价格和x日后价格
        shape_end_price = self._stockData.iloc[shape_end_day_index]['close']
        period_end_price = self._stockData.iloc[period_end_day_index]['close']
        return TA.get_percent_change_from_price(period_end_price, shape_end_price)


# 单只股票多日分析
class FiveDaySearcherSingle(FiveDaySearcher):

    def __init__(self, stock_code: str):
        super().__init__()
        self.stockCode = stock_code
        self._stockData = FileManager.read_stock_history_data(self.stockCode, True)
        # 获取条件组中用到的最长日数
        self._maxDaysUsed = FiveDayFinder.Instance.criteriaItems[-1].dayIndex - 1
        # 弹出选股进度条
        progress_bar = ProgressBar(self._stockData.shape[0], self.stockCode + '图形寻找', self)
        progress_bar.show()
        self.progressBarCallback.connect(progress_bar.update_search_progress)
        self.finishedCallback.connect(progress_bar.destroy)

    def run(self):
        # 获取股票名称
        stock_name = Tools.get_stock_name_from_code(self.stockCode)
        for day_index in range(self._stockData.shape[0] - self._maxDaysUsed):
            date = self._stockData.index[day_index]
            self.progressBarCallback.emit(day_index, stock_name, date)
            if FiveDayFinder.Instance.match_criteria(day_index, self._stockData):
                next_day_performance = self.get_day_performance(day_index, 1)
                three_day_performance = self.get_day_performance(day_index, 3)
                five_day_performance = self.get_day_performance(day_index, 5)
                ten_day_performance = self.get_day_performance(day_index, 10)
                # 打包数据列表
                items = [self.stockCode, stock_name, date, next_day_performance, three_day_performance, five_day_performance, ten_day_performance]
                self.addItemCallback.emit(items)
        # 搜索结束回调
        self.finishedCallback.emit()


# 多只股票单日分析
class FiveDaySearcherMultiple(FiveDaySearcher):

    def __init__(self, search_date: str):
        super().__init__()
        self.searchDate = search_date
        self.stockList = FileManager.read_stock_list_file()
        # 获取条件组中用到的最长日数
        self._maxDaysUsed = FiveDayFinder.Instance.criteriaItems[-1].dayIndex - 1
        # 弹出选股进度条
        progress_bar = ProgressBar(self.stockList.shape[0], search_date + '图形寻找', self)
        progress_bar.show()
        self.progressBarCallback.connect(progress_bar.update_search_progress)
        self.finishedCallback.connect(progress_bar.destroy)

    def run(self):
        for index, row in self.stockList.iterrows():
            code_num = row['code']
            # 将股票代码固定为6位数
            code = str(code_num).zfill(6)
            # 获得股票中文名称
            name = row['name']
            # 更新窗口进度条
            self.progressBarCallback.emit(index, code, name)
            # 获得股票历史数据
            self._stockData = FileManager.read_stock_history_data(code, True)
            # 选股日期不在K线中，非交易日或新股
            if self.searchDate not in self._stockData.index:
                continue
            day_index = self._stockData.index.get_loc(self.searchDate)
            if FiveDayFinder.Instance.match_criteria(day_index, self._stockData):
                next_day_performance = self.get_day_performance(day_index, 1)
                three_day_performance = self.get_day_performance(day_index, 3)
                five_day_performance = self.get_day_performance(day_index, 5)
                ten_day_performance = self.get_day_performance(day_index, 10)
                # 打包数据列表
                items = [code, name, self.searchDate, next_day_performance, three_day_performance, five_day_performance, ten_day_performance]
                self.addItemCallback.emit(items)
        # 搜索结束回调
        self.finishedCallback.emit()
