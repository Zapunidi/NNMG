from mido import MidiFile, MidiTrack, Message, second2tick
from random import randint


track = MidiTrack()
second = round(second2tick(1, 480, 500000))
for i in range(1000):
    message = randint(0, 1)
    note = randint(36, 96)
    ticks = randint(0, second)

    if message == 1:
        track.append(Message("note_on", note=note, velocity=127, time=ticks))

    if message == 0:
        track.append(Message("note_off", note=note, velocity=127, time=ticks))


midi = MidiFile()
midi.tracks.append(track)
midi.save("melody.mid")


