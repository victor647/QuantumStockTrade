from QtDesign.ProgressBar_ui import Ui_ProgressBar
from PyQt5.QtWidgets import QDialog, QMessageBox


class ProgressBar(QDialog, Ui_ProgressBar):

    def __init__(self, total):
        super().__init__()
        self.setupUi(self)
        self.total = total

    def update_search_progress(self, index, code, name):
        if index == self.total:
            message = QMessageBox()
            message.setWindowTitle("成功")
            message.setText("已获得所有股票最新数据！")
            message.show()
            self.close()
        self.pgbSearching.setValue(index / self.total * 100)
        self.lblCurrentWorking.setText(code + name + "(" + str(index) + "/" + str(self.total) + ")")
