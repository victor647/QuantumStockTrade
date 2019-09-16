from QtDesign.ProgressBar_ui import Ui_ProgressBar
from PyQt5.QtWidgets import QDialog


class ProgressBar(QDialog, Ui_ProgressBar):

    def __init__(self, total):
        super().__init__()
        self.setupUi(self)
        self.total = total

    def update_search_progress(self, index, code, name):
        # 更新进度条显示
        self.pgbSearching.setValue(index / self.total * 100)
        # 更新底部文字显示
        self.lblCurrentWorking.setText(code + name + "(" + str(index) + "/" + str(self.total) + ")")

    def finish_progress(self):
        self.close()
