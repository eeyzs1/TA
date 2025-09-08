
from talib import ADX,ADXR,APO,AROON,AROONOSC,BOP,CCI,CMO,DX,MACD,MACDEXT,MACDFIX,MFI,MINUS_DI,MINUS_DM,MOM,PLUS_DI,\
    PLUS_DM,PPO,ROC,ROCP,ROCR,ROCR100,RSI,STOCH,STOCHF,STOCHRSI,TRIX,ULTOSC,WILLR


# ENUM_BEGIN( MAType )
#    ENUM_DEFINE( TA_MAType_SMA,   Sma   ) =0,
#    ENUM_DEFINE( TA_MAType_EMA,   Ema   ) =1,
#    ENUM_DEFINE( TA_MAType_WMA,   Wma   ) =2,
#    ENUM_DEFINE( TA_MAType_DEMA,  Dema  ) =3,
#    ENUM_DEFINE( TA_MAType_TEMA,  Tema  ) =4,
#    ENUM_DEFINE( TA_MAType_TRIMA, Trima ) =5,
#    ENUM_DEFINE( TA_MAType_KAMA,  Kama  ) =6,
#    ENUM_DEFINE( TA_MAType_MAMA,  Mama  ) =7,
#    ENUM_DEFINE( TA_MAType_T3,    T3    ) =8
# ENUM_END( MAType )

def calculate_momentum_indicators(open, high, low, close, volume):
    # some results can be distorted with different parameters(for example, change timeperiod or length of input data to ADX can significantly change the output), 
    # so I can only judgement the current momentum with previous value
    weak_count = 0
    strong_count = 0
    up_trend = 0
    ### ADX - Average Directional Movement Index
    # seems for efficiency, the author of talib.ADX didn't smooth the tr when get prevTR for later calculate +DI and -DI 
    # ADX的取值范围在0到100之间。
    # ADX值越高，表示市场趋势越强。一般来说，ADX值超过25表示市场趋势较强，超过50表示市场趋势非常强。
    # ADX值的上升或下降也可以提供趋势变化的信号。例如，如果ADX值逐渐上升至40以上，表明市场趋势明显增强；反之，如果ADX值低于20，则表示市场可能进入震荡期。
    # adx = ADX(high, low, close, timeperiod=7)#default timeperiod is 14,but code will almost double it as start id, so use a relatively small value to decrease calculation cost

    # # ### ADXR - Average Directional Movement Index Rating
    # adxr = ADXR(high, low, close, timeperiod=7)

    # ### APO - Absolute Price Oscillator
    apo = APO(close, fastperiod=4, slowperiod=7, matype=0)

    # ### AROON - Aroon
    aroondown, aroonup = AROON(high, low, timeperiod=7)

    # ### AROONOSC - Aroon Oscillator, did by Aroon,Aroon Oscillator = Aroon-Up - Aroon-Down
    # real = AROONOSC(high, low, timeperiod=14)

    # ### BOP - Balance Of Power
    bop = BOP(open, high, low, close)

    # ### CCI - Commodity Channel Index,CCI = (Typical Price - MA) / (0.015 × Mean Deviation)
    # Typical Price（TP，典型价格） = （最高价 + 最低价 + 收盘价）÷ 3
    # MA（移动平均）：计算公式：最近N个交易时段内典型价格的移动平均值
    # Mean Deviation（MD，平均偏差）：计算公式：最近N个交易时段内典型价格与MA差值的绝对值的平均值
    # CCI > +100：表明资产可能处于超买状态，市场可能即将回调。CCI < -100：表明资产可能处于超卖状态，市场可能即将反弹。CCI在+100和-100之间：表明资产价格处于常态区间，市场趋势不明显。
    cci = CCI(high, low, close, timeperiod=7)

    # ### CMO - Chande Momentum Oscillator
    # CMO指标的计算公式为：CMO = (Su - Sd) × 100 / (Su + Sd)
    # Su是上涨日的价格增量总和，即今日收盘价高于昨日收盘价时的差值加总。若当日下跌，则增加值为0。
    # Sd是下跌日的价格减量总和，即今日收盘价低于昨日收盘价时的差值绝对值的加总。若当日上涨，则增加值为0。
    # 当CMO值大于+50时，市场可能处于超买状态，投资者应注意回调风险。
    # 当CMO值小于-50时，市场可能处于超卖状态，投资者可关注反弹机会。
    # CMO值的绝对值越高，市场趋势越强。当CMO值在+50或-50附近时，市场可能即将出现突破或反转。
    # 当CMO值在0附近波动时，市场可能处于盘整状态，投资者应谨慎操作
    cmo = CMO(close, timeperiod=7)

    # ### DX - Directional Movement Index,DX = [ | +DI - -DI | / ( +DI + -DI ) ] × 100, didnt use coz used adx
    # real = DX(high, low, close, timeperiod=14)

    # ### MACD - Moving Average Convergence/Divergence
    # DIF = EMA(短期收盘价, 短期天数) - EMA(长期收盘价, 长期天数), DEA = EMA(DIF, M), MACD = 2 × (DIF - DEA)
    # DIF线（差离值线）、DEA线（信号线）和MACD柱状图。DIF线是短期EMA（指数移动平均值）与长期EMA的差值，DEA线是DIF线的EMA，而MACD柱状图则是DIF线与DEA线之间的差值乘以2得到的。
    diff, dea, macdhist = MACD(close, fastperiod=3, slowperiod=12, signalperiod=7)
    
    # ### MACDEXT - MACD with controllable MA type， macdhist = (DIF - DEA) here, negligence or laziness of the programmer, does't matter
    # macd, macdsignal, macdhist = MACDEXT(real, fastperiod=12, fastmatype=0, slowperiod=26, slowmatype=0, signalperiod=9, signalmatype=0)

    # ### MACDFIX - Moving Average Convergence/Divergence Fix 12/26
    # macd, macdsignal, macdhist = MACDFIX(real, signalperiod=9)

    # ### MFI - Money Flow Index
    # typical price = (High + Low + Close)/3
    # positive_raw_money_flow = positive_typical_price * volume
    # negtive_raw_money_flow = negtive_typical_price * volume
    # money_flow_ratio = (positive_raw_money_flow x 14 period)/(negtive_raw_money_flow x 14 period)
    # money_flow_index = 100 - 100/(1 + money_flow_ratio)
    # TYP:=(HIGH+LOW+CLOSE)/3;
    # V1:=SUM(IF(TYP＞REF(TYP,1),TYP*VOL,0),N)/SUM(IF(TYP＜REF(TYP,1),TYP*VOL,0),N)
    # MFI:100-(100/(1+V1));
    # 具体是说：
    # 1.先计算一定期限内（一般14天）每天的典型价格（即TYP），它是当天最高价，最低价和收盘价三者的均值。也有给收盘价更大权值再算三者均值的算法。
    # 2.如果当天的典型价格大于昨天的则定义为流入，反之为流出，流入流出金额为典型价格乘以当天交易量。这样把14天每天结果计算出来，然后再把流出额和流入额分别加总，得到14天内的流入总额和流出总额，接着前者除以后者，大于1则14天内的资金为流入，反之为流出。V1就是代表这个比值。
    # 3.MFI就是在V1的基础上，为了更好地在坐标上显示出来，进行的数据处理。
    mfi = MFI(high, low, close, volume, timeperiod=14)

    # ### MINUS_DI - Minus Directional Indicator
    # real = MINUS_DI(high, low, close, timeperiod=14)

    # ### MINUS_DM - Minus Directional Movement
    # real = MINUS_DM(high, low, timeperiod=14)

    # ### MOM - Momentum, Momentum=当前价格−指定时间周期前的价格, too simple, abandoned
    # real = MOM(real, timeperiod=10)

    # ### PLUS_DI - Plus Directional Indicator
    # real = PLUS_DI(high, low, close, timeperiod=14)

    # ### PLUS_DM - Plus Directional Movement
    # real = PLUS_DM(high, low, timeperiod=14)

    # ### PPO - Percentage Price Oscillator
    # 基于正涨幅度之和的百分比计算：
    # 计算短期（通常为12日）和长期（通常为26日）的正涨幅度之和。正涨幅度是指当天收盘价高于前一天收盘价的差值。
    # 计算短期和长期正涨幅度之和的百分比，公式为：(短期正涨幅度之和 / 长期正涨幅度之和) × 100。
    # 基于移动平均线百分比变化的计算：
    # 使用短期（如12日）和长期（如26日）的指数移动平均线（EMA或SMA，但EMA更常用）。
    # 计算PPO指标，公式为：PPO = ((短期EMA - 长期EMA) / 长期EMA) × 100。
    # didnt use coz used macd instead
    # real = PPO(real, fastperiod=12, slowperiod=26, matype=0)

    # ### ROC - Rate of change : ((price/prevPrice)-1)100
    # real = ROC(real, timeperiod=10)

    # ### ROCP - Rate of change Percentage: (price-prevPrice)/prevPrice
    # real = ROCP(real, timeperiod=10)

    # ### ROCR - Rate of change ratio: (price/prevPrice)
    # real = ROCR(real, timeperiod=10)

    # ### ROCR100 - Rate of change ratio 100 scale: (price/prevPrice)100
    # real = ROCR100(real, timeperiod=10)

    # ### RSI - Relative Strength Index, 两种算法：
    # 1. RSI = (N日内上涨总幅度平均值 / N日内上涨总幅度和下跌总幅度平均值) × 100%
    # 2. RSI = 100 - (100 / (1 + RS))
    # RS = 过去N天的平均上涨幅度 / 过去N天的平均下跌幅度
    # 当RSI值在70以上时（有些交易者可能设定为80以上），市场被认为处于超买状态，价格可能即将回调或下跌。
    # 当RSI值在30以下时（有些交易者可能设定为20以下），市场处于超卖状态，价格可能即将反弹或上涨。
    # 当RSI值在50左右时，代表市场多空力量均衡。RSI值高于50表明市场处于强势状态，低于50则表明市场处于弱势状态
    rsi = RSI(close, timeperiod=7)

    # With stochastic, there is a total of 4 different lines that
    # are defined: FASTK, FASTD, SLOWK and SLOWD.
    # *
    # The D is the signal line usually drawn over its
    # corresponding K function.
    # *
    #                    (Today's Close - LowestLow)
    #  FASTK(Kperiod) =  --------------------------- 100
    #                     (HighestHigh - LowestLow)
    # *
    #  FASTD(FastDperiod, MA type) = MA Smoothed FASTK over FastDperiod
    # *
    #  SLOWK(SlowKperiod, MA type) = MA Smoothed FASTK over SlowKperiod
    # *
    #  SLOWD(SlowDperiod, MA Type) = MA Smoothed SLOWK over SlowDperiod
    # *
    # The HighestHigh and LowestLow are the extreme values among the
    # last 'Kperiod'.
    # *
    # SLOWK and FASTD are equivalent when using the same period.
    # *
    # The following shows how these four lines are made available in TA-LIB:
    # *
    #  TA_STOCH  : Returns the SLOWK and SLOWD
    #  TA_STOCHF : Returns the FASTK and FASTD

    # ### STOCH - Stochastic
    # Kt = 100 x ((Ct-Lt)/(Ht-Lt))
    # Kt is today stochastic
    # Ct is today closing price.
    # Lt is the lowest price of the last K Period (including today)
    # Ht is the highest price of the last K Period (including today)
    # then K was smoothed, Calculate the %D which is simply a moving average of the already smoothed %K
    slowk, slowd = STOCH(high, low, close, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)

    # ### STOCHF - Stochastic Fast
    fastk, fastd = STOCHF(high, low, close, fastk_period=5, fastd_period=3, fastd_matype=0)

    # ### STOCHRSI - Stochastic Relative Strength Index
    # StochRSI = (RSI - Lowest Low RSI) / (Highest High RSI - Lowest Low RSI)
    # fastkrsi is unsmoothed rsi, fastdrsi is smoothed fastkrsi
    fastkrsi, fastdrsi = STOCHRSI(close, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)

    # ### TRIX - 1-day Rate-Of-Change (ROC) of a Triple Smooth EMA
    # EMA1是原始价格数据的指数移动平均。其计算公式通常基于价格数据的加权平均值，权重随着距离当前时间点的远近而递减。具体公式可能因软件或平台而异，但一般形式为：EMA1 = (今日收盘价 - 昨日EMA1) × K + 昨日EMA1，其中K为平滑系数，与所选周期长度有关。
    # optInK_1  = 2 / (optInTimePeriod + 1)
    # 计算第二次指数移动平均（EMA2）：
    # EMA2是对EMA1的指数移动平均。其计算方法与EMA1相同，只是输入数据变为了EMA1的值。
    # 计算第三次指数移动平均（EMA3）：
    # EMA3是对EMA2的指数移动平均。同样地，其计算方法与EMA1和EMA2相同，只是输入数据变为了EMA2的值。
    # 计算TRIX：
    # TRIX是EMA3的百分比变化，用于突出趋势的转折点。其计算公式为：TRIX = (今日EMA3 - 昨日EMA3) / 昨日EMA3 × 100%。
    # trix = TRIX(close, timeperiod=15)

    # ### ULTOSC - Ultimate Oscillator
    # 一、选择移动平均线周期
    # 首先，需要选择三个不同周期的移动平均线。通常，这些周期被设定为7、14和28，但也可以根据个人偏好或市场特性进行调整。
    # 二、计算真实范围（True Range）
    # 对于每个选定的周期，需要计算其真实范围（True Range）。真实范围是以下三者中的最大值：
    # 当前周期的高价和低价之差。
    # 当前周期的高价和前一个周期的收盘价之差的绝对值。
    # 当前周期的低价和前一个周期的收盘价之差的绝对值。
    # 三、计算移动平均（Average1）
    # 接下来，对每个周期的真实范围进行移动平均计算。这里分别使用7个周期、14个周期和28个周期的移动平均线来得到三个Average1值。
    # 四、计算ULTOSC值
    # 最后，使用以下公式来计算ULTOSC指标的值：
    # ULTOSC = [(4 * Average1_period1) + (2 * Average1_period2) + Average1_period3] / (4 + 2 + 1)

    # 其中，Average1_period1、Average1_period2和Average1_period3分别代表7个周期、14个周期和28个周期的移动平均值。
    # ultosc = ULTOSC(high, low, close, timeperiod1=7, timeperiod2=14, timeperiod3=28)

    # ### WILLR - Williams' %R
    # 确定观察期：首先确定一个观察期，通常为14天（或其他天数，如7天、20天等），这个观察期用于计算最高价、最低价和收盘价。
    # 计算周期内的最高价和最低价：在观察期内，找出最高价（Hn）和最低价（Ln）。
    # 计算当日收盘价与周期内最高价和最低价的相对位置：使用公式（Hn-Ct）/（Hn-Ln）×-100来计算，其中Ct为当日的收盘价。这个公式反映了当日收盘价在观察期内价格波动范围中的相对位置。
    willr = WILLR(high, low, close, timeperiod=14)

    # if adx.iloc[-1] > 20:
    #     if adx.iloc[-1] < adx.iloc[-2]:
    #         weak_count += 1
    #     else:
    #         strong_count += 1

    # if adxr.iloc[-1] > 20:
    #     if adxr.iloc[-1] < adxr.iloc[-2]:
    #         weak_count += 1
    #     else:
    #         strong_count += 1

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

    if (cci.iloc[-1] < 100 and cci.iloc[-1] > 0) or cci.iloc[-1] < -100: 
        up_trend += 1
        if cci.iloc[-1] > cci.iloc[-2]:
            weak_count += 1
        else:
            strong_count += 1

    if (cmo.iloc[-1] < 50 and cmo.iloc[-1] > 0) or cmo.iloc[-1] < -50: 
        up_trend += 1
        if cmo.iloc[-1] > cmo.iloc[-2]:
            weak_count += 1
        else:
            strong_count += 1

    if macdhist.iloc[-1] > 0:
        up_trend += 1
        if macdhist.iloc[-1] < macdhist.iloc[-2] or (diff.iloc[-1] < 0 and dea.iloc[-1] < 0):
            weak_count += 1
        else:
            strong_count += 1

    if mfi.iloc[-1] > 0:
        up_trend += 1
        if mfi.iloc[-1] < mfi.iloc[-2]:
            weak_count += 1
        else:
            strong_count += 1
    
    if rsi.iloc[-1] > 0:
        up_trend += 1
        if rsi.iloc[-1] < rsi.iloc[-2]:
            weak_count += 1
        else:
            strong_count += 1
    
    if slowk.iloc[-1] > slowd.iloc[-1]:
        up_trend += 1
        if slowk.iloc[-1] > 20:
            weak_count += 1
        else:
            strong_count += 1

    if fastk.iloc[-1] > fastd.iloc[-1]:
        up_trend += 1
        if fastk.iloc[-1] > 20:
            weak_count += 1
        else:
            strong_count += 1

    if fastkrsi.iloc[-1] > fastdrsi.iloc[-1]:
        up_trend += 1
        if fastkrsi.iloc[-1] > 20:
            weak_count += 1
        else:
            strong_count += 1

    if willr.iloc[-1] < -80:
        up_trend += 1
        if willr.iloc[-1] > willr.iloc[-2]:
            weak_count += 1
        else:
            strong_count += 1

    return up_trend, weak_count, strong_count