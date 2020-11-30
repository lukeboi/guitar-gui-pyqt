import time
import rtmidi

midiout = rtmidi.MidiOut()

def init():
    print()
    # midiout = rtmidi.MidiOut()


def play_note(n):
    note_on = [0x90, n, 100]  # channel 1, note n, velocity 100
    midiout.send_message(note_on)
    # note_off = [0x90, n, 100]
    # midiout.send_message(note_off)

def destroy_midi_out():
    print()
    del midiout
