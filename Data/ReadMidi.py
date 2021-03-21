from mido import MidiFile


path = "WithoutMetaMessageData/Classic/beeth9-2.mid"
path1 = "test.mid"
midi = MidiFile(path)
midi1 = MidiFile(path1)

print(midi.length)
print(midi1.length)

for i, track in enumerate(midi.tracks):
    print('Track {}: {} Messages: {}'.format(i, track.name, len(track)))
    for msg in track:
        # if not (msg.is_meta):
        print(msg)
