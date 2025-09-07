#! /usr/bin/env python3
# -*- coding=utf-8 -*-
import akshare as ak
import pandas as pd
import requests
import os
import csv
import time
from datetime import datetime
from dateutil.parser import parse
from tqdm import tqdm

def is_trading_day():
    """判断是否为交易日"""
    try:
        # 获取交易日历
        today = datetime.now().strftime("%Y%m%d")
        trade_cal = ak.tool_trade_date_hist_sina()
        # 判断今天是否在交易日列表中
        trade_dates = pd.to_datetime(trade_cal['trade_date']).dt.strftime("%Y%m%d")
        return today in trade_dates.values
    except:
        # 如果获取失败，通过星期判断（简单判断，周一到周五为交易日）
        weekday = datetime.now().weekday()
        return weekday < 5  # 0-4 表示周一到周五


def get_active_stocks_today():
    """获取当日非停牌的A股股票列表"""
    today_str = datetime.today().strftime("%Y%m%d")
    try:
        stock_all_df = ak.stock_zh_a_spot_em()[['代码', '名称']]
    except Exception as e:
        print(f"获取股票列表失败: {e}")
        return pd.DataFrame()

    try:
        suspend_df = ak.news_trade_notify_suspend_baidu(date=today_str)
        suspended_codes = suspend_df[suspend_df['复牌时间'].isna()]['股票代码'].tolist()
        stock_active_df = stock_all_df[~stock_all_df['代码'].isin(suspended_codes)]
    except:
        print(f"停复牌数据获取失败，使用全部股票")
        stock_active_df = stock_all_df

    return stock_active_df.reset_index(drop=True)


def stock_zh_a_hist_with_proxy(symbol, start_date="19700101", end_date="20500101", proxy=None):
    """获取股票历史数据"""
    market_code = 1 if symbol.startswith("6") else 0
    url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
    params = {
        "fields1": "f1,f2,f3,f4,f5,f6",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f116",
        "ut": "fa5fd1943c7b386f172d6893dbfba10b",
        "klt": "101",  # 日线
        "fqt": "1",  # 前复权
        "secid": f"{market_code}.{symbol}",
        "beg": start_date,
        "end": end_date,
    }

    try:
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4295.400'

        headers = {'User-Agent': user_agent}
        r = requests.get(url, headers=headers, params=params, timeout=5, proxies=proxy)
        data_json = r.json()

        if not (data_json.get("data") and data_json["data"].get("klines")):
            return pd.DataFrame()

        temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]["klines"]])
        temp_df.columns = ["日期", "开盘", "收盘", "最高", "最低", "成交量", "成交额",
                           "振幅", "涨跌幅", "涨跌额", "换手率"]

        temp_df["日期"] = pd.to_datetime(temp_df["日期"]).dt.date
        temp_df["股票代码"] = symbol

        # 转换数值类型
        numeric_cols = ["开盘", "收盘", "最高", "最低", "成交量", "成交额",
                        "振幅", "涨跌幅", "涨跌额", "换手率"]
        temp_df[numeric_cols] = temp_df[numeric_cols].apply(pd.to_numeric)

        return temp_df[["日期", "股票代码", "开盘", "收盘", "最高", "最低",
                        "成交量", "成交额", "振幅", "涨跌幅", "涨跌额", "换手率"]]
    except Exception as e:
        return pd.DataFrame()


def update_stock_data(code, data_dir, proxy=None):
    """更新单只股票数据"""
    csv_file = os.path.join(data_dir, f"{code}.csv")

    # 确定起始日期
    start_date = "20050101"
    if os.path.exists(csv_file):
        try:
            existing_df = pd.read_csv(csv_file, encoding="utf-8")
            if not existing_df.empty:
                last_date = pd.to_datetime(existing_df.iloc[-1]['日期'])
                start_date = last_date.strftime("%Y%m%d")
        except:
            pass

    # 获取股票代码（去除市场前缀）
    symbol = code[2:] if code.startswith(('sh', 'sz')) else code

    # 获取数据
    new_data = stock_zh_a_hist_with_proxy(symbol, start_date, proxy=proxy)
    if new_data.empty:
        return False

    # 保存数据
    try:
        if os.path.exists(csv_file):
            # 追加模式
            existing_df = pd.read_csv(csv_file, encoding="utf-8")
            combined_df = pd.concat([existing_df, new_data], ignore_index=True)
            # 去重，保留最新的
            combined_df = combined_df.drop_duplicates(subset=['日期'], keep='last')
            combined_df.to_csv(csv_file, index=False, encoding="utf-8")
        else:
            # 新文件
            new_data.to_csv(csv_file, index=False, encoding="utf-8")
        return True
    except Exception as e:
        print(f"保存{code}数据失败: {e}")
        return False


def main(proxy_api_url, use_proxy = True, max_proxy_switches = 10):
    """主函数"""
    # 配置参数
    data_dir = "./stock_data"  # 数据保存目录
    temp_dir = "./temp"  # 临时文件目录

    # 创建目录
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(temp_dir, exist_ok=True)

    # 检查是否交易日
    if not is_trading_day():
        print("今天不是交易日，程序退出")
        return

    print("开始获取股票列表...")
    stocks_df = get_active_stocks_today()
    if stocks_df.empty:
        print("获取股票列表失败")
        return

    # 生成股票代码列表（加上市场前缀）
    stock_codes = []
    for code in stocks_df['代码']:
        if code.startswith('6'):
            stock_codes.append('sh' + code)
        else:
            stock_codes.append('sz' + code)

    print(f"共获取到 {len(stock_codes)} 只开盘股票")

    # 读取已完成记录
    today_str = datetime.now().strftime('%Y-%m-%d')
    completed_file = os.path.join(temp_dir, f"completed_{today_str}.csv")
    completed_codes = set()

    if os.path.exists(completed_file):
        try:
            with open(completed_file, 'r') as f:
                reader = csv.reader(f)
                completed_codes = {row[0] for row in reader if row}
        except:
            pass

    # 待更新股票
    remaining_codes = [code for code in stock_codes if code not in completed_codes]
    print(f"已完成: {len(completed_codes)}, 待更新: {len(remaining_codes)}")

    if not remaining_codes:
        print("所有股票已更新完成")
        return

    # 初始化代理IP
    proxy_manager = ProxyManager(proxy_api_url) if use_proxy else None
    current_proxy = None
    proxy_switches = 0
    success_count = 0
    fail_count = 0
    consecutive_fails = 0

    # 进度条
    pbar = tqdm(total=len(remaining_codes), desc='更新进度')

    # 主循环
    i = 0
    while i < len(remaining_codes):
        code = remaining_codes[i]

        # 检查是否需要切换代理
        if use_proxy and (current_proxy is None or consecutive_fails >= 3):
            if proxy_switches >= max_proxy_switches:
                print("\n达到最大代理切换次数，使用直连模式")
                use_proxy = False
                current_proxy = None
            else:
                current_proxy = proxy_manager.get_valid_proxy()
                if current_proxy:
                    proxy_switches += 1
                    consecutive_fails = 0
                else:
                    print("\n无法获取代理，使用直连模式")
                    use_proxy = False

        # 更新数据
        success = update_stock_data(code, data_dir, current_proxy)

        if success:
            success_count += 1
            consecutive_fails = 0
            # 记录完成
            with open(completed_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([code])
            pbar.update(1)
            i += 1
        else:
            fail_count += 1
            consecutive_fails += 1

            # 如果不是代理问题，跳过该股票
            if consecutive_fails < 3 or not use_proxy:
                i += 1
                pbar.update(1)

        time.sleep(0.1)  # 简单延时

    pbar.close()

    # 输出统计
    print(f"\n更新完成!")
    print(f"成功: {success_count}")
    print(f"失败: {fail_count}")
    print(f"代理切换: {proxy_switches} 次")


if __name__ == '__main__':
    start_time = time.time()
    proxy_api_url = 'XXXX'
    main(proxy_api_url=proxy_api_url, use_proxy=True, max_proxy_switches=10)
    elapsed = int(time.time() - start_time)
    print(f"\n总用时: {elapsed // 60}分{elapsed % 60}秒")
