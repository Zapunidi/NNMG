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


ticks = round(second2tick(1/8, 480, 500000))
number_file = 0
for root, dirs, files in os.walk("CutData/Classic"):
    for file in files:
        if (os.path.splitext(file)[1] == ".mid" or os.path.splitext(file)[1] == ".midi"):
            number_file += 1
            print(number_file, end="\r")

            try:
                midi = MidiFile(os.path.join(root, file))

                newMidi = MidiFile()
                for track in midi.tracks[:]:
                    newTrack = MidiTrack()
                    for msg in track:
                        # Устанавливаем время.
                        msg.time = ticks
                    newMidi.tracks.append(newTrack)

                path = os.path.join("WithoutTimeData", pathWithoutFirstFolder(root))
                createPath(path)
                newMidi.save(os.path.join(path, file))

            except:
                pass

input("Complete!")

