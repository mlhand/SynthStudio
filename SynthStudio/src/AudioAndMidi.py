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

gpioPinChords = [(7, lambda func: chordButtonCallBack("Db")), (11, lambda func: chordButtonCallBack("Ab")),
                 (12, lambda func: tonalityButtonCallBack()),
                 (13, lambda func: extensionButtonCallBack("7")), (15, lambda func: extensionButtonCallBack("9"))] # used to track gpio pins to their chord

# set the output device
player = pygame.midi.Output(device)
# set the instrument 
player.set_instrument(instrument)

# states to track
notesPlaying = [] # used to stop all notes when changing chords 
tonality = "M" # toggle change when button is pressed
extensions = [] # added when 7 or 9 is toggeled


def playNotes(notes):
    for note in notes:
        player.note_on(note, volume)


def stopNotes(notes):
    for note in notes:
        player.note_off(note, volume)


# necessary functions for playback
def chordButtonCallBack(chord):

    # stop all notes playing right now to prevent overlap
    stopNotes(notesPlaying)

    print("Playing", chord, extensions, tonality)
    cG.newChord(chord, tonality, extensions) # construct a new chord

    # play new chord
    cG.newChord(chord, tonality, extensions)
    playNotes(cG.getChordAndStrumPadMidi()[0])


def tonalityButtonCallBack():
    global tonality
    if tonality == "M":
        tonality = "m"
    else:
        tonality = "M"

    print("New tonality", tonality)

def extensionButtonCallBack(extension):
    global extensions
    if extension in extensions:
        extensions.remove(extension)
    else:
        extensions.append(extension)

    print("New extensions", extensions)


def exit(player):
    GPIO.cleanup()
    del player
    pygame.midi.quit()


def initChordGPIOs(): # TODO: add rest of buttons
    for pinAndChord in gpioPinChords:
        GPIO.setup(pinAndChord[0], GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set to read input pin and as a pull down resistor
        GPIO.add_event_detect(pinAndChord[0], GPIO.RISING, callback=pinAndChord[1], bouncetime=200) # Setup event on pin on rising edge

if __name__=="__main__":

    initChordGPIOs()

    try:
        print("Press the button to test. Ctrl+C to exit.")
        while True:
            time.sleep(1)  # Delay for a short period

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        GPIO.cleanup()  # Clean up GPIO settings
        exit(player)    # close the device 
            
