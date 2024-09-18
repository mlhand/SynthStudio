import audiogen

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

        return chord
    
    def getChordHertz(self): 
        midiChord = self.getChordMidi()
        freqChord = []
        for val in midiChord:
            freqChord.append(self.convertMidiToFreq(val))
            
        return freqChord

    def convertMidiToFreq(self, midiVal):
        return 440 * (2 ** ((midiVal - 69)/12))


cG = ChordGenerator("Db", "m", ["7"])
print(cG.getChordMidi())
print(cG.getChordHertz())

audiogen.sampler.play(audiogen.tone(440))
audiogen.crop