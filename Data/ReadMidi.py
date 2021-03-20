from mido import MidiFile


path = "au_22_bar.gp3"
path1 = "test/0.mid"
midi = MidiFile(path1)

for i, track in enumerate(midi.tracks):
    print('Track {}: {} Messages: {}'.format(i, track.name, len(track)))
    for msg in track:
        # if not (msg.is_meta):
        print(msg)
