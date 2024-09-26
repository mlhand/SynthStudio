import pygame.midi
import time
from ChordGenerator import ChordGenerator
import RPi.GPIO as GPIO

device = 0      # output device for 3.5mm once config using alsamixer
instrument = 24 # http://www.ccarh.org/courses/253/handout/gminstruments/
volume = 127
wait_time = 3

# init Chord Generator, pygame, and RPi.GPIO
cG = ChordGenerator("Db", "m", ["7", "9"]) # instantiate chord generator 
pygame.midi.init()
GPIO.setmode(GPIO.BOARD) # init to use board GPIO numbers for consistency across boards

gpioPinChords = [(10, "Db")] # used to track gpio pins to their chord

# set the output device
player = pygame.midi.Output(device)
# set the instrument 
player.set_instrument(instrument)

# states to track
notesPlaying = [] # used to stop all notes when changing chords 
tonality = "M" # toggle change when button is pressed
extensions = [] # added when 7 or 9 is held down


def playNotes(notes):
    for note in notes:
        player.note_on(note, volume)


def stopNotes(notes):
    for note in notes:
        player.note_off(note, volume)


# necessary functions for playback
def chordButtonCallBack(chord, tonality, extensions):
    # stop all notes playing right now to prevent overlap
    stopNotes(notesPlaying)

    # play new chord
    cG.newChord(chord, tonality, extensions)
    playNotes(cG.getChordAndStrumPadMidi()[0])


def exit(player):
    GPIO.cleanup()
    del player
    pygame.midi.quit()


def initGPIOs(): # TODO: add rest of buttons
    for pinAndChord in gpioPinChords:
        GPIO.setup(pinAndChord[0], GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to read input pin and as a pull down resistor
        GPIO.add_event_detect(pinAndChord[0], GPIO.RISING,callback=lambda func: chordButtonCallBack(pinAndChord[1], tonality, extensions)) # Setup event on pin 10 rising edge and play Chord Db


if __name__=="__main__":

    initGPIOs()

    # read and wait for input
    message = input("Press enter to quit\n\n") # Run until someone presses enter
        
    # close the device 
    exit(player)

