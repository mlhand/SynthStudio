import math
import random

def createWavetable(sample_count):
    # To create a sound with a frequency of F, set the sample_count to (sample_rate/F) - 1/2
    high = 1.0
    low = -1.0
    wavetable = []
    for i in range(0, sample_count):
        if random.randint(0, 1) == 1:
            wavetable.append(high)
        else:
            wavetable.append(low)
    return wavetable
    
def karplusStrongCycle(wavetable, soundlength):
    tablelength = len(wavetable)
    currentval = 0
    lastval = 0
    fullwavetable = []
    for i = 0; i < soundlength; i++:
        wavetable[currentval] = wavetable[currentval]/2 + wavetable[lastval]/2
        fullwavetable.append(wavetable[currental])
        lastval = currentval
        currentval = currentval + 1
        if currentval >= tablelength:
            currentval = 0
    return fullwavetable
