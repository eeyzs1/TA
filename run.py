import requests
import json
import time
import math
import pandas as pd
import numpy as np
import pysnowball as ball

# 股票EMA，即指数移动平均线（Exponential Moving Average）EMA是以指数式递减加权的移动平均，它给予最近的价格数据更高的权重，使得均线对价格变动的反应更为灵敏
# EMA的计算公式为：EMA(C,N)=2*C/(N+1)+(N-1)/(N+1)*EMA(C,N-1)，其中C代表当日的收盘价，N为选择的周期天数，EMA(C,N-1)为前一日的N周期EMA值。平滑系数=2/(周期单位+1)
# 若Y=EMA(X，N)，则Y=［2*X+(N-1)*Y’］/(N+1)，其中Y’表示上一周期的Y值
# 简化公式EMA（X，N）＝2Ni/((N+1)*N)*X(Ni),X(Ni)是第Ni个数据，越靠近输入右侧（输入数据日期从左到右由远及近），Ni越大
def ema(data,n):
    ema1 = 0
    if n == len(data):
        divisor = n*(n+1)
        for i in range(n-1,0,-1):
            ema1 += data[i]*(i+1)/divisor
        return ema1
    num = math.floor(len(data)/n)*n#the data that can be used to calculate EMA(X,N) by N data points
    ema1_len = len(data) - num
    ema1_data = data[:ema1_len]
    subsequent_data = data[-num:]
    divisor = (ema1_len*ema1_len+ema1_len)/2
    for i in range(ema1_len-1,0,-1):
        ema1 += ema1_data[i]*(i+1)/divisor
    res = [ema1]
    divisor = n+1
    coefficient = n-1
    for i in range(num):
        y = (2*subsequent_data[i]+coefficient*res[-1])/divisor
        res.append(y)
    return res

# MACD（Moving Average Convergence and Divergence）异同移动平均线
# DIF = EMA(今日收盘价,12)-EMA(今日收盘价,26), DEA = EMA(今日DIF,9） 第一天的DEA值等于第一天的DIF, MACD = BAR = 2 *（DIF-DEA）
def macd(data,minuend:int=12,subtrahend:int=26,dea_pts:int = 9):
    ema12 = ema(data,minuend)
    ema26 = ema(data,subtrahend)
    min_len = min(len(ema12),len(ema26))
    dif = [a - b for a, b in zip(ema12[-min_len:], ema26[-min_len:])]
    dea = ema(dif,dea_pts)
    dif_cut = dif[-len(dea):]
    macd = [2*(a - b) for a, b in zip(dif_cut, dea)]
    return macd

# 当DIF > 0时(0轴之上)：说明股票的价格在上涨，DIF越大，代表价格上涨的越多,当DIF < 0时(0轴之下)：说明股票的价格在下跌，DIF的绝对值越大，代表价格下跌的越多,DEA是对EMA指数移动平均指标，相对来说EMA变化的更缓慢，更平滑一些。
# 当MACD>0，即DIF上穿DEA时，说明DIF趋势变化走强，此时显示为红柱,当MACD<0，即DIF下破DEA时，说明DIF趋势变化走弱，此时显示为绿柱
# 零轴上金叉：DIF>0，DIF上穿DEA，MACD>0,表示股票处于上涨状态，且加速上涨，持续上涨趋势
# 零轴上死叉：DIF>0，DIF下破DEA，MACD<0,表示股票处于上涨状态，但上涨速度减慢，上涨趋势可能会有变化，股价有可能转而下跌
# 零轴下金叉：DIF<0，DIF上穿DEA，MACD>0,表示股票处于下跌状态，但下跌速度减慢，下跌趋势可能会有变化，股价有可能转而上涨
# 零轴下死叉：DIF<0，DIF下破DEA，MACD<0,表示股票处于下跌状态，且加速下跌，持续下跌趋势
def judge_macd(macd,n:int = 3):#一周五个交易日，一半向上取整为3作为默认值
    ema_macd = ema(macd[-n:],n)
    if macd[-1]>0 and ema_macd[-1] > 0:#整体趋势n天大于0且，最近1天趋势依然大于0
        return True

#简单移动平均线（Simple Moving Average），MA = (P1 + P2 + P3 + ... + Pn) / n
def sma(prices,period=5):
    sma = []
    for i in range(period,len(prices)+1):
        price_slice = prices[i-period:i]
        average = sum(price_slice) / period
        sma.append(average)
    return sma

def judge_sma(close_data):
    ma5 = sma(close_data[-14:],5)
    ma10 = sma(close_data[-19:],10)
    ma15 = sma(close_data[-24:],15)
    print(ma5)
    day_ary = np.array(list(range(10)))
    ma5_ary = np.array(ma5)
    cc_ma5 = np.corrcoef(day_ary, ma5_ary)[0,1]#correlation_coefficient
    ma10_ary = np.array(ma10)
    cc_ma10 = np.corrcoef(day_ary, ma10_ary)[0,1]
    ma15_ary = np.array(ma15)
    cc_ma15 = np.corrcoef(day_ary, ma15_ary)[0,1]
    return cc_ma5 > 0 and cc_ma10 > 0 and cc_ma15 > 0

def judge_ema(close_data):
    ma5 = ema(close_data[-14:],5)
    ma10 = ema(close_data[-19:],10)
    ma15 = ema(close_data[-24:],15)
    print(ma5)
    day_ary = np.array(list(range(10)))
    ma5_ary = np.array(ma5)
    cc_ma5 = np.corrcoef(day_ary, ma5_ary)[0,1]#correlation_coefficient
    ma10_ary = np.array(ma10)
    cc_ma10 = np.corrcoef(day_ary, ma10_ary)[0,1]
    ma15_ary = np.array(ma15)
    cc_ma15 = np.corrcoef(day_ary, ma15_ary)[0,1]
    return cc_ma5 > 0 and cc_ma10 > 0 and cc_ma15 > 0

# ['timestamp',时间戳 'volume',成交量（股）'open',开盘价 'high',最高价 'low',最低价 'close',收盘价
# 'chg',变化量（相较于昨天收盘价） 'percent',变化量百分比 'turnoverrate',周转率or换手率（成交量/流通股， 3-15为合理区间，9，7-11） 
# 'amount',成交额 'volume_post', 'amount_post', 此接口无法获取，服务器返回None
# 'pe',市盈率(price to earnings ratio，股票/每股收益(EPS)，公司盈利能力，成长性公司盈利差所以pe高)， 此处为（Trailing Twelve Months P/E Ratio），又称滚动市盈率，，是指在一定的考察期（一般是12个月）内，股票的价格和每股收益的比率。
# 'pb',市净率（Price to Book Value Ratio，PB）是股票价格与每股净资产（即股东权益）的比率
# 'ps',市销率（Price to Sales Ratio，PS）是股票价格与每股销售收入(公司每单位销售收入)的比率，例如成长性公司，高销售但是低利润
# 'pcf',市现率（Price to Cash Flow Ratio，PCF）是股票价格与每股现金流量的比率，现金流
# 'market_capital', 总市值
# 'balance', 'hold_volume_cn', 'hold_ratio_cn', 'net_volume_cn', 'hold_volume_hk', 'hold_ratio_hk', 'net_volume_hk']此接口获取不到
def run_kline_analysis():
    ball.set_token("xq_a_token=c3fee82524969f1ad85e825d9a1fbb38e6d258ed;u=2598601362")
    tech_stocks = ['SZ000158']
    print("The judgement of tech stocks:")
    for stock_id in tech_stocks:
        res = ball.kline(stock_id,30)
        df = pd.DataFrame(res['data']['item'], columns=res['data']['column']).dropna(axis = 1)
        close_data = df['close'].tolist()
        macd_res = macd(close_data,12,26,9)#macd_res to avoid conflict with functon macd's name that cause UnboundLocalError
        if judge_macd(macd_res,3):
            if judge_sma(close_data):
                if judge_ema(close_data):
                    print(stock_id,macd_res)


if __name__ == '__main__':
    run_kline_analysis()
