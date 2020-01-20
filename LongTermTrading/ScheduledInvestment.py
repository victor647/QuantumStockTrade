from QtDesign.ScheduledInvestment_ui import Ui_ScheduledInvestment
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QFileDialog
from PyQt5.QtCore import Qt
from Tools import Tools, FileManager


# 定投组合模拟
class ScheduledInvestment(QMainWindow, Ui_ScheduledInvestment):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

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

    # 移除一只股票
    def remove_stock_code(self):
        selection = self.tblStockList.selectedIndexes()
        if len(selection) == 0:
            return
        index = selection[0].row()
        self.tblStockList.removeRow(index)

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
        start_date = self.dteStartDate.date().toString()

