from QtDesign.ScheduledInvestment_ui import Ui_ScheduledInvestment
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QFileDialog
from PyQt5.QtCore import Qt, QDate
from Tools import Tools, FileManager
import baostock, pandas, math


# 定投组合模拟
class ScheduledInvestment(QMainWindow, Ui_ScheduledInvestment):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.cbbIntervalType.addItems(['周', '月'])

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
        row_count = self.tblStockList.rowCount()
        self.tblStockList.insertRow(row_count)
        # 获取股票名称
        name = Tools.get_stock_name_from_code(code)
        self.tblStockList.setItem(row_count, 0, QTableWidgetItem(code))
        self.tblStockList.setItem(row_count, 1, QTableWidgetItem(name))
        Tools.add_sortable_item(self.tblStockList, share, str(share) + '%', row_count, 2)
        self.tblStockList.repaint()

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
        start_date = self.dteStartDate.date().toString('yyyy-MM-dd')
        end_date = QDate.currentDate().toString('yyyy-MM-dd')
        frequency = 'w' if self.cbbIntervalType.currentText() == '周' else 'y'
        for row in range(self.tblStockList.rowCount()):
            stock_code = self.tblStockList.item(row, 0).text()
            market = Tools.get_trade_center(stock_code)
            bs_result = baostock.query_history_k_data(code=market + '.' + stock_code, fields='date,open,high,low,close,pctChg',
                                                      start_date=start_date, end_date=end_date, frequency=frequency, adjustflag='2')
            stock_data = pandas.DataFrame(bs_result.data, columns=bs_result.fields, dtype=float)
            # 开始价格
            start_price = stock_data.iloc[0]['open']
            # 当前价格
            end_price = stock_data.iloc[-1]['close']
            years = int(stock_data.iloc[-1]['date'][:4]) - int(stock_data.iloc[0]['date'][:4]) + 1
            # 年化复利
            annual_profit = round((math.pow(end_price / start_price, 1 / years) - 1) * 100, 2)
            Tools.add_colored_item(self.tblStockList, annual_profit, row, 3, '%')
            # 初始投资
            percentage = int(self.tblStockList.item(row, 2).text())
            self.buy_stock(stock_code, start_price, percentage, self.spbInitialInvestment.value())

    def buy_stock(self, code: str, price: float, percentage: int, total_money: int):
        allocated_money = total_money * percentage / 100
        # 计算买入股数，至少买入100股
        share = max(round(allocated_money / (price * 100)), 1) * 100
        actual_money = share * price







