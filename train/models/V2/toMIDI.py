import json
from mido import MidiFile, MidiTrack, Message


melody = json.load(open("melody.json", "r"))


track = MidiTrack()
for message in melody:
    if message[0] == 1:
        track.append(Message("note_on", note=12*message[2]+24+message[1], velocity=127, time=message[3]))

    if message[0] == 0:
        track.append(Message("note_off", note=12*message[2]+24+message[1], velocity=127, time=message[3]))


midi = MidiFile()
midi.tracks.append(track)
midi.save("melody.mid")


