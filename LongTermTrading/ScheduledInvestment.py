from QtDesign.ScheduledInvestment_ui import Ui_ScheduledInvestment
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QFileDialog, QHeaderView
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QKeyEvent
from Data.InvestmentStatus import StockInvestment
from Data.HistoryGraph import CandleStickChart
import Data.TechnicalAnalysis as TA
from Tools import Tools, FileManager
import baostock, pandas, math


# 定投组合模拟
class ScheduledInvestment(QMainWindow, Ui_ScheduledInvestment):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 默认开始日期为10年前
        self.dteStartDate.setDate(QDate.currentDate().addYears(-10))
        self.__stockInvestments = {}
        self.tblStockList.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.__stockData = {}

    # 读取股票列表（可多选）
    def import_stock_list(self):
        full_data = FileManager.import_scheduled_investment_stock_list()
        for code, share in full_data:
            self.fill_stock_list(code, share)

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
            self.fill_stock_list(stock_code, '0')

    # 移除一只股票
    def remove_stock_code(self):
        selection = self.tblStockList.selectedIndexes()
        if len(selection) == 0:
            return
        index = selection[0].row()
        self.tblStockList.removeRow(index)

    # 根据导入的选股列表文件填表
    def fill_stock_list(self, code: str, share: str):
        name = Tools.get_stock_name_from_code(code)
        if name == '':
            return
        row = self.tblStockList.rowCount()
        self.tblStockList.insertRow(row)
        self.tblStockList.setItem(row, 0, QTableWidgetItem(code))
        self.tblStockList.setItem(row, 1, QTableWidgetItem(name))
        Tools.add_sortable_item(self.tblStockList, row, 2, float(share.strip('%')), share)
        # 获取上市日期
        stock_list = FileManager.read_stock_list_file()
        stock_list.set_index('name', inplace=True)
        time_to_market = str(stock_list.loc[name]['timeToMarket'])
        # 优化日期格式
        time_to_market = time_to_market[:4] + '-' + time_to_market[4:6] + '-' + time_to_market[6:]
        self.tblStockList.setItem(row, 3, QTableWidgetItem(time_to_market))

    # 快捷键设置
    def keyPressEvent(self, key: QKeyEvent):
        # 回车键添加股票
        if key.key() == Qt.Key_Enter or key.key() == Qt.Key_Return:
            self.add_stock_code()
        # 按删除键删除股票或指标组
        elif key.key() == Qt.Key_Delete or key.key() == Qt.Key_Backspace:
            self.remove_stock_code()

    # 股票详细信息
    def show_stock_graph(self, row: int, column: int):
        stock_code = self.tblStockList.item(row, 0).text()
        # 通过网页打开
        if column < 2:
            Tools.open_stock_page(stock_code)
        # 直接画K线图
        elif column > 2:
            graph = CandleStickChart(self.__stockData[stock_code], stock_code, True)
            graph.plot_ma(self.spbSmartBuyMaPeriod.value(), Qt.yellow)
            graph.plot_price()
            graph.plot_volume()
            graph.plot_trade_history(self.__stockInvestments[stock_code])
            graph.exec_()

    # 导出股票交易策略
    def export_investment_plan(self):
        file_path = QFileDialog.getSaveFileName(directory=FileManager.investment_plan_path(), filter='JSON(*.json)')
        data = {
            'startDate': self.dteStartDate.date().toString('yyyy-MM-dd'),
            'initialInvestment': self.spbInitialInvestment.value(),
            'investInterval': self.spbInvestInterval.value(),
            'eachInvestment': self.spbEachInvestment.value(),
            'smartBuy': self.cbxSmartBuy.isChecked(),
            'smartBuyMaPeriod': self.spbSmartBuyMaPeriod.value(),
            'smartBuyMaBias': self.spbSmartBuyMaBias.value(),
            'smartBuyFactor': self.spbSmartBuyFactor.value(),
            'smartSell': self.cbxSmartSell.isChecked(),
            'smartSellThreshold': self.spbSmartSellThreshold.value(),
            'smartSellFactor': self.spbSmartSellFactor.value(),
            'sellByPercent': self.cbxSellByPercent.isChecked(),
            'buyBackAfterSell': self.cbxBuyBackAfterSell.isChecked(),
        }
        if file_path[0] != '':
            FileManager.export_config_as_json(data, file_path[0])

    # 导入股票交易策略
    def import_investment_plan(self):
        file_path = QFileDialog.getOpenFileName(directory=FileManager.investment_plan_path(), filter='JSON(*.json)')
        if file_path[0] != '':
            data = FileManager.import_json_config(file_path[0])
            if 'eachInvestment' not in data:
                Tools.show_error_dialog('选取的配置文件格式不对！')
                return
            self.dteStartDate.setDate(QDate.fromString(data['startDate'], 'yyyy-MM-dd'))
            self.spbInitialInvestment.setValue(data['initialInvestment'])
            self.spbInvestInterval.setValue(data['investInterval'])
            self.spbEachInvestment.setValue(data['eachInvestment'])
            self.cbxSmartBuy.setChecked(data['smartBuy'])
            self.spbSmartBuyMaPeriod.setValue(data['smartBuyMaPeriod'])
            self.spbSmartBuyMaBias.setValue(data['smartBuyMaBias'])
            self.spbSmartBuyFactor.setValue(data['smartBuyFactor'])
            self.cbxSmartSell.setChecked(data['smartSell'])
            self.spbSmartSellThreshold.setValue(data['smartSellThreshold'])
            self.spbSmartSellFactor.setValue(data['smartSellFactor'])
            self.cbxSellByPercent.setChecked(data['sellByPercent'])
            self.cbxBuyBackAfterSell.setChecked(data['buyBackAfterSell'])

    # 平均分配持股仓位
    def auto_split_ratio(self):
        # 获取股票数量
        stock_count = self.tblStockList.rowCount()
        # 计算平均仓位
        share = round(100 / stock_count, 2)
        for row in range(stock_count):
            Tools.add_sortable_item(self.tblStockList, row, 2, share, str(share) + '%')

    # 开始定投模拟
    def start_investing(self):
        start_date = self.dteStartDate.date()
        end_date = QDate.currentDate()
        # 所有股票总计
        total_share_ratio = total_spent = total_profit = 0
        for row in range(self.tblStockList.rowCount()):
            stock_code = self.tblStockList.item(row, 0).text()
            market, index_code = Tools.get_trade_center_and_index(stock_code)
            bs_result = baostock.query_history_k_data(code=market + '.' + stock_code, fields='date,open,high,low,close,turn',
                                                      start_date=start_date.toString('yyyy-MM-dd'), end_date=end_date.toString('yyyy-MM-dd'), frequency='m', adjustflag='2')
            if not bs_result.data:
                Tools.show_error_dialog('数据有误！')
                continue
            stock_data = pandas.DataFrame(bs_result.data, columns=bs_result.fields, dtype=float)
            stock_data.set_index('date', inplace=True)
            TA.calculate_ma_curve(stock_data, self.spbSmartBuyMaPeriod.value())
            self.__stockData[stock_code] = stock_data
            investment = StockInvestment()
            self.__stockInvestments[stock_code] = investment
            # 开始价格
            start_price = stock_data.iloc[0]['open']
            # 当前价格
            end_price = stock_data.iloc[-1]['close']
            # 获取实际k线开始和截止日期
            actual_start_date = QDate.fromString(stock_data.index[0], 'yyyy-MM-dd')
            years = int(stock_data.index[-1][:4]) - int(stock_data.index[0][:4]) + 1
            # 年化复利
            annual_profit = round((math.pow(end_price / start_price, 1 / years) - 1) * 100, 2)
            column = Tools.add_colored_item(self.tblStockList, row, 4,  annual_profit, '%')
            # 仓位百分比
            share_ratio = float(self.tblStockList.item(row, 2).text().strip('%')) / 100
            total_share_ratio += share_ratio
            # 超过100%仓位则跳过
            if round(total_share_ratio, 2) > 1:
                continue
            # 最后一只股票，仍然未满仓，则补齐
            elif row == self.tblStockList.rowCount() - 1 and total_share_ratio < 1:
                share_ratio += 1 - total_share_ratio
                self.tblStockList.item(row, 2).setText(str(round(share_ratio * 100, 2)) + '%')
            # 进行首笔投资，上市日期晚于定投开始日期的新股跳过
            time_to_market = QDate.fromString(self.tblStockList.item(row, 3).text(), 'yyyy-MM-dd')
            if time_to_market < start_date:
                investment.buy_stock_by_money(start_price, share_ratio * self.spbInitialInvestment.value() * 10000, actual_start_date.toString('yyyy-MM-dd'))
            # 记录上次买卖的价格
            last_price = start_price
            # 记录上次操作的净买入金额
            last_trade_money = 1
            # 初始化最高亏损额
            max_losing = 0
            # 每期基础买入额
            base_money = share_ratio * self.spbEachInvestment.value() * 10000
            month_index = 0
            # 进行每次定投
            for date, month_data in stock_data.iterrows():
                month_index += 1
                # 跳过第一个月和停牌时期
                if month_index == 1 or month_data['turn'] == 0:
                    continue
                open_price = month_data['open']
                # 计算当期最高亏损额
                max_losing = min(max_losing, investment.net_profit(month_data['close']))
                money = base_money
                # 若单月涨幅过高则卖出
                if self.cbxSellByPercent.isChecked():
                    sell_price = TA.get_price_from_percent_change(open_price, self.spbSellByPercent.value())
                    sell_count = 1
                    # 每上涨X%卖出一次
                    while sell_price <= month_data['high']:
                        investment.sell_stock_by_money(sell_price, money, date)
                        sell_count += 1
                        sell_price = TA.get_price_from_percent_change(open_price, self.spbSellByPercent.value() * sell_count)

                # 若单月跌幅过高则买入
                if self.cbxBuyByPercent.isChecked():
                    buy_price = TA.get_price_from_percent_change(open_price, -self.spbBuyByPercent.value())
                    buy_count = 1
                    # 每下跌X%买入一次
                    while buy_price >= month_data['low']:
                        investment.buy_stock_by_money(buy_price, money, date)
                        buy_count += 1
                        buy_price = TA.get_price_from_percent_change(open_price, -self.spbBuyByPercent.value() * buy_count)

                # 跳过定投间隔月
                if month_index % self.spbInvestInterval.value() != 1:
                    continue

                # 允许根据上期买入价格进行卖出
                if self.cbxSmartSell.isChecked():
                    percent_change = TA.get_percent_change_from_price(open_price, last_price) - self.spbSmartSellThreshold.value()
                    if percent_change >= 0:
                        money *= max(0, 1 + self.spbSmartSellFactor.value() * percent_change / 100)
                        last_trade_money = -money
                        investment.sell_stock_by_money(open_price, TA.get_price_from_percent_change(money, percent_change), date)
                        last_price = open_price
                        continue

                # 允许自动根据涨幅调节买入额
                if self.cbxSmartBuy.isChecked():
                    # 计算距离均线的偏离值
                    ma_price = month_data['ma_' + str(self.spbSmartBuyMaPeriod.value())]
                    percent_change = TA.get_percent_change_from_price(open_price, ma_price) - self.spbSmartBuyMaBias.value()
                    # 计算实际投入金钱
                    money *= max(0, 1 - self.spbSmartBuyFactor.value() * percent_change / 100)
                    # 上次卖出了，这次下跌了买回来
                    if self.cbxBuyBackAfterSell.isChecked() and last_trade_money < 0 and open_price < last_price:
                        money -= last_trade_money
                if money > 0:
                    last_trade_money = money
                    investment.buy_stock_by_money(open_price, money, date)
                last_price = open_price

            # 累计投入
            column = Tools.add_sortable_item(self.tblStockList, row, column, round(investment.totalInvestment, 2))
            # 最终获利
            final_price = round(stock_data.iloc[-1]['close'], 2)
            investment.sell_all(final_price, stock_data.index[-1])
            column = Tools.add_colored_item(self.tblStockList, row, column, investment.final_profit())
            # 最高亏损额
            column = Tools.add_colored_item(self.tblStockList, row, column, max_losing)
            # 计算收益率
            Tools.add_colored_item(self.tblStockList, row, column, investment.final_profit_percentage(), '%')
            # 累计所有股票成本与利润
            total_spent += investment.totalInvestment
            total_profit += investment.final_profit()
        self.lblTradeSummary.setText('共计成本{}元，至今获利{}元，收益率{}%'.format(round(total_spent, 2), round(total_profit, 2), TA.get_profit_percentage(total_profit, total_spent)))








