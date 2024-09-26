import pyaudio 
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
    
    def newChord(self, root, tonality, extensions):
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

