import math
import pandas as pd
import numpy as np
import akshare as ak
from datetime import datetime, timedelta
import argparse
from pattern_recognition import calculate_overlap_for_tech

def run_kline_analysis():
    # 创建ArgumentParser对象
    parser = argparse.ArgumentParser(description="user input")

    # 添加参数
    # parser.add_argument("positional_arg", help="位置参数")
    # print(f"位置参数: {args.positional_arg}")
    parser.add_argument("--datedelta", "-o", type=int, default=16, help="日期范围范围")
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

    res = calculate_overlap_for_tech(open_a_hist, high_a_hist, low_a_hist, close_a_hist)
    print(res)
    print(stock_zh_a_hist_df)

if __name__ == '__main__':
    run_kline_analysis()
