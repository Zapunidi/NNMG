from mido import MidiFile


path = "WithoutMetaMessageData/MidiWorld/Pop/ABBA_-_Gimme_Gimme_Gimme.mid"
path1 = "test/0/0.mid"
midi = MidiFile(path1)


# print(midi.length)

for i, track in enumerate(midi.tracks):
    print('Track {}: {} Messages: {}'.format(i, track.name, len(track)))
    for msg in track:
        # if not (msg.is_meta):
        print(msg)
