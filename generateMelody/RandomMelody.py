from mido import MidiFile, MidiTrack, Message, second2tick
from random import randint


track = MidiTrack()
ticks = round(second2tick(1/8, 480, 500000))
for i in range(1000):
    message = randint(0, 1)
    note = randint(0, 11)
    octave = randint(0, 7)

    if message == 1:
        track.append(Message("note_on", note=12*octave+24+note, velocity=127, time=ticks))

    if message == 0:
        track.append(Message("note_off", note=12*octave+24+note, velocity=127, time=ticks))


midi = MidiFile()
midi.tracks.append(track)
midi.save("melody.mid")


