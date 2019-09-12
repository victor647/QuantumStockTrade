def get_trade_center(stock_code):
    code = int(stock_code)
    market = ""
    # 深圳主板
    if 0 < code < 100000:
        market = "sz"
    # 创业板
    elif 300000 < code < 400000:
        market = "sz"
    # 上海主板
    elif 600000 < code < 700000:
        market = "sh"
    # 深圳可转债
    elif 128000 <= code <= 129000:
        market = "sz"
    # 上海可转债
    elif 113500 <= code <= 113600:
        market = "sh"
    return market
