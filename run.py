import math
import pandas as pd
import numpy as np
import akshare as ak
from datetime import datetime, timedelta
import argparse
from pattern_recognition import pattern_match
from cycle_indicators import cycle_indicators_calculations
from volatility_indicators import calculate_volatility_indicators
from price_transform import calculate_price
from momentum_indicators import calculate_momentum_indicators
from volume_indicators import calculate_volume_indicators
from overlap_studies import calculate_overlap


def run_kline_analysis():
    # 创建ArgumentParser对象
    parser = argparse.ArgumentParser(description="user input")

    # 添加参数
    # parser.add_argument("positional_arg", help="位置参数")
    # print(f"位置参数: {args.positional_arg}")
    parser.add_argument("--datedelta", "-o", type=int, default=32, help="日期范围范围")#default to ensue below judgement can get not NaN value
    # 解析参数
    args = parser.parse_args()

    today = datetime.now()
    start_day = today - timedelta(days=args.datedelta)
    
    # 格式化日期为YYYYMMDD格式
    formatted_today = today.strftime('%Y%m%d')
    formatted_start_day = start_day.strftime('%Y%m%d')

    stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date=formatted_start_day, end_date=formatted_today, adjust="")
    open_a_hist = stock_zh_a_hist_df["开盘"]
    close_a_hist = stock_zh_a_hist_df["收盘"]
    high_a_hist = stock_zh_a_hist_df["最高"]
    low_a_hist = stock_zh_a_hist_df["最低"]
    volume_a_hist = stock_zh_a_hist_df["成交量"]
    
    with open('results.txt', 'a', encoding='utf-8') as output_file:
        output_file.write("sth")

    # buy_count,sell_count = calculate_overlap(high_a_hist, low_a_hist, close_a_hist)
    # print(buy_count,sell_count)

    # neg_count, pos_count = pattern_match(open_a_hist, high_a_hist, low_a_hist, close_a_hist)
    # print(neg_count,pos_count)

    calculate_momentum_indicators(open_a_hist, high_a_hist, low_a_hist, close_a_hist, volume_a_hist)

    # turnaround_count, consistency_count = calculate_volume_indicators(volume_a_hist, high_a_hist, low_a_hist, close_a_hist)#max = 3
    # print(turnaround_count, consistency_count)

    # print(stock_zh_a_hist_df)

    # unstable and hard to use, tested with data generated bad res, abandoned
    # res = cycle_indicators_calculations(np.arange(100, dtype=np.float64))
    # res = cycle_indicators_calculations(np.array([0.0 if i % 2 == 0 else 1.0 for i in range(100)]))
    # res = cycle_indicators_calculations(np.array([np.sin(np.pi * i/2)+1 for i in range(100)]))

    # at this moment, seems natr is enough for volatility judgement
    # natr = calculate_volatility_indicators(high_a_hist, low_a_hist, close_a_hist)#higher, the greater risk
    # weighted_close_prices = calculate_price(open_a_hist, high_a_hist, low_a_hist, close_a_hist) #judge price trend
    # print("The Natr values are:")
    # # print(natr)
    # print("The weighted_close_prices are:")
    # print(weighted_close_prices)
    

if __name__ == '__main__':
    run_kline_analysis()
