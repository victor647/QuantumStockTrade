from Data.StockData import *


class DataManager:
    stockDatabase = []
    marketDatabase = []

    @staticmethod
    def parse_daily_data(data_list, database):
        for data in data_list:
            stock_data = StockData()
            stock_data.date = data[0]
            stock_data.open = round(float(data[1]), 2)
            stock_data.high = round(float(data[2]), 2)
            stock_data.low = round(float(data[3]), 2)
            stock_data.close = round(float(data[4]), 2)
            stock_data.previousClose = round(float(data[5]), 2)
            stock_data.turn = round(float(data[6]), 2) if data[6] != "" else 0
            database.append(stock_data)

    @staticmethod
    def get_average_price(database, price_period, volume_period):
        for i in range(len(database) - 1, -1, -1):
            count = total = 0
            for j in range(0, 5):
                if i - j >= 0:
                    total += database[i - j].close
                    count += 1
                else:
                    break
            database[i].averagePriceFive = round(total / count, 2)

            count = total = 0
            for j in range(0, price_period):
                if i - j >= 0:
                    total += database[i - j].close
                    count += 1
                else:
                    break
            database[i].averagePriceLong = round(total / count, 2)

            count = total = 0
            for j in range(0, volume_period):
                if i - j >= 0:
                    total += database[i - j].turn
                    count += 1
                else:
                    break
            database[i].averageTurn = round(total / count, 2)

    @staticmethod
    def parse_minute_data(data_list, database):
        for data in data_list:
            stock_data = StockData()
            stock_data.time = data[0]
            stock_data.high = round(float(data[1]), 2)
            stock_data.low = round(float(data[2]), 2)
            database.append(stock_data)

    @staticmethod
    def parse_time(time):
        if len(time) < 15:
            return str(time)
        year = time[2:4]
        month = time[4:6]
        day = time[6:8]
        hour = time[8:10]
        minute = time[10:12]
        return year + "/" + month + "/" + day + " " + hour + ":" + minute

    @staticmethod
    def init():
        DataManager.stockDatabase = []
        DataManager.marketDatabase = []

    def bias_from_market(self, index):
        stock_data = self.stockDatabase[index]
        market_data = self.marketDatabase[index]
        return stock_data.close_percentage() - market_data.close_percentage()

    @staticmethod
    def win_market_probability():
        total = len(DataManager.stockDatabase)
        count = 0
        for i in range(total):
            if DataManager.stockDatabase[i].close_percentage() > DataManager.marketDatabase[i].close_percentage():
                count += 1
        return round(count / total * 100, 2)

    @staticmethod
    def off_market_point():
        days = len(DataManager.stockDatabase)
        total = 0
        for i in range(days):
            total += DataManager.stockDatabase[i].close_percentage() - DataManager.marketDatabase[i].close_percentage()
        return round(total / days * 100, 2)

    @staticmethod
    def inverse_market_up_probability():
        total = len(DataManager.stockDatabase)
        count = 0
        for i in range(total):
            if DataManager.stockDatabase[i].up_from_last() and not DataManager.marketDatabase[i].up_from_last():
                count += 1
        return round(count / total * 100, 2)

    @staticmethod
    def inverse_market_down_probability():
        total = len(DataManager.stockDatabase)
        count = 0
        for i in range(total):
            if not DataManager.stockDatabase[i].up_from_last() and DataManager.marketDatabase[i].up_from_last():
                count += 1
        return round(count / total * 100, 2)

    @classmethod
    def average_high(cls):
        total = 0
        for data in cls.stockDatabase:
            total += data.high_percentage()
        return round(total / len(cls.stockDatabase), 2)

    @classmethod
    def average_high_when_up(cls):
        total = 0
        count = 0
        for data in cls.stockDatabase:
            if data.up_from_last():
                total += data.high_percentage()
                count += 1
        return round(total / count, 2)

    @classmethod
    def average_low(cls):
        total = 0
        for data in cls.stockDatabase:
            total += data.low_percentage()
        return round(total / len(cls.stockDatabase), 2)

    @classmethod
    def average_low_when_down(cls):
        total = 0
        count = 0
        for data in cls.stockDatabase:
            if not data.up_from_last():
                total += data.low_percentage()
                count += 1
        return round(total / count, 2)

    @classmethod
    def average_full_amplitude(cls):
        total = 0
        for data in cls.stockDatabase:
            total += data.full_amplitude()
        return round(total / len(cls.stockDatabase), 2)

    @classmethod
    def average_close_up(cls):
        total = 0
        count = 0
        for data in cls.stockDatabase:
            if data.up_from_last():
                total += data.close_percentage()
                count += 1
        return round(total / count, 2)

    @classmethod
    def average_close_down(cls):
        total = 0
        count = 0
        for data in cls.stockDatabase:
            if not data.up_from_last():
                total += data.close_percentage()
                count += 1
        return round(total / count, 2)

    @classmethod
    def average_fallback(cls):
        total = 0
        count = 0
        for data in cls.stockDatabase:
            if data.up_from_last():
                total += data.fallback_amplitude()
                count += 1
        return round(total / count, 2)

    @classmethod
    def average_bounce(cls):
        total = 0
        count = 0
        for data in cls.stockDatabase:
            if not data.up_from_last():
                total += data.bounce_amplitude()
                count += 1
        return round(total / count, 2)

    @classmethod
    def average_turn(cls):
        total = 0
        for data in cls.stockDatabase:
            total += data.turn
        return round(total / len(cls.stockDatabase), 2)

    @classmethod
    def reach_max_probability(cls):
        count = 0
        for data in cls.stockDatabase:
            if data.reach_max_limit():
                count += 1
        return round(count / len(cls.stockDatabase) * 100, 2)

    @classmethod
    def reach_min_probability(cls):
        count = 0
        for data in cls.stockDatabase:
            if data.reach_min_limit():
                count += 1
        return round(count / len(cls.stockDatabase) * 100, 2)

    @classmethod
    def stay_max_probability(cls):
        count = 0
        for data in cls.stockDatabase:
            if data.stay_max_limit():
                count += 1
        return round(count / len(cls.stockDatabase) * 100, 2)

    @classmethod
    def stay_min_probability(cls):
        count = 0
        for data in cls.stockDatabase:
            if data.stay_min_limit():
                count += 1
        return round(count / len(cls.stockDatabase) * 100, 2)

    @staticmethod
    def interval_up_probability(database):
        total = 0
        for data in database:
            if data.up_from_last():
                total += 1
        return round(total / len(database) * 100, 2)

    @staticmethod
    def interval_open_price(database):
        return database[0].open

    @staticmethod
    def interval_close_price(database):
        return database[-1].close

    @staticmethod
    def interval_highest_price(database):
        high = database[0].high
        for data in database:
            high = max(high, data.high)
        return high

    @staticmethod
    def interval_lowest_price(database):
        low = database[0].low
        for data in database:
            low = min(low, data.low)
        return low

    @staticmethod
    def interval_average_price(database):
        total = 0
        for data in database:
            total += data.close
        return round(total / len(database), 2)

    @staticmethod
    def interval_total_performance(database):
        return round((DataManager.interval_close_price(database) / DataManager.interval_open_price(database) - 1) * 100, 2)

    @staticmethod
    def interval_average_performance(database):
        return round(DataManager.interval_total_performance(database) / len(database), 2)
