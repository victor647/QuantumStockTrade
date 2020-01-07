from QtDesign.TradeSettings_ui import Ui_TradeSettings
from PyQt5.QtWidgets import QDialog

brokerFeePercentage = 0.00018
stampDuty = 0.001
minBrokerFee = 5


# 交易费用设置
class TradeSettings(QDialog, Ui_TradeSettings):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    # 保存设置
    def save_settings(self):
        global brokerFeePercentage, stampDuty, minBrokerFee
        brokerFeePercentage = self.spbBrokerFeePercentage.value() / 10000
        minBrokerFee = self.spbMinBrokerFee.value()
        stampDuty = self.spbStampDuty.value() / 1000
        self.close()

