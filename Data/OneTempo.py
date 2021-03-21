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
for root, dirs, files in os.walk("WithoutMetaMessageData"):
    for file in files:
        if (os.path.splitext(file)[1] == ".mid" or os.path.splitext(file)[1] == ".midi"):
            number_file += 1
            print(number_file, end="\r")

            try:
                midi = MidiFile(os.path.join(root, file))
                ticks_per_beat = midi.ticks_per_beat  # 480
                tempo = midi.tracks[0][0].tempo  # 500000

                newMidi = MidiFile()
                for track in midi.tracks[1:]:
                    newTrack = MidiTrack()
                    for msg in track:
                        # Время в секундах не зависит от ticks_per_beat и tempo
                        msg.time = round(second2tick(tick2second(msg.time, ticks_per_beat, tempo), 480, 500000))
                        newTrack.append(msg)
                    newMidi.tracks.append(newTrack)

                path = os.path.join("OneTempoData", pathWithoutFirstFolder(root))
                createPath(path)
                newMidi.save(os.path.join(path, file))

            except:
                pass

input("Complete!")

