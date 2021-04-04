from mido import MidiFile


path = "CutData/Classic/2.mid"
midi = MidiFile(path)


for i, track in enumerate(midi.tracks):
    print('Track {}: {} Messages: {}'.format(i, track.name, len(track)))
    for msg in track:
        # if not (msg.is_meta):
        print(msg)
