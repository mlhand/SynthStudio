import threading
import itertools
import math
import pygame.midi
import time
import keyboard
from ChordGenerator import ChordGenerator

device = 0     # device number in win10 laptop
instrument = 24 # http://www.ccarh.org/courses/253/handout/gminstruments/
volume = 127
wait_time = .05
pygame.midi.init()
player = pygame.midi.Output(device)
player.set_instrument(instrument)

#global quitProgram, minor, currentRoot, seventh, ninth, currentChord

quitProgram = False
currentRoot = "C"
minor = False
seventh = False
ninth = False
currentChord = ChordGenerator("C", "M", [])
notesPlaying = []

def setCurrentRoot(newRoot):
    global currentRoot

    if(currentRoot == newRoot):
        currentChord.flipOctave()
        print("Flipping octaves")

    currentRoot = newRoot
    setCurrentChord()
    playChord()

def playChord():
    for note in notesPlaying: 
        player.note_off(note, volume)

    chord = currentChord.getChordAndStrumPadMidi()[0]
    for note in chord:
        player.note_on(note, volume)
        notesPlaying.append(note)

def setCurrentChord():
    global currentChord
    tonality = "M"
    if (minor == True):
        tonality = "m"
    if (not seventh and not ninth):
        currentChord.newChord(currentRoot, tonality, [])
    elif (seventh and not ninth):
        currentChord.newChord(currentRoot, tonality, ["7"])
    elif (not seventh and ninth):
        currentChord.newChord(currentRoot, tonality, ["9"])
    else:
        currentChord.newChord(currentRoot, tonality, ["7", "9"])

def playNote(noteNum):
    chord = currentChord.getChordAndStrumPadMidi()[0] + currentChord.getChordAndStrumPadMidi()[1]
    note = chord[noteNum]
    player.note_on(note, volume)
    time.sleep(wait_time)
    player.note_off(note, volume)

def setMinor():
    global minor
    minor = not minor
    setCurrentChord()

def setSeventh():
    global seventh
    seventh = not seventh
    setCurrentChord()

def setNinth():
    global ninth
    ninth = not ninth
    setCurrentChord()

def changeInstrument(num):
    global instrument
    instrument += num
    player.set_instrument(instrument)

def exitProgram():
    quitProgram = True
    
#Functionality Buttons
keyboard.on_press_key('esc', lambda x: exitProgram())
keyboard.on_press_key('=', lambda x: changeInstrument(1))
keyboard.on_press_key('-', lambda x: changeInstrument(-1))

#Chord Selection Buttons
keyboard.on_press_key('q', lambda x: setCurrentRoot("Db"))
keyboard.on_press_key('w', lambda x: setCurrentRoot("Ab"))
keyboard.on_press_key('e', lambda x: setCurrentRoot("Eb"))
keyboard.on_press_key('r', lambda x: setCurrentRoot("Bb"))
keyboard.on_press_key('a', lambda x: setCurrentRoot("F"))
keyboard.on_press_key('s', lambda x: setCurrentRoot("C"))
keyboard.on_press_key('d', lambda x: setCurrentRoot("G"))
keyboard.on_press_key('f', lambda x: setCurrentRoot("D"))
keyboard.on_press_key('z', lambda x: setCurrentRoot("A"))
keyboard.on_press_key('x', lambda x: setCurrentRoot("E"))
keyboard.on_press_key('c', lambda x: setCurrentRoot("B"))
keyboard.on_press_key('v', lambda x: setCurrentRoot("F#"))

#Tonalities
keyboard.on_press_key('m', lambda x: setMinor())
keyboard.on_press_key('k', lambda x: setSeventh())
keyboard.on_press_key('l', lambda x: setNinth())

#Individual Notes
keyboard.on_press_key('1', lambda x: playNote(0))
keyboard.on_press_key('2', lambda x: playNote(1))
keyboard.on_press_key('3', lambda x: playNote(2))
keyboard.on_press_key('4', lambda x: playNote(3))
keyboard.on_press_key('5', lambda x: playNote(4))
keyboard.on_press_key('6', lambda x: playNote(5))
keyboard.on_press_key('7', lambda x: playNote(6))
keyboard.on_press_key('8', lambda x: playNote(7))



while not quitProgram:
    keyboard.wait()
#time.sleep(1000000)


# close the device -------------------------------------------------------------
del player
pygame.midi.quit()