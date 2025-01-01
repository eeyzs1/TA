from talib import ATR,NATR,TRANGE

# ATR = 前一日ATR × (N - 1) / N + 当日TR / N
# 其中，N代表周期长度，通常设为14天，但也可以根据具体需求进行调整。为了计算前一日的ATR，你需要知道前一日的ATR值（First value of the ATR is a simple Average of
#     * the TRANGE output for the specified period.）以及前一日的真实范围TR。
# 前一日的真实范围TR同样是通过以下公式计算的：
# TR = Max[(H−L), Abs(H−Cprev), Abs(L−Cprev)]
# 其中，H表示前一日的最高价，L表示前一日的最低价，Cprev表示前两日的收盘价。将这个TR值代入前一日ATR的计算公式中，并考虑到N的值（比如14天），你就可以得到前一日的ATR值。

# NATR = ATR / Close * 100，其中Close代表当天的收盘价。

def calculate_volatility_indicators(high, low, close):
    # atr = ATR(high, low, close, timeperiod=14)

    return NATR(high, low, close, timeperiod=14)

    # trange = TRANGE(high, low, close)