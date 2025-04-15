from PyQt6.QtWidgets import QTableWidgetItem


class CustomSortingTableData(QTableWidgetItem):

    customData = 0.0

    def set_sorting_data(self, value: float):
        self.customData = value

    def __lt__(self, other):
        return self.customData < other.customData

    def __gt__(self, other):
        return self.customData > other.customData

    def __le__(self, other):
        return self.customData <= other.customData

    def __ge__(self, other):
        return self.customData >= other.customData

    def __eq__(self, other):
        return self.customData == other.customData
