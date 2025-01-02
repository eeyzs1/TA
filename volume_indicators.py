
from talib import AD,ADOSC,OBV

def calculate_volume_indicators(volume, high, low, close):
    turnaround_count = 0
    consistency_count = 0
    ### AD - Chaikin A/D Line
    # AD = AD_prev + ((close - low) - (high - close)) / (high - low) * volume
    ad_v = AD(high, low, close, volume)

    ### ADOSC - Chaikin A/D Oscillator
    # ADOSC = EMA(AD, short_period) - EMA(AD, long_period)
    # 当ADOSC的值为正数时，表示买入压力较大，市场可能处于上升趋势
    adosc = ADOSC(high, low, close, volume, fastperiod=3, slowperiod=10)

    ### OBV - On Balance Volume
    # OBV=OBV前一日+sgn×今成交量。其中sgn为符号函数，当今收盘价>昨收盘价时，sgn取+1（表示成交量加入OBV）；当今收盘价<昨收盘价时，sgn取-1（表示成交量从OBV中减去）；当今收盘价=昨收盘价时，sgn取0（表示成交量不影响OBV
    obv = OBV(close, volume)

    if ad_v.iloc[-1] > ad_v.iloc[-2]:
        if close.iloc[-1] > close.iloc[-2]:#如果AD线上升的同时，价格也在上升，则说明上升趋势被确认，可能产生买入信号
            consistency_count += 1
        else:#如果AD线上升的同时，价格在下降，二者产生背离，说明价格的下降趋势可能减弱，有可能反转回升。
            turnaround_count += 1

    if adosc.iloc[-1] > adosc.iloc[-2]:
        if close.iloc[-1] > close.iloc[-2]:#如果ADOSC线上升的同时，价格也在上升，则说明上升趋势被确认，可能产生买入信号
            consistency_count += 1
        else:# 当价格创出新低而ADOSC未能同步创出新低时，可能形成看涨背离，暗示市场下跌动力减弱，可能产生买入信号
            turnaround_count += 1

    if obv.iloc[-1] > obv.iloc[-2]:
        consistency_count += 1
        turnaround_count += 1

    return turnaround_count, consistency_count