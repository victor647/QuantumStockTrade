from QtDesign.ScheduledInvestment_ui import Ui_ScheduledInvestment
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QFileDialog, QHeaderView
from PyQt5.QtCore import QDate
from Data.InvestmentStatus import StockInvestment
from Data.HistoryGraph import HistoryGraph
import Data.TechnicalAnalysis as TechnicalAnalysis
from Tools import Tools, FileManager
import baostock, pandas, math


# 定投组合模拟
class ScheduledInvestment(QMainWindow, Ui_ScheduledInvestment):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.cbbIntervalType.addItems(['周', '月'])
        # 默认以月定投
        self.cbbIntervalType.setCurrentText('月')
        # 默认开始日期为10年前
        self.dteStartDate.setDate(QDate.currentDate().addYears(-10))
        self.__stockInvestments = {}
        self.tblStockList.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.__stockData = {}

    # 读取股票列表（可多选）
    def import_stock_list(self):
        full_data = FileManager.import_scheduled_investment_stock_list()
        for code, share in full_data.items():
            self.fill_stock_list(code, int(share))

    # 导出股票列表
    def export_stock_list(self):
        FileManager.export_scheduled_investment_stocks(self.tblStockList)

    # 清空股票列表
    def clear_stock_list(self):
        self.tblStockList.setRowCount(0)

    # 添加股票按钮
    def add_stock_code(self):
        stock_code = Tools.get_stock_code(self.iptStockCode)
        if stock_code == '':
            Tools.show_error_dialog('股票代码或名称无效！')
        else:
            self.fill_stock_list(stock_code, 0)
        self.tblStockList.repaint()

    # 移除一只股票
    def remove_stock_code(self):
        selection = self.tblStockList.selectedIndexes()
        if len(selection) == 0:
            return
        index = selection[0].row()
        self.tblStockList.removeRow(index)
        self.tblStockList.repaint()

    # 根据导入的选股列表文件填表
    def fill_stock_list(self, code: str, share: int):
        row = self.tblStockList.rowCount()
        self.tblStockList.insertRow(row)
        # 获取股票名称
        name = Tools.get_stock_name_from_code(code)
        self.tblStockList.setItem(row, 0, QTableWidgetItem(code))
        self.tblStockList.setItem(row, 1, QTableWidgetItem(name))
        Tools.add_sortable_item(self.tblStockList, row, 2, share, str(share) + '%')
        self.tblStockList.repaint()

    # 股票详细信息
    def show_stock_graph(self, row: int, column: int):
        code = self.tblStockList.item(row, 0).text()
        # 通过网页打开
        if column < 2:
            Tools.open_stock_page(code)
        # 直接画K线图
        elif column > 2:
            graph = HistoryGraph(code, self.__stockData[code], True)
            graph.plot_all_ma_lines()
            graph.plot_price()
            graph.plot_volume()
            graph.plot_trade_history(self.__stockInvestments[code])
            graph.exec_()

    # 导出股票交易策略
    def export_investment_plan(self):
        file_path = QFileDialog.getSaveFileName(directory=FileManager.investment_plan_path(), filter='JSON(*.json)')
        data = {
            'startDate': self.dteStartDate.date(),
            'initialInvestment': self.spbInitialInvestment.value(),
            'interval': self.spbInterval.value(),
            'intervalType': self.cbbIntervalType.currentText(),
            'eachInvestment': self.spbEachInvestment.value(),
        }
        if file_path[0] != '':
            FileManager.export_config_as_json(data, file_path[0])

    # 导入股票交易策略
    def import_investment_plan(self):
        file_path = QFileDialog.getOpenFileName(directory=FileManager.investment_plan_path(), filter='JSON(*.json)')
        if file_path[0] != '':
            data = FileManager.import_json_config(file_path[0])
            if 'moneyPerTrade' not in data:
                Tools.show_error_dialog('选取的配置文件格式不对！')
                return
            self.dteStartDate.setDate(data['startDate'])
            self.spbInitialInvestment.setValue(data['initialInvestment'])
            self.spbInterval.setValue(data['interval'])
            self.cbbIntervalType.setCurrentText(data['intervalType'])
            self.spbEachInvestment.setValue(data['eachInvestment'])

    # 开始定投模拟
    def start_investing(self):
        start_date = self.dteStartDate.date()
        end_date = QDate.currentDate()
        frequency = 'w' if self.cbbIntervalType.currentText() == '周' else 'm'
        total_share_ratio = 0
        for row in range(self.tblStockList.rowCount()):
            stock_code = self.tblStockList.item(row, 0).text()
            self.__stockInvestments[stock_code] = StockInvestment()

            market = Tools.get_trade_center(stock_code)
            bs_result = baostock.query_history_k_data(code=market + '.' + stock_code, fields='date,open,high,low,close,turn',
                                                      start_date=start_date.toString('yyyy-MM-dd'), end_date=end_date.toString('yyyy-MM-dd'), frequency=frequency, adjustflag='2')
            if not bs_result.data:
                Tools.show_error_dialog('数据有误！')
                continue
            stock_data = pandas.DataFrame(bs_result.data, columns=bs_result.fields, dtype=float)
            stock_data.set_index('date', inplace=True)
            self.__stockData[stock_code] = stock_data
            # 获取均线数据
            TechnicalAnalysis.calculate_all_ma_curves(stock_data)
            # 开始价格
            start_price = stock_data.iloc[0]['open']
            # 当前价格
            end_price = stock_data.iloc[-1]['close']
            # 获取实际k线开始和截止日期
            start_date = QDate.fromString(stock_data.index[0], 'yyyy-MM-dd')
            end_date = QDate.fromString(stock_data.index[-1], 'yyyy-MM-dd')
            years = int(stock_data.index[-1][:4]) - int(stock_data.index[0][:4]) + 1
            # 年化复利
            annual_profit = round((math.pow(end_price / start_price, 1 / years) - 1) * 100, 2)
            column = Tools.add_colored_item(self.tblStockList, row, 3,  annual_profit, '%')
            # 仓位百分比
            share_ratio = float(self.tblStockList.item(row, 2).text().strip('%')) / 100
            total_share_ratio += share_ratio
            # 超过100%仓位则跳过
            if total_share_ratio > 1:
                continue
            # 最后一只股票，仍然未满仓，则补齐
            elif row == self.tblStockList.rowCount() - 1 and total_share_ratio < 1:
                share_ratio += 1 - total_share_ratio
                self.tblStockList.item(row, 2).setText(str(share_ratio * 100) + '%')
            # 进行首笔投资
            self.__stockInvestments[stock_code].buy_stock_by_money(start_price, share_ratio * self.spbInitialInvestment.value() * 10000, start_date.toString('yyyy-MM-dd'))
            self.__stockInvestments[stock_code].initial_invest()
            # 当前交易日期
            current_date = QDate(start_date)
            # 进行每次定投
            while current_date < end_date:
                if self.cbbIntervalType.currentText() == '周':
                    current_date = current_date.addDays(7 * self.spbInterval.value())
                    # 确保每周一买入
                    while current_date.dayOfWeek() > 1:
                        current_date = current_date.addDays(-1)
                else:
                    current_date = current_date.addMonths(self.spbInterval.value())
                    # 确保每月第一天买入
                    if current_date.day() > 1:
                        current_date = current_date.addDays(-current_date.day() + 1)
                # 获得该交易日信息
                data = stock_data.loc[current_date.toString('yyyy-MM-dd'):].head(1)
                # 跳过停牌股票
                if data.shape[0] > 0 and data.iloc[0]['high'] != data.iloc[0]['low']:
                    self.__stockInvestments[stock_code].buy_stock_by_money(data.iloc[0]['open'], share_ratio * self.spbEachInvestment.value() * 10000, data.index[0])

            # 总计投入
            total_investment = round(self.__stockInvestments[stock_code].totalInvestment, 2)
            column = Tools.add_sortable_item(self.tblStockList, row, column, total_investment)
            # 当前价格
            final_price = round(stock_data.iloc[-1]['close'], 2)
            column = Tools.add_colored_item(self.tblStockList, row, column, self.__stockInvestments[stock_code].net_profit(final_price))
            profit_percentage = self.__stockInvestments[stock_code].profit_percentage(final_price)
            Tools.add_colored_item(self.tblStockList, row, column, profit_percentage, '%')









