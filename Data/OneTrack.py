import os
from mido import MidiFile, MidiTrack


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



# Итератор файла миди одновременно по всем трекам.
class IteratorMidi(object):
    def __init__(self, tracks):
        self.tracks = tracks

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.tracks) != 0:
            index = 0
            time = self.tracks[0][0].time
            for i, track in enumerate(self.tracks[1:]):
                if track[0].time < time:
                    time = track[0].time
                    index = i + 1

            for i in range(len(self.tracks)):
                self.tracks[i][0].time -= time

            message = self.tracks[index].pop(0)
            message.time = time
            if len(self.tracks[index]) == 0:
                self.tracks.pop(index)
            return message
        else:
            raise StopIteration



number_file = 0
for root, dirs, files in os.walk("OneTempoData"):
    for file in files:
        if (os.path.splitext(file)[1] == ".mid" or os.path.splitext(file)[1] == ".midi"):
            number_file += 1
            print(number_file, end="\r")

            path = os.path.join(os.path.join("OneTrackData", pathWithoutFirstFolder(root)))

            midi = MidiFile(os.path.join(root, file))
            createPath(path)

            oneTrackMidi = MidiFile()
            track = MidiTrack()
            # Цикл по всем сообщениям
            for msg in IteratorMidi(midi.tracks):
                track.append(msg)
            oneTrackMidi.tracks.append(track)
            oneTrackMidi.save(os.path.join(path, file))


input("Complete!")
