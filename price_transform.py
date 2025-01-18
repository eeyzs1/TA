
from talib import  AVGPRICE,MEDPRICE,TYPPRICE,WCLPRICE

def calculate_price(open, high, low, close):
    # real = AVGPRICE(open, high, low, close)

    ### MEDPRICE - Median Price
    # real = MEDPRICE(high, low)

    ### TYPPRICE - Typical Price
    # real = TYPPRICE(high, low, close)

    ### WCLPRICE - Weighted Close Price
    # at this moment, seems only this is needed
    return WCLPRICE(high, low, close)