from mido import MidiFile


path = "CutData/Classic/12887.mid"
midi = MidiFile(path)

print(len(midi.tracks))
for i, track in enumerate(midi.tracks):
    print('Track {}: {} Messages: {}'.format(i, track.name, len(track)))
    for msg in track:
        # if not (msg.is_meta):
        print(msg)
