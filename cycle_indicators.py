
from talib import HT_DCPERIOD,HT_DCPHASE,HT_PHASOR,HT_SINE,HT_TRENDMODE

def cycle_indicators_calculations(close):
    ### HT_DCPERIOD - Hilbert Transform - Dominant Cycle Period
    period = HT_DCPERIOD(close)
    ### HT_DCPHASE - Hilbert Transform - Dominant Cycle Phase
    real = HT_DCPHASE(close)

    ### HT_PHASOR - Hilbert Transform - Phasor Components
    inphase, quadrature = HT_PHASOR(close)

    ### HT_SINE - Hilbert Transform - SineWave
    sine, leadsine = HT_SINE(close)

    ### HT_TRENDMODE - Hilbert Transform - Trend vs Cycle Mode,=0 is cycle, =1 is trend
    integer = HT_TRENDMODE(close)

    print("period~~~~~~~~~~~~~~~~")
    print(period)
    print("real~~~~~~~~~~~~~~~~")
    print(real)
    print("inphase@@@@@@@@@@@@@@")
    print(inphase, quadrature )
    print("sine$$$$$$$$$$$$$$$$$$$$$$")
    print(sine, leadsine)
    print("integer&&&&&&&&&&&&&&&&&&&&&&&&&")
    print(integer)