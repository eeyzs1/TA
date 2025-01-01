
from talib import CDL2CROWS,CDL3BLACKCROWS,CDL3INSIDE,CDL3LINESTRIKE,CDL3OUTSIDE,CDL3STARSINSOUTH,CDL3WHITESOLDIERS,CDLABANDONEDBABY,CDLADVANCEBLOCK,\
    CDLBELTHOLD,CDLBREAKAWAY,CDLCLOSINGMARUBOZU,CDLCONCEALBABYSWALL,CDLCOUNTERATTACK,CDLDARKCLOUDCOVER,CDLDOJI,CDLDOJISTAR,CDLDRAGONFLYDOJI,CDLENGULFING,\
        CDLEVENINGDOJISTAR,CDLEVENINGSTAR,CDLGAPSIDESIDEWHITE,CDLGRAVESTONEDOJI,CDLHAMMER,CDLHANGINGMAN,CDLHARAMI,CDLHARAMICROSS,CDLHIGHWAVE,CDLHIKKAKE,\
            CDLHIKKAKEMOD,CDLHOMINGPIGEON,CDLIDENTICAL3CROWS,CDLINNECK,CDLINVERTEDHAMMER,CDLKICKING,CDLKICKINGBYLENGTH,CDLLADDERBOTTOM,CDLLONGLEGGEDDOJI,\
                CDLLONGLINE,CDLMARUBOZU,CDLMATCHINGLOW,CDLMATHOLD,CDLMORNINGDOJISTAR,CDLMORNINGSTAR,CDLONNECK,CDLPIERCING,CDLRICKSHAWMAN,CDLRISEFALL3METHODS,\
                    CDLSEPARATINGLINES,CDLSHOOTINGSTAR,CDLSHORTLINE,CDLSPINNINGTOP,CDLSTALLEDPATTERN,CDLSTICKSANDWICH,CDLTAKURI,CDLTASUKIGAP,CDLTHRUSTING,CDLTRISTAR,\
                        CDLUNIQUE3RIVER,CDLUPSIDEGAP2CROWS,CDLXSIDEGAP3METHODS


# neg means downward trend, pos upward, 0 unrelated
def pattern_match(open, high, low, close):
    neg_count = 0
    pos_count = 0
    res = 0

    if CDL2CROWS(open, high, low, close).iloc[-1] < 0:
        neg_count += 1
    if CDL3BLACKCROWS(open, high, low, close).iloc[-1] < 0:
        neg_count += 1
    res = CDL3INSIDE(open, high, low, close).iloc[-1] < 0
    if res < 0:
        neg_count += 1
    elif res > 0:
        pos_count += 1
    res = CDL3LINESTRIKE(open, high, low, close).iloc[-1]
    if  res < 0:
        neg_count += 1
    elif res > 0:
        pos_count += 1
    res = CDL3OUTSIDE(open, high, low, close).iloc[-1]
    if  res < 0:
        neg_count += 1
    elif res > 0:
        pos_count += 1
    if CDL3STARSINSOUTH(open, high, low, close).iloc[-1] > 0:
        pos_count += 1
    if CDL3WHITESOLDIERS(open, high, low, close).iloc[-1] > 0:
        pos_count += 1
    res = CDLABANDONEDBABY(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    if CDLADVANCEBLOCK(open, high, low, close).iloc[-1] < 0:
        neg_count += 1
    res = CDLBELTHOLD(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    res = CDLBREAKAWAY(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    res = CDLCLOSINGMARUBOZU(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    if CDLCONCEALBABYSWALL(open, high, low, close).iloc[-1] > 0:
        pos_count += 1
    res = CDLCOUNTERATTACK(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    if CDLDARKCLOUDCOVER(open, high, low, close).iloc[-1] < 0:
        neg_count += 1
    res = CDLDOJISTAR(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    if CDLDRAGONFLYDOJI(open, high, low, close).iloc[-1] > 0:
        pos_count += 1
    res = CDLENGULFING(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    if CDLEVENINGDOJISTAR(open, high, low, close).iloc[-1] < 0:
        neg_count += 1
    if CDLEVENINGSTAR(open, high, low, close).iloc[-1] < 0:
        neg_count += 1
    res = CDLGAPSIDESIDEWHITE(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    if CDLGRAVESTONEDOJI(open, high, low, close).iloc[-1] > 0:#special condition that current understanding of gravestone doji different from original ~
        neg_count += 1
    if CDLHAMMER(open, high, low, close).iloc[-1] > 0:
        pos_count += 1
    if CDLHANGINGMAN(open, high, low, close).iloc[-1] < 0:
        neg_count += 1
    res = CDLHARAMI(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    res = CDLHARAMICROSS(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    res = CDLHIKKAKE(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    res = CDLHIKKAKEMOD(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    if CDLHOMINGPIGEON(open, high, low, close).iloc[-1] > 0:
        pos_count += 1
    if CDLIDENTICAL3CROWS(open, high, low, close).iloc[-1] < 0:
        neg_count += 1
    if CDLINNECK(open, high, low, close).iloc[-1] < 0:
        neg_count += 1
    if CDLINVERTEDHAMMER(open, high, low, close).iloc[-1] > 0:
        pos_count += 1
    res = CDLKICKING(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    res = CDLKICKINGBYLENGTH(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    if CDLLADDERBOTTOM(open, high, low, close).iloc[-1] > 0:
        pos_count += 1
    res = CDLLONGLINE(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    res = CDLMARUBOZU(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    if CDLMATCHINGLOW(open, high, low, close).iloc[-1] > 0:
        pos_count += 1
    if CDLMATHOLD(open, high, low, close).iloc[-1] > 0:
        pos_count += 1
    if CDLMORNINGDOJISTAR(open, high, low, close).iloc[-1] > 0:
        pos_count += 1
    if CDLMORNINGSTAR(open, high, low, close).iloc[-1] > 0:
        pos_count += 1
    if CDLONNECK(open, high, low, close).iloc[-1] < 0:
        neg_count += 1
    if CDLPIERCING(open, high, low, close).iloc[-1] > 0:
        pos_count += 1
    res = CDLRISEFALL3METHODS(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    res = CDLSEPARATINGLINES(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    if CDLSHOOTINGSTAR(open, high, low, close).iloc[-1] < 0:
        neg_count += 1
    if CDLSTALLEDPATTERN(open, high, low, close).iloc[-1] < 0:
        neg_count += 1
    if CDLSTICKSANDWICH(open, high, low, close).iloc[-1] > 0:
        pos_count += 1
    res = CDLTASUKIGAP(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    if CDLTHRUSTING(open, high, low, close).iloc[-1] < 0:
        neg_count += 1
    res = CDLTRISTAR(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    res = CDLUNIQUE3RIVER(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    if CDLUPSIDEGAP2CROWS(open, high, low, close).iloc[-1] < 0:
        neg_count += 1
    res = CDLXSIDEGAP3METHODS(open, high, low, close).iloc[-1]
    if res > 0:
        pos_count += 1
    elif res < 0:
        neg_count += 1
    return neg_count, pos_count