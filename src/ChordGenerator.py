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

    def buildChord(self, midiVal, chordArray):
            chord = []
            for i in range(3):
                chord.append(midiVal + chordArray[i])

            if "7" in self.extensions:
                chord.append(midiVal + chordArray[3])

            if "9" in self.extensions:
                chord.append(midiVal + chordArray[4])
            
            return chord

    def getChordMidi(self): 
        midiVal = self.circleOfFifths.get(self.root)
        chord = []
        if self.tonality == "M": # build out major chord
            chord = self.buildChord(midiVal, self.majorChord)

        elif self.tonality == "m": # build out minor chord
            chord = self.buildChord(midiVal, self.minorChord)
        
        strumNotes = self.getStrumPadNotes()
        return (chord, strumNotes)
    
    def getChordHertz(self): 
        midiChord, strumNotes = self.getChordMidi() # convert midi to freq
        freqChord = []
        freqStrum = []

        for val in midiChord:
            freqChord.append(self.convertMidiToFreq(val))

        for val in strumNotes:
            freqStrum.append(self.convertMidiToFreq(val))

        return (freqChord, freqStrum)

    def convertMidiToFreq(self, midiVal):
        return math.floor(440 * (2 ** ((midiVal - 69)/12))) #TODO: DISCUSS FLOOR VS CEIL

    def getStrumPadNotes(self):
        midiVal = self.circleOfFifths.get(self.root)
        strumNotes = []
        additive = 0
        octave = 12
        for i in range(8): # to be discussed how many notes to have
            strumNotes.append(midiVal + additive + octave)
            additive = additive + 3 # build up in thirds
        
        return strumNotes



cG = ChordGenerator("Db", "M", ["7", "9"])
print(cG.getChordMidi())
print(cG.getChordHertz())

# p = pyaudio.PyAudio() # instantiate pyAudio or else it does not work

# def playNoteThread(freq):
#     audiogen.sampler.play(audiogen.tone(frequency=freq))


# def playChord(chord):
#     listOfThreads = []

#     for note in chord:
#         print("starting thread for", note)
#         thread = threading.Thread(target=playNoteThread, args=(note,))
#         listOfThreads.append(thread)
#         thread.start()
#     return listOfThreads

# playChord(cG.getChordHertz())

