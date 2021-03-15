import os
from mido import MidiFile, MidiTrack, MetaMessage



def createPath(path):
    head, tail = os.path.split(path)

    if ((not os.path.exists(head)) or os.path.isfile(head)) and head != "":
        createPath(head)

    if ((not os.path.exists(path)) or os.path.isfile(path)) and path != "":
        os.mkdir(path)


def pathWithoutFirstFolder(path):
    folders = []
    while path != "":
        path, tail = os.path.split(path)
        if tail != "":
            folders.append(tail)
    folders.reverse()

    return os.path.join(*folders[1:])

folders = ["Classic", "Pop", "Rock"]
folder = folders[2]
print(folder)

number_file = 0
for root, dirs, files in os.walk(os.path.join("RawData/MidiWorld", folder)):
    for file in files:
        if os.path.splitext(file)[1] == ".mid" or os.path.splitext(file)[1] == ".midi":
            number_file += 1
            print(number_file, end="\r")


            try:
                midi = MidiFile(os.path.join(root, file))

                newMidi = MidiFile()
                track0 = MidiTrack()
                newMidi.tracks.append(track0)
                for track in midi.tracks:
                    newTrack = MidiTrack()

                    messages = 0
                    for msg in track:
                        if not msg.is_meta:
                            newTrack.append(msg)
                            messages += 1
                    if messages != 0:
                        newMidi.tracks.append(newTrack)
                track0.append(MetaMessage("set_tempo", tempo=int(500000/newMidi.length*midi.length), time=0))

                path = os.path.join("WithoutMetaMessageData", pathWithoutFirstFolder(root))
                createPath(path)
                newMidi.save(os.path.join(path, file))
            except:
                pass

input("Complete!")
