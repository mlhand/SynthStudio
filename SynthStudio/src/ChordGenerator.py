import audiogen
import pyaudio 

import threading
import time
import itertools

import math

class ChordGenerator: # passes back chord with tonality and extension(s) based on button

    majorChord = [0, 4, 7, 11, 14] 
    minorChord = [0, 3, 7, 10, 14]
    middleC = 60

    layout = {} # dict tracking ids and chords
    
    # chord roots to midi value
    circleOfFifths = {"Db": 61, "Ab": 56, "Eb": 58, "Bb": 65, "F": 60, "C": 67, "G": 62, "D": 62, "A": 57, "E": 64, "B": 59, "F#": 54}

    def __init__(self, root, tonality, extensions):
        self.root = root
        self.tonality = tonality
        self.extensions = extensions

    def buildChord(self, midiVal, chordArray): #returns chord and strumNotes
            chord = []
            strumNotes = []
            for i in range(3):
                chord.append(midiVal + chordArray[i])

            for ocatve in range(1, 3):
                for note in range(3):
                    strumNotes.append(midiVal + chordArray[note] + 12*ocatve)

            if "7" in self.extensions:
                chord.append(midiVal + chordArray[3])

            if "9" in self.extensions:
                chord.append(midiVal + chordArray[4])
            
            return (chord, strumNotes)

    def getChordAndStrumPadMidi(self): 
        midiVal = self.circleOfFifths.get(self.root)
        chord = []
        strumNotes = []
        if self.tonality == "M": # build out major chord
            return self.buildChord(midiVal, self.majorChord)

        elif self.tonality == "m": # build out minor chord
            return self.buildChord(midiVal, self.minorChord)
            
    def getChordAndStrumPadHertz(self): 
        midiChord, strumNotes = self.getChordAndStrumPadMidi() # convert midi to freq
        freqChord = []
        freqStrum = []

        for val in midiChord:
            freqChord.append(self.convertMidiToFreq(val))

        for val in strumNotes:
            freqStrum.append(self.convertMidiToFreq(val))

        return (freqChord, freqStrum)

    def convertMidiToFreq(self, midiVal):
        return math.floor(440 * (2 ** ((midiVal - 69)/12))) #TODO: DISCUSS FLOOR VS CEIL


cG = ChordGenerator("Db", "m", ["7", "9"])
print(cG.getChordAndStrumPadMidi())
print(cG.getChordAndStrumPadHertz())

# import library 
import pygame.midi
import time

device = 0     # device number in win10 laptop
instrument = 24 # http://www.ccarh.org/courses/253/handout/gminstruments/
volume = 127
wait_time = 3

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

