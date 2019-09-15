from QtDesign.StockReviewer_ui import Ui_StockReviewer
from PyQt5.QtWidgets import QMainWindow


class StockReviewer(QMainWindow, Ui_StockReviewer):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
