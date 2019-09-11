from PyQt5.QtWidgets import QMainWindow
from QtDesign.StockFinder_ui import Ui_StockFinder


class StockFinder(QMainWindow, Ui_StockFinder):

    def __init__(self):
        super().__init__()
        self.setupUi(self)