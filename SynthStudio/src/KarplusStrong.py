import math
import random
import numpy as np
import pygame

def createWavetable(sample_count):
    # To create a sound with a frequency of F, set the sample_count to (sample_rate/F) - 1/2
    # The default PyGame sample rate is 44100Hz
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
    for i in range(soundlength):
        wavetable[currentval] = wavetable[currentval]/2 + wavetable[lastval]/2
        fullwavetable.append(wavetable[currentval])
        lastval = currentval
        currentval = currentval + 1
        if currentval >= tablelength:
            currentval = 0
    return fullwavetable
    
def createSound(frequency, length = 6):
    freqlength = length * 44100
    wavetable = createWavetable(44100//frequency)
    buffer = np.array(karplusStrongCycle(wavetable, freqlength)).astype(np.float32)
    sound = pygame.mixer.Sound(buffer)
    sound.play(0)
    # pygame.time.wait(int(sound.get_length() * 1000)) # Is this necessary?
    
    

pygame.mixer.init(size=32, channels=1)

createSound(440)
