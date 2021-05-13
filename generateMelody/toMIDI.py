import json
from mido import MidiFile, MidiTrack, Message, second2tick


melody = json.load(open("melody.json", "r"))


track = MidiTrack()
ticks = round(second2tick(1/8, 480, 500000))
for message in melody:
    if message[0] == 1:
        track.append(Message("note_on", note=12*message[2]+24+message[1], velocity=127, time=ticks))

    if message[0] == 0:
        track.append(Message("note_off", note=12*message[2]+24+message[1], velocity=127, time=ticks))


midi = MidiFile()
midi.tracks.append(track)
midi.save("melody.mid")


