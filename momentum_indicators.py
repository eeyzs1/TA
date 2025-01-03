
from talib import ADX,ADXR,APO,AROON,AROONOSC,BOP,CCI,CMO,DX,MACD,MACDEXT,MACDFIX,MFI,MINUS_DI,MINUS_DM,MOM,PLUS_DI,\
    PLUS_DM,PPO,ROC,ROCP,ROCR,ROCR100,RSI,STOCH,STOCHF,STOCHRSI,TRIX,ULTOSC,WILLR


def calculate_momentum_indicators(open, high, low, close):
    # some results can be distorted with different parameters(for example, change timeperiod or length of input data to ADX can significantly change the output), 
    # so I can only judgement the current momentum with previous value
    weak_count = 0
    strong_count = 0
    up_trend = 0
    down_trend = 0
    ### ADX - Average Directional Movement Index
    # seems for efficiency, the author of talib.ADX didn't smooth the tr when get prevTR for later calculate +DI and -DI 
    # ADX的取值范围在0到100之间。
    # ADX值越高，表示市场趋势越强。一般来说，ADX值超过25表示市场趋势较强，超过50表示市场趋势非常强。
    # ADX值的上升或下降也可以提供趋势变化的信号。例如，如果ADX值逐渐上升至40以上，表明市场趋势明显增强；反之，如果ADX值低于20，则表示市场可能进入震荡期。
    adx = ADX(high, low, close, timeperiod=7)#default timeperiod is 14,but code will almost double it as start id, so use a relatively small value to decrease calculation cost

    # ### ADXR - Average Directional Movement Index Rating
    adxr = ADXR(high, low, close, timeperiod=7)

    # ### APO - Absolute Price Oscillator
    apo = APO(close, fastperiod=4, slowperiod=7, matype=0)

    # ### AROON - Aroon
    aroondown, aroonup = AROON(high, low, timeperiod=7)

    # ### AROONOSC - Aroon Oscillator, did by Aroon,Aroon Oscillator = Aroon-Up - Aroon-Down
    # real = AROONOSC(high, low, timeperiod=14)

    # ### BOP - Balance Of Power
    bop = BOP(open, high, low, close)

    # ### CCI - Commodity Channel Index
    # real = CCI(high, low, close, timeperiod=14)

    # ### CMO - Chande Momentum Oscillator
    # real = CMO(real, timeperiod=14)

    # ### DX - Directional Movement Index
    # real = DX(high, low, close, timeperiod=14)

    # ### MACD - Moving Average Convergence/Divergencepython
    # macd, macdsignal, macdhist = MACD(real, fastperiod=12, slowperiod=26, signalperiod=9)

    # ### MACDEXT - MACD with controllable MA typepython
    # macd, macdsignal, macdhist = MACDEXT(real, fastperiod=12, fastmatype=0, slowperiod=26, slowmatype=0, signalperiod=9, signalmatype=0)

    # ### MACDFIX - Moving Average Convergence/Divergence Fix 12/26python
    # macd, macdsignal, macdhist = MACDFIX(real, signalperiod=9)

    # ### MFI - Money Flow Index
    # real = MFI(high, low, close, volume, timeperiod=14)

    # ### MINUS_DI - Minus Directional Indicator
    # real = MINUS_DI(high, low, close, timeperiod=14)

    # ### MINUS_DM - Minus Directional Movement
    # real = MINUS_DM(high, low, timeperiod=14)

    # ### MOM - Momentumpython
    # real = MOM(real, timeperiod=10)

    # ### PLUS_DI - Plus Directional Indicator
    # real = PLUS_DI(high, low, close, timeperiod=14)

    # ### PLUS_DM - Plus Directional Movement
    # real = PLUS_DM(high, low, timeperiod=14)

    # ### PPO - Percentage Price Oscillatorpython
    # real = PPO(real, fastperiod=12, slowperiod=26, matype=0)

    # ### ROC - Rate of change : ((price/prevPrice)-1)*100python
    # real = ROC(real, timeperiod=10)

    # ### ROCP - Rate of change Percentage: (price-prevPrice)/prevPricepython
    # real = ROCP(real, timeperiod=10)

    # ### ROCR - Rate of change ratio: (price/prevPrice)python
    # real = ROCR(real, timeperiod=10)

    # ### ROCR100 - Rate of change ratio 100 scale: (price/prevPrice)*100python
    # real = ROCR100(real, timeperiod=10)

    # ### RSI - Relative Strength Index
    # real = RSI(real, timeperiod=14)

    # ### STOCH - Stochasticpython
    # slowk, slowd = STOCH(high, low, close, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)

    # ### STOCHF - Stochastic Fastpython
    # fastk, fastd = STOCHF(high, low, close, fastk_period=5, fastd_period=3, fastd_matype=0)

    # ### STOCHRSI - Stochastic Relative Strength Index
    # fastk, fastd = STOCHRSI(real, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)

    # ### TRIX - 1-day Rate-Of-Change (ROC) of a Triple Smooth EMApython
    # real = TRIX(real, timeperiod=30)

    # ### ULTOSC - Ultimate Oscillatorpython
    # real = ULTOSC(high, low, close, timeperiod1=7, timeperiod2=14, timeperiod3=28)

    # ### WILLR - Williams' %Rpython
    # real = WILLR(high, low, close, timeperiod=14)

    if adx.iloc[-1] > 20:
        if adx.iloc[-1] < adx.iloc[-2]:
            weak_count += 1
        else:
            strong_count += 1

    if adxr.iloc[-1] > 20:
        if adxr.iloc[-1] < adxr.iloc[-2]:
            weak_count += 1
        else:
            strong_count += 1

    if apo.iloc[-1] > 0:
        up_trend += 1
        if apo.iloc[-1] < apo.iloc[-2]:
            weak_count += 1
        else:
            strong_count += 1

    if aroonup.iloc[-1] > aroondown.iloc[-1]:
        up_trend += 1
        if aroonup.iloc[-1] - aroondown.iloc[-1] < aroonup.iloc[-2] - aroondown.iloc[-2]:
            weak_count += 1
        else:
            strong_count += 1

    if bop.iloc[-1] > 0:
        up_trend += 1
        if bop.iloc[-1] < bop.iloc[-2]:
            weak_count += 1
        else:
            strong_count += 1


    print("adx",adx)
    print("adxr",adxr)
    print("apo",apo)
    print("aroonup",aroonup)
    print("aroondown",aroondown)
    print("bop",bop)




    return up_trend, down_trend, weak_count, strong_count