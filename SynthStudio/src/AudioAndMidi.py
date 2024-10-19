import pygame.midi
import time
from ChordGenerator import ChordGenerator
import RPi.GPIO as GPIO
from gpiozero import MCP3008 # MUST FOLLOW THIS SET UP https://projects.raspberrypi.org/en/projects/physical-computing/13
from KarplusStrong import createSound # used when not on midi

device = 0      # output device for 3.5mm once config using alsamixer
instrument = 24 # http://www.ccarh.org/courses/253/handout/gminstruments/
volume = 127
wait_time = 3
NUM_STRUMPAD_NOTES = 5
isMidi = False # TODO: FIND HOW TO SET THIS VALUE

# init Chord Generator, pygame, and RPi.GPIO
cG = ChordGenerator("Db", "m", ["7", "9"]) # instantiate chord generator 
pygame.midi.init()
GPIO.setmode(GPIO.BOARD) # init to use board GPIO numbers for consistency across boards

gpioPinChords = [(7, lambda func: chordButtonCallBack("Db")), (8, lambda func: stopNotesCallBack()), (11, lambda func: chordButtonCallBack("Ab")),
                 (12, lambda func: tonalityButtonCallBack()),
                 (13, lambda func: extensionButtonCallBack("7")), (15, lambda func: extensionButtonCallBack("9")),
                 (38, lambda func: instrumentCallBack(-1)), (40, lambda func: instrumentCallBack(1))] # used to track gpio pins to their chord

# set the output device
player = pygame.midi.Output(device)
# set the instrument 
player.set_instrument(instrument)

# states to track
notesPlaying = [] # used to stop all notes when changing chords
tonality = "M" # toggle change when button is pressed
extensions = [] # added when 7 or 9 is toggeled


def playNotes(notes):
    global notesPlaying
    for note in notes:
        player.note_on(note, volume)
    
    notesPlaying = notes


def stopNotes(notes):
    global notesPlaying
    for note in notes:
        player.note_off(note, volume)
    
    notesPlaying = []


# necessary functions for playback

def instrumentCallBack(num):
    global instrument
    global isMidi

    if(not isMidi):
        instrument += num

        # protect against the under and overflow
        if(instrument > 127):
            instrument = 0
        if(instrument < 0):
            instrument = 127

        print(instrument)
        player.set_instrument(instrument)


def stopNotesCallBack():
    global notesPlaying
    print("Was playing.")
    print(notesPlaying)

    print("Stopping notes.")
    stopNotes(notesPlaying)
    print(notesPlaying)


def chordButtonCallBack(chord):

    # stop all notes playing right now to prevent overlap
    stopNotes(notesPlaying)

    print("Playing", chord, extensions, tonality)
    cG.newChord(chord, tonality, extensions) # construct a new chord

    # play new chord
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


def handleTouchPad(value):
    global isMidi

    print(f"Integer ADC Value: {value}")
    touchPadNotes = cG.getChordAndStrumPadMidi()[1]
    print(touchPadNotes)
    
    if value < len(touchPadNotes):  # Ensure the value is within range
        print(touchPadNotes[value])
        note = touchPadNotes[value]

        if(isMidi):
            player.note_on(note, volume)
        else: # play with Karplus strong if not midi, 
            createSound(cG.convertMidiToFreq(note)) # convert to frequency 


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
    pot = MCP3008(0) # linear soft pot on channel 0
    prevValue = round(pot.value * NUM_STRUMPAD_NOTES) # convert to 8 range 

    try:
        print("Press buttons to test. Ctrl+C to exit.")
        while True:
            value = round(pot.value * NUM_STRUMPAD_NOTES)
            changed = value != prevValue

            if(changed):                
                handleTouchPad(value)

            prevValue = value 
            time.sleep(0.1)  # Delay for a short period

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        GPIO.cleanup()  # Clean up GPIO settings
        exit(player)    # close the device 
            
