import math
import random

def createWavetable(sample_count):
    high = 1.0
    low = -1.0
    wavetable = []
    for i in range(0, sample_count):
        if random.randint(0, 1) == 1:
            wavetable.append(high)
        else:
            wavetable.append(low)
    return wavetable