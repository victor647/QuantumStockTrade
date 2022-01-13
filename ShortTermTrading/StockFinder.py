from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QListWidgetItem
from PyQt5.QtGui import QKeyEvent
from QtDesign.StockFinder_ui import Ui_StockFinder
from ShortTermTrading.SearchResult import SearchResult
from ShortTermTrading.BatchSearcher import BatchSearcher
from ShortTermTrading.FiveDayFinder import FiveDayFinder
from ShortTermTrading.StockSearchThread import StandardStockSearcher
from datetime import datetime
import ShortTermTrading.SearchCriteria as SearchCriteria
import pandas
from Tools import Tools, FileManager
import Data.TechnicalAnalysis as TA


Instance = None


class StockFinder(QMainWindow, Ui_StockFinder):
    __searchResult = None
    __criteriaItems = []

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 初始化单例
        global Instance
        Instance = self
        self.setup_triggers()
        # 初始化选股日期
        self.dteSearchDate.setDate(QDate.currentDate())
        # 初始化技术面指标下拉菜单
        self.cbbMACDBehaviour.addItems(['金叉', '翻红', '绿柱缩短'])
        self.cbbBOLLBehaviour.addItems(['上穿', '下穿'])
        self.cbbBOLLTrack.addItems(['上轨', '中轨', '下轨'])
        self.cbbSpecialShape.addItems(['对数底', '金针探底', '揉搓线', '仙人指路', '早晨之星'])

    def setup_triggers(self):
        self.btnStartSearch.clicked.connect(self.start_searching)
        self.btnAutoSearch.clicked.connect(self.run_batch_searcher)
        self.btnExportBasicConfig.clicked.connect(self.export_basic_config)
        self.btnImportBasicConfig.clicked.connect(self.import_basic_config)
        self.btnExportTechnicalConfig.clicked.connect(self.export_technical_config)
        self.btnImportTechnicalConfig.clicked.connect(self.import_technical_config)
        self.btnExportCustomConfig.clicked.connect(self.export_custom_config)
        self.btnImportCustomConfig.clicked.connect(self.import_custom_config)
        self.btnAddCriteria.clicked.connect(self.add_criteria_item)
        self.btnEditCriteria.clicked.connect(self.edit_selected_item)
        self.btnRemoveCriteria.clicked.connect(self.remove_criteria_item)
        self.btnResetCriteria.clicked.connect(self.reset_criteria_items)
        self.lstCriteriaItems.itemDoubleClicked.connect(self.edit_selected_item)
        self.cbxPE.toggled.connect(self.spbPEMax.setEnabled)
        self.cbxPB.toggled.connect(self.spbPBMax.setEnabled)
        self.cbxPS.toggled.connect(self.spbPSMax.setEnabled)
        self.cbxMACD.toggled.connect(self.spbPEMax.setEnabled)
        self.cbxSpecialShape.toggled.connect(self.cbbSpecialShape.setEnabled)

    # 快捷键设置
    def keyPressEvent(self, key: QKeyEvent):
        # Esc键清除选择
        if key.key() == Qt.Key_Escape:
            self.lstCriteriaItems.clearSelection()
        # 按删除键删除股票或指标组
        elif key.key() == Qt.Key_Delete or key.key() == Qt.Key_Backspace:
            self.remove_criteria_item()

    # 打开批量自动选股器
    @staticmethod
    def run_batch_searcher():
        batch_searcher = BatchSearcher()
        batch_searcher.show()
        batch_searcher.exec_()

    # 保存基本面指标搜索条件
    def export_basic_config(self):
        file_path = QFileDialog.getSaveFileName(directory=FileManager.search_config_path(), filter='JSON(*.json)')
        data = {
            'peOn': self.cbxPE.isChecked(),
            'peMax': self.spbPEMax.value(),
            'pbOn': self.cbxPB.isChecked(),
            'pbMax': self.spbPBMax.value(),
            'psOn': self.cbxPS.isChecked(),
            'psMax': self.spbPSMax.value(),
            'includeSt': self.cbxIncludeST.isChecked()
        }
        if file_path[0] != '':
            FileManager.export_config_as_json(data, file_path[0])

    # 载入基本面指标搜索条件
    def import_basic_config(self):
        file_path = QFileDialog.getOpenFileName(directory=FileManager.search_config_path(), filter='JSON(*.json)')
        if file_path[0] != '':
            data = FileManager.import_json_config(file_path[0])
            if 'peOn' not in data:
                Tools.show_error_dialog('选取的配置文件格式不对！')
                return
            self.cbxPE.setChecked(data['peOn'])
            self.spbPEMax.setValue(data['peMax'])
            self.cbxPB.setChecked(data['pbOn'])
            self.spbPBMax.setValue(data['pbMax'])
            self.cbxPS.setChecked(data['psOn'])
            self.spbPSMax.setValue(data['psMax'])
            self.cbxIncludeST.setChecked(data['includeSt'])

    # 保存技术面指标搜索条件
    def export_technical_config(self):
        file_path = QFileDialog.getSaveFileName(directory=FileManager.search_config_path(), filter='JSON(*.json)')
        data = {
            'timePeriod': self.spbTechnicalTimePeriod.value(),
            'macdOn': self.cbxMACD.isChecked(),
            'macdBehaviour': self.cbbMACDBehaviour.currentText(),
            'bollOn': self.cbxBOLL.isChecked(),
            'bollBehaviour': self.cbbBOLLBehaviour.currentText(),
            'bollTrack': self.cbbBOLLTrack.currentText(),
            'maOn': self.cbxMA.isChecked(),
            'maShort': self.spbMaShort.value(),
            'maLong': self.spbMaLong.value(),
            'specialOn': self.cbxSpecialShape.isChecked(),
            'specialShape': self.cbbSpecialShape.currentText()
        }
        if file_path[0] != '':
            FileManager.export_config_as_json(data, file_path[0])

    # 载入技术面指标搜索条件
    def import_technical_config(self):
        file_path = QFileDialog.getOpenFileName(directory=FileManager.search_config_path(), filter='JSON(*.json)')
        if file_path[0] != '':
            data = FileManager.import_json_config(file_path[0])
            if 'timePeriod' not in data:
                Tools.show_error_dialog('选取的配置文件格式不对！')
                return
            self.spbTechnicalTimePeriod.setValue(data['timePeriod'])
            self.cbxMACD.setChecked(data['macdOn'])
            self.cbbMACDBehaviour.setCurrentText(data['macdBehaviour'])
            self.cbxBOLL.setChecked(data['bollOn'])
            self.cbbBOLLBehaviour.setCurrentText(data['bollBehaviour'])
            self.cbbBOLLTrack.setCurrentText(data['bollTrack'])
            self.cbxMA.setChecked(data['maOn'])
            self.spbMaShort.setValue(data['maShort'])
            self.spbMaLong.setValue(data['maLong'])
            self.cbxSpecialShape.setChecked(data['specialOn'])
            self.cbbSpecialShape.setCurrentText(data['specialShape'])

    # 保存自定义指标搜索条件
    def export_custom_config(self):
        file_path = QFileDialog.getSaveFileName(directory=FileManager.search_config_path(), filter='JSON(*.json)')
        if file_path[0] != '':
            FileManager.export_config_as_json(self.__criteriaItems, file_path[0])

    # 载入自定义指标搜索条件
    def import_custom_config(self):
        file_path = QFileDialog.getOpenFileName(directory=FileManager.search_config_path(), filter='JSON(*.json)')
        if file_path[0] != '':
            self.__criteriaItems = FileManager.import_json_config(file_path[0], SearchCriteria.CriteriaItem.import_criteria_item)
            self.update_criteria_list()

    # 更新自定义搜索条件列表显示
    def update_criteria_list(self, edited_item=None):
        # 添加条件时
        if edited_item is not None and edited_item not in self.__criteriaItems:
            self.__criteriaItems.append(edited_item)
        # 重新生成图表
        self.lstCriteriaItems.clear()
        for item in self.__criteriaItems:
            self.lstCriteriaItems.addItem(item.to_display_text())

    # 新增自定义搜索条件
    @staticmethod
    def add_criteria_item():
        item = SearchCriteria.CriteriaItem()
        window = SearchCriteria.SearchCriteria(item)
        window.show()
        window.exec()

    # 双击编辑所选自定义搜索条件
    def edit_selected_item(self, item: QListWidgetItem):
        index = self.lstCriteriaItems.indexFromItem(item)
        window = SearchCriteria.SearchCriteria(self.__criteriaItems[index.row()])
        window.show()
        window.exec()

    # 点击编辑按钮编辑所选自定义搜索条件
    def modify_criteria_item(self):
        selection = self.lstCriteriaItems.selectedIndexes()
        if len(selection) == 0:
            return
        index = selection[0].row()
        item = self.__criteriaItems[index]
        window = SearchCriteria.SearchCriteria(item)
        window.show()
        window.exec()

    # 删除所选自定义搜索条件
    def remove_criteria_item(self):
        selection = self.lstCriteriaItems.selectedIndexes()
        if len(selection) == 0:
            return
        index = selection[0].row()
        self.__criteriaItems.pop(index)
        self.lstCriteriaItems.takeItem(index)

    # 清空自定义搜索条件
    def reset_criteria_items(self):
        self.__criteriaItems = []
        self.lstCriteriaItems.clear()

    # 开始搜索全部股票
    def start_searching(self):
        # 确保选股日期不是周末
        search_date = Tools.get_nearest_trade_date(self.dteSearchDate.date()).toString('yyyy-MM-dd')
        # 弹出搜索结果界面
        self.__searchResult = SearchResult(search_date)
        self.__searchResult.show()
        # 开始选股线程
        search_process = StandardStockSearcher(search_date, False)
        search_process.addItemCallback.connect(self.__searchResult.add_stock_item)
        search_process.start()

    # 批量选股器自动选股接口
    @staticmethod
    def auto_search(searcher: BatchSearcher, start_date: QDate, end_date: QDate):
        current_searching_date = start_date
        # 初始化选股结果列表
        while current_searching_date < end_date:
            # 确保选股日期不是周末
            current_searching_date = Tools.get_nearest_trade_date(current_searching_date)
            date_string = current_searching_date.toString('yyyy-MM-dd')
            # 开始选股进程
            search_process = StandardStockSearcher(date_string, True, searcher.iptCriteriaName.text())
            search_process.start()
            current_searching_date = searcher.move_to_next_date(current_searching_date)

    # 基本面指标分析
    def match_basic_criterias(self, data: pandas.DataFrame):
        # 检测股票是否是ST股
        if not self.cbxIncludeST.isChecked():
            if data['isST'] == 1:
                return False

        # 检测股票市盈率是否符合范围
        if self.cbxPE.isChecked():
            pe = data['peTTM']
            if pe < 0 or pe > self.spbPEMax.value():
                return False

        # 检测股票市净率是否符合范围
        if self.cbxPB.isChecked():
            pb = data['pbMRQ']
            if pb < 0 or pb > self.spbPBMax.value():
                return False

        # 检测股票市销率是否符合范围
        if self.cbxPS.isChecked():
            ps = data['psTTM']
            if ps < 0 or ps > self.spbPSMax.value():
                return False

        # 所有指标全部达标
        return True

    # 自定义指标分析
    def match_custom_criterias(self, data: pandas.DataFrame):
        # 若没有自定义指标则跳过
        if len(self.__criteriaItems) == 0:
            return True
        # 跳过还未上市新股
        if data.empty:
            return False
        # 跳过当日停牌股票
        if data.iloc[-1]['tradestatus'] == 0:
            return False

        # 逐条筛选自定义指标
        for item in self.__criteriaItems:
            if not SearchCriteria.match_criteria_item(data, item):
                return False
        return True

    # 技术指标分析
    def match_technical_criterias(self, data: pandas.DataFrame):
        # 跳过上市一个月内的新股
        if data.shape[0] < 20:
            return False
        period = self.spbTechnicalTimePeriod.value() + 1
        # 检测MACD图形
        if self.cbxMACD.isChecked() and not TA.match_macd(data, period, self.cbbMACDBehaviour.currentText()):
            return False
        # 检测BOLL区间
        if self.cbxBOLL.isChecked() and not TA.match_boll(data, period, self.cbbBOLLTrack.currentText(), self.cbbBOLLBehaviour.currentText()):
            return False
        # 检测均线交叉
        if self.cbxMA.isChecked() and not TA.match_ma(data, period, self.spbMaShort.value(), self.spbMaLong.value()):
            return False
        # 检测特殊图形
        if self.cbxSpecialShape.isChecked() and not TA.match_special_shape(data, self.spbTechnicalTimePeriod.value(), self.cbbSpecialShape.currentText()):
            return False
        return True

    # 检测股票是否在所选交易所中
    def code_in_search_range(self, code: int):
        # 上海主板
        if self.cbxShanghaiMain.isChecked() and 600000 <= code < 688000:
            return True
        # 深圳主板
        if self.cbxShenZhenMain.isChecked() and 0 <= code < 2000:
            return True
        # 中小板
        if self.cbxShenZhenSmall.isChecked() and 2000 <= code < 3000:
            return True
        # 创业板
        if self.cbxShenZhenNew.isChecked() and 300000 <= code < 301000:
            return True
        # 科创板
        if self.cbxShanghaiScience.isChecked() and 688000 <= code < 689000:
            return True
        return False
