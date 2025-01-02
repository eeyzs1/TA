
from talib import BBANDS,DEMA,EMA,HT_TRENDLINE,KAMA,MA,MAMA,MAVP,MIDPOINT,MIDPRICE,SAR,SAREXT,SMA,T3,TEMA,TRIMA,WMA


def calculate_overlap_for_tech(open, high, low, close):
    ### BBANDS - Bollinger Bands
    upperband, middleband, lowerband = BBANDS(real, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)

    ### DEMA - Double Exponential Moving Average
    real = DEMA(real, timeperiod=30)

    ### EMA - Exponential Moving Average
    #NOTE: The ``EMA`` function has an unstable period.  
    real = EMA(real, timeperiod=30)

    ### HT_TRENDLINE - Hilbert Transform - Instantaneous Trendline
    #NOTE: The ``HT_TRENDLINE`` function has an unstable period.  
    real = HT_TRENDLINE(real)

    ### KAMA - Kaufman Adaptive Moving Average
    #NOTE: The ``KAMA`` function has an unstable period.  
    real = KAMA(real, timeperiod=30)

    ### MA - Moving average
    real = MA(real, timeperiod=30, matype=0)

    ### MAMA - MESA Adaptive Moving Average
    #NOTE: The ``MAMA`` function has an unstable period.  
    mama, fama = MAMA(real, fastlimit=0, slowlimit=0)

    ### MAVP - Moving average with variable period
    real = MAVP(real, periods, minperiod=2, maxperiod=30, matype=0)

    ### MIDPOINT - MidPoint over period
    real = MIDPOINT(real, timeperiod=14)

    ### MIDPRICE - Midpoint Price over period
    real = MIDPRICE(high, low, timeperiod=14)

    ### SAR - Parabolic SAR
    real = SAR(high, low, acceleration=0, maximum=0)

    ### SAREXT - Parabolic SAR - Extended
    real = SAREXT(high, low, startvalue=0, offsetonreverse=0, accelerationinitlong=0, accelerationlong=0, accelerationmaxlong=0, accelerationinitshort=0, accelerationshort=0, accelerationmaxshort=0)

    ### SMA - Simple Moving Average
    real = SMA(real, timeperiod=30)

    ### T3 - Triple Exponential Moving Average (T3)
    #NOTE: The ``T3`` function has an unstable period.  
    real = T3(real, timeperiod=5, vfactor=0)

    ### TEMA - Triple Exponential Moving Average
    real = TEMA(real, timeperiod=30)

    ### TRIMA - Triangular Moving Average
    real = TRIMA(real, timeperiod=30)

    ### WMA - Weighted Moving Average
    real = WMA(real, timeperiod=30)