from mido import MidiFile, MidiTrack, Message, tick2second, second2tick
import os



# Создает путь, если его нет.
def createPath(path):
    head, tail = os.path.split(path)

    if ((not os.path.exists(head)) or os.path.isfile(head)) and head != "":
        createPath(head)

    if ((not os.path.exists(path)) or os.path.isfile(path)) and path != "":
        os.mkdir(path)


# Возвращает путь без первого
def pathWithoutFirstFolder(path):
    folders = []
    while path != "":
        path, tail = os.path.split(path)
        if tail != "":
            folders.append(tail)
    folders.reverse()

    return os.path.join(*folders[1:])


number_file = 0
for root, dirs, files in os.walk("OneTrackOneChannelData"):
    for file in files:
        if (os.path.splitext(file)[1] == ".mid" or os.path.splitext(file)[1] == ".midi"):
            number_file += 1
            print(number_file, end="\r")

            try:
                midi = MidiFile(os.path.join(root, file))

                newMidi = MidiFile()
                for track in midi.tracks:
                    newTrack = MidiTrack()
                    for msg in track:
                        if msg.type == "note_off" or msg.type == "note_on":
                            msg.note = msg.note % 12 + 60
                        newTrack.append(msg)
                    newMidi.tracks.append(newTrack)

                path = os.path.join("OneOctaveData", pathWithoutFirstFolder(root))
                createPath(path)
                newMidi.save(os.path.join(path, file))

            except:
                pass

input("Complete!")



