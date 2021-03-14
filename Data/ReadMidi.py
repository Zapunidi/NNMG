from mido import MidiFile


mid = MidiFile("RawData\MidiWorld\Pop\Ace_of_Base_-_All_That_She_Wants.mid")


for i, track in enumerate(mid.tracks):
    print('Track {}: {}'.format(i, track.name))
    for msg in track:
        print(msg)

