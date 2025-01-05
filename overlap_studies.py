
from talib import BBANDS,DEMA,EMA,HT_TRENDLINE,KAMA,MA,MAMA,MAVP,MIDPOINT,MIDPRICE,SAR,SAREXT,SMA,T3,TEMA,TRIMA,WMA


def calculate_overlap(high, low, close):
    buy_count = 0
    sell_count = 0
    ### BBANDS - Bollinger Bands
    upperband, middleband, lowerband = BBANDS(close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)

    ### DEMA - Double Exponential Moving Average
    dema = DEMA(close, timeperiod=7)

    # ### EMA - Exponential Moving Average
    # #NOTE: The ``EMA`` function has an unstable period.  
    # close = EMA(close, timeperiod=30)

    ### HT_TRENDLINE - Hilbert Transform - Instantaneous Trendline
    # #NOTE: The ``HT_TRENDLINE`` function has an unstable period.  
    # close = HT_TRENDLINE(close)

    ### KAMA - Kaufman Adaptive Moving Average
    #NOTE: The ``KAMA`` function has an unstable period.  
    # close = KAMA(close, timeperiod=30)

    # ### MA - Moving average
    # close = MA(close, timeperiod=30, matype=0)

    ### MAMA - MESA Adaptive Moving Average
    #NOTE: The ``MAMA`` function has an unstable period.  
    # mama, fama = MAMA(close, fastlimit=0, slowlimit=0)

    ### MAVP - Moving average with variable period
    # close = MAVP(close, periods, minperiod=2, maxperiod=30, matype=0)

    ### MIDPOINT - MidPoint over period
    # close = MIDPOINT(close, timeperiod=14)

    ### MIDPRICE - Midpoint Price over period
    # close = MIDPRICE(high, low, timeperiod=14)

    ### SAR - Parabolic SAR
    sar = SAR(high, low, acceleration=0.02, maximum=0.2)

    ### SAREXT - Parabolic SAR - Extended
    # the extended parameters are too complex and effect is unsure, so abandoned
    # close = SAREXT(high, low, startvalue=0, offsetonreverse=0, accelerationinitlong=0, accelerationlong=0, accelerationmaxlong=0, accelerationinitshort=0, accelerationshort=0, accelerationmaxshort=0)

    # ### SMA - Simple Moving Average
    # close = SMA(close, timeperiod=30)

    # ### T3 - Triple Exponential Moving Average (T3)
    # #NOTE: The ``T3`` function has an unstable period.  
    # close = T3(close, timeperiod=5, vfactor=0)

    ### TEMA - Triple Exponential Moving Average
    tema = TEMA(close, timeperiod=7)

    ### TRIMA - Triangular Moving Average
    trima = TRIMA(close, timeperiod=7)

    ### WMA - Weighted Moving Average
    wma = WMA(close, timeperiod=7)

    if close.iloc[-1] > middleband.iloc[-1] and close.iloc[-1] < upperband.iloc[-1]:
        buy_count += 1
    else:
        sell_count += 1

    if close.iloc[-1] > dema.iloc[-1] and dema.iloc[-1] > dema.iloc[-2]:
        buy_count += 1
    else:
        sell_count += 1

    if close.iloc[-1] > sar.iloc[-1] and sar.iloc[-1] > sar.iloc[-2]:
        buy_count += 1
    else:
        sell_count += 1
    
    if close.iloc[-1] > tema.iloc[-1] and tema.iloc[-1] > tema.iloc[-2]:
        buy_count += 1
    else:
        sell_count += 1
    
    if close.iloc[-1] > trima.iloc[-1] and trima.iloc[-1] > trima.iloc[-2]:
        buy_count += 1
    else:
        sell_count += 1

    if close.iloc[-1] > wma.iloc[-1] and wma.iloc[-1] > wma.iloc[-2]:
        buy_count += 1
    else:
        sell_count += 1

    return buy_count,sell_count