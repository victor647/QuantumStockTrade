from PyQt5.QtGui import QColor


class StockData:
    date = None
    time = None
    high = 0
    low = 0
    open = 0
    close = 0
    previousClose = 0
    turn = 0
    averagePriceFive = 0
    averagePriceLong = 0
    averageTurn = 0

    def full_amplitude(self):
        return round((self.high - self.low) / self.previousClose * 100, 2)

    def close_percentage(self):
        return round((self.close / self.previousClose - 1) * 100, 2)

    def high_percentage(self):
        return round((self.high / self.previousClose - 1) * 100, 2)

    def high_percentage_minute(self, pre_close):
        return round((self.high / pre_close - 1) * 100, 2)

    def low_percentage(self):
        return round((self.low / self.previousClose - 1) * 100, 2)

    def low_percentage_minute(self, pre_close):
        return round((self.low / pre_close - 1) * 100, 2)

    def up_from_last(self):
        return self.close > self.previousClose

    def low_open_high_end(self):
        return self.open < self.previousClose and self.close > self.open

    def low_open_low_end(self):
        return self.previousClose > self.open > self.close

    def high_open_low_end(self):
        return self.open > self.previousClose and self.close < self.open

    def high_open_high_end(self):
        return self.previousClose < self.open < self.close

    def reach_max_limit(self):
        return self.high / self.previousClose < 1.1 < (self.high + 0.01) / self.previousClose

    def reach_min_limit(self):
        return (self.low - 0.01) / self.previousClose < 0.9 < self.low / self.previousClose

    def stay_max_limit(self):
        return self.close / self.previousClose < 1.1 < (self.close + 0.01) / self.previousClose

    def stay_min_limit(self):
        return (self.close - 0.01) / self.previousClose < 0.9 < self.close / self.previousClose

    def get_text_color(self, price):
        if price > self.previousClose:
            return QColor(200, 0, 0)
        if price < self.previousClose:
            return QColor(0, 128, 0)
        return QColor(0, 0, 0)

    def fallback_amplitude(self):
        return self.high_percentage() - self.close_percentage()

    def bounce_amplitude(self):
        return self.close_percentage() - self.low_percentage()

    def price_at_percentage(self, percentage):
        return round(self.previousClose * (1 + percentage / 100), 2)

    def percentage_at_price(self, price):
        return round((price / self.previousClose - 1) * 100, 2)
