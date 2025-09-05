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
from stock_collection import stock_classes
import multiprocessing
import threading
import queue
import psutil
import time
from stock_codes_reader import read_stock_data
from stock_codes_acquirer import acquire_stock_data
from concurrent.futures  import ThreadPoolExecutor

def run_kline_analysis(stock_zh_a_hist_df):
    open_a_hist = stock_zh_a_hist_df["开盘"]
    close_a_hist = stock_zh_a_hist_df["收盘"]
    high_a_hist = stock_zh_a_hist_df["最高"]
    low_a_hist = stock_zh_a_hist_df["最低"]
    volume_a_hist = stock_zh_a_hist_df["成交量"]

    buy_count,sell_count = calculate_overlap(high_a_hist, low_a_hist, close_a_hist)
    # print(buy_count,sell_count)

    neg_count, pos_count = pattern_match(open_a_hist, high_a_hist, low_a_hist, close_a_hist)
    # print(neg_count,pos_count)

    up_trend, weak_count, strong_count = calculate_momentum_indicators(open_a_hist, high_a_hist, low_a_hist, close_a_hist, volume_a_hist)

    # print(up_trend, weak_count, strong_count)

    turnaround_count, consistency_count = calculate_volume_indicators(volume_a_hist, high_a_hist, low_a_hist, close_a_hist)#max = 3
    # print(turnaround_count, consistency_count)

    # print(stock_zh_a_hist_df)

    # unstable and hard to use, tested with data generated bad res, abandoned
    # res = cycle_indicators_calculations(np.arange(100, dtype=np.float64))
    # res = cycle_indicators_calculations(np.array([0.0 if i % 2 == 0 else 1.0 for i in range(100)]))
    # res = cycle_indicators_calculations(np.array([np.sin(np.pi * i/2)+1 for i in range(100)]))

    # # at this moment, seems natr is enough for volatility judgement
    # natr = calculate_volatility_indicators(high_a_hist, low_a_hist, close_a_hist)#higher, the greater risk
    # weighted_close_prices = calculate_price(open_a_hist, high_a_hist, low_a_hist, close_a_hist) #judge price trend
    # print("The Natr values are:")
    # print(natr)
    # print("The weighted_close_prices are:")
    # print(weighted_close_prices)
    if buy_count > sell_count and pos_count > neg_count and up_trend > 0 and (turnaround_count + consistency_count) > 0:
        return True,[buy_count,sell_count,neg_count, pos_count,up_trend, weak_count, strong_count,turnaround_count, consistency_count]
    else:
        return False, None
    
def stock_data_getter(stock_codes, formatted_start_day, formatted_today, data_queue):
    for stock_code in stock_codes:
        stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=stock_code, period="daily", start_date=formatted_start_day, end_date=formatted_today, adjust="")
        if stock_zh_a_hist_df.empty:
            print("wrong code:",stock_code)
        else:
            data_queue.put((stock_code, stock_zh_a_hist_df))


def collect_and_analyze_data(stock_codes, one_cpu_length, formatted_start_day, formatted_today, lock):
    # threads = []
    data_queue = queue.Queue()

    chunked_list = [stock_codes[i:i + one_cpu_length] for i in range(0, len(stock_codes), one_cpu_length)]

    # # collect data
    # for i in chunked_list:
    #     t = threading.Thread(target=stock_data_getter, args=(i, formatted_start_day, formatted_today, data_queue))
    #     threads.append(t)
    #     t.start()
 
    # for t in threads:
    #     t.join(timeout=10)
 
    with ThreadPoolExecutor(max_workers=len(chunked_list)) as executor:
        futures = [
            executor.submit(stock_data_getter,  chunk, formatted_start_day, formatted_today, data_queue)
            for chunk in chunked_list
        ]
        for future in futures:
            try:
                future.result() 
            except Exception as e:
                print("Error in thread:", e)
    
    print("stock code:",stock_codes[0],"data collection finished:", time.time())
    res_ls = []
    while not data_queue.empty(): 
        try:
            stock_code, stock_data = data_queue.get_nowait()
            # data_queue.task_done()
            print("got code:",stock_code)
            suggested, res = run_kline_analysis(stock_data)
            if suggested:
                res_ls.append((stock_code, res))
        except Exception as e:
            print("the exception is:",e)
            print("stock code:",stock_codes[0],"data calculation finished:", time.time())
            with lock:
                with open('today_suggestions.txt', 'a', encoding='utf-8') as today_suggestions,open('history_suggestions.txt', 'a', encoding='utf-8') as history_suggestions:
                    for stock_code, result in res_ls:
                        [buy_count,sell_count,neg_count, pos_count,up_trend, weak_count, strong_count,turnaround_count, consistency_count] = result
                        today_suggestions.write(str(stock_code) + " ")
                        words = f"""
                        stock_code: {stock_code}
                        buy_count: {buy_count} sell_count: {sell_count} neg_count: {neg_count} pos_count: {pos_count}
                        up_trend: {up_trend} weak_count: {weak_count} strong_count: {strong_count}
                        turnaround_count: {turnaround_count} consistency_count: {consistency_count}
                        \n
                        """
                        sentence = " ".join(words)
                        history_suggestions.write(sentence)
            return

if __name__ == '__main__':
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

    with open('today_suggestions.txt', 'w', encoding='utf-8') as today_suggestions,open('history_suggestions.txt', 'a', encoding='utf-8') as history_suggestions:
        today_suggestions.write(formatted_today + "!!!!!!!!~~~~~~~~~~~~~~\n")
        history_suggestions.write(formatted_today + "!!!!!!!!!!!~~~~~~~~~~~~\n")
    lock = multiprocessing.Lock()
    total_len = 0
    physical_cpus = psutil.cpu_count(logical=False)#多核CPU：对于多核CPU，线程数可以设置为“CPU核心数 × (1 + I/O计算耗时 / CPU计算耗时)”,简便起见直接用cpu核心数
    for value_list in stock_classes.values():
        total_len += len(value_list)

    one_cpu_length = int(total_len/physical_cpus)

    print("process start:",time.time())
    acquire_stock_data()
    stock_data = read_stock_data()
    for key in stock_data.keys():
        processes = []
        p = multiprocessing.Process(target=collect_and_analyze_data, args=(stock_data[key]["code"].tolist(), one_cpu_length, formatted_start_day, formatted_today, lock))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    print("process finished:",time.time())

    
