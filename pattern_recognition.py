
import talib



# neg means downward trend, pos upward, 0 unrelated
def calculate_overlap_for_tech(open, high, low, close):
    neg_count = 0
    pos_count = 0
    res = 0

    if talib.CDL2CROWS(open, high, low, close).iloc[-1] < 0:
        neg_count += 1
    if talib.CDL3BLACKCROWS(open, high, low, close).iloc[-1] < 0:
        neg_count += 1
    res = talib.CDL3INSIDE(open, high, low, close).iloc[-1] < 0
    if res < 0:
        neg_count += 1
    elif res > 0:
        pos_count += 1
    res = talib.CDL3LINESTRIKE(open, high, low, close).iloc[-1]
    if  res < 0:
        neg_count += 1
    elif res > 0:
        pos_count += 1
    res = talib.CDL3OUTSIDE(open, high, low, close).iloc[-1]
    if  res < 0:
        neg_count += 1
    elif res > 0:
        pos_count += 1
    if talib.CDL3STARSINSOUTH(open, high, low, close).iloc[-1] > 0:
        pos_count += 1
    if talib.CDL3WHITESOLDIERS(open, high, low, close).iloc[-1] > 0:
        pos_count += 1
    res = talib.CDLABANDONEDBABY(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    if talib.CDLADVANCEBLOCK(open, high, low, close).iloc[-1] < 0:
        neg_count += 1
    res = talib.CDLBELTHOLD(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    res = talib.CDLBREAKAWAY(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    res = talib.CDLCLOSINGMARUBOZU(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    if talib.CDLCONCEALBABYSWALL(open, high, low, close).iloc[-1] > 0:
        pos_count += 1
    res = talib.CDLCOUNTERATTACK(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    if talib.CDLDARKCLOUDCOVER(open, high, low, close).iloc[-1] < 0:
        neg_count += 1
    res = talib.CDLDOJISTAR(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    if talib.CDLDRAGONFLYDOJI(open, high, low, close).iloc[-1] > 0:
        pos_count += 1
    res = talib.CDLENGULFING(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    if talib.CDLEVENINGDOJISTAR(open, high, low, close).iloc[-1] < 0:
        neg_count += 1
    if talib.CDLEVENINGSTAR(open, high, low, close).iloc[-1] < 0:
        neg_count += 1
    res = talib.CDLGAPSIDESIDEWHITE(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    if talib.CDLGRAVESTONEDOJI(open, high, low, close).iloc[-1] > 0:#special condition that current understanding of gravestone doji different from original ~
        neg_count += 1
    if talib.CDLHAMMER(open, high, low, close).iloc[-1] > 0:
        pos_count += 1
    if talib.CDLHANGINGMAN(open, high, low, close).iloc[-1] < 0:
        neg_count += 1
    res = talib.CDLHARAMI(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    res = talib.CDLHARAMICROSS(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    res = talib.CDLHIKKAKE(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    res = talib.CDLHIKKAKEMOD(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    if talib.CDLHOMINGPIGEON(open, high, low, close).iloc[-1] > 0:
        pos_count += 1
    if talib.CDLIDENTICAL3CROWS(open, high, low, close).iloc[-1] < 0:
        neg_count += 1
    if talib.CDLINNECK(open, high, low, close).iloc[-1] < 0:
        neg_count += 1
    if talib.CDLINVERTEDHAMMER(open, high, low, close).iloc[-1] > 0:
        pos_count += 1
    res = talib.CDLKICKING(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    res = talib.CDLKICKINGBYLENGTH(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    if talib.CDLLADDERBOTTOM(open, high, low, close).iloc[-1] > 0:
        pos_count += 1
    res = talib.CDLLONGLINE(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    res = talib.CDLMARUBOZU(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    if talib.CDLMATCHINGLOW(open, high, low, close).iloc[-1] > 0:
        pos_count += 1
    if talib.CDLMATHOLD(open, high, low, close).iloc[-1] > 0:
        pos_count += 1
    if talib.CDLMORNINGDOJISTAR(open, high, low, close).iloc[-1] > 0:
        pos_count += 1
    if talib.CDLMORNINGSTAR(open, high, low, close).iloc[-1] > 0:
        pos_count += 1
    if talib.CDLONNECK(open, high, low, close).iloc[-1] < 0:
        neg_count += 1
    if talib.CDLPIERCING(open, high, low, close).iloc[-1] > 0:
        pos_count += 1
    res = talib.CDLRISEFALL3METHODS(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    res = talib.CDLSEPARATINGLINES(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    if talib.CDLSHOOTINGSTAR(open, high, low, close).iloc[-1] < 0:
        neg_count += 1
    if talib.CDLSTALLEDPATTERN(open, high, low, close).iloc[-1] < 0:
        neg_count += 1
    if talib.CDLSTICKSANDWICH(open, high, low, close).iloc[-1] > 0:
        pos_count += 1
    res = talib.CDLTASUKIGAP(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    if talib.CDLTHRUSTING(open, high, low, close).iloc[-1] < 0:
        neg_count += 1
    res = talib.CDLTRISTAR(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    res = talib.CDLUNIQUE3RIVER(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    if talib.CDLUPSIDEGAP2CROWS(open, high, low, close).iloc[-1] < 0:
        neg_count += 1
    res = talib.CDLXSIDEGAP3METHODS(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    return neg_count, pos_count