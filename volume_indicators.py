
import talib



# neg means downward trend, pos upward, 0 unrelated
def calculate_overlap_for_tech(open, high, low, close):
    neg_count = 0
    pos_count = 0
    neu_count = 0
    integer = talib.CDL2CROWS(open, high, low, close)
    print(type(integer))
    print(integer.iloc[-1])
    return integer