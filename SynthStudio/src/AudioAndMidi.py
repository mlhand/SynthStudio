# import library 
import pygame.midi
import time
from ChordGenerator import ChordGenerator

device = 0      # device number in win10 laptop
instrument = 24 # http://www.ccarh.org/courses/253/handout/gminstruments/
volume = 127
wait_time = 3

cG = ChordGenerator("Db", "m", ["7", "9"]) # instantiate chord generator 
print(cG.getChordAndStrumPadMidi())
print(cG.getChordAndStrumPadHertz())

pygame.midi.init()

# set the output device
player = pygame.midi.Output(device)

# set the instrument 
player.set_instrument(instrument)

# play the notes in chord

for note in cG.getChordAndStrumPadMidi()[0]:
    player.note_on(note, volume)

time.sleep(wait_time)

for note in cG.getChordAndStrumPadMidi()[0]:
    player.note_off(note, volume)

# close the device -------------------------------------------------------------
del player
pygame.midi.quit()

