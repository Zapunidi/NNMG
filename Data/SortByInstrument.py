import os
from mido import MidiFile, MidiTrack, Message


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


# Отдельный класс для инструмента.
class Instrument(object):
    def __init__(self):
        self.track = MidiTrack()
        self.program = None

        self.currentNote = []
        self.firstNote = True
        self.time = 0

    def setProgram(self, program):
        self.program = program
        self.track.append(Message("program_change", program=program, time=0))

    def addMessage(self, msg, globalTime):
        if self.firstNote:
            msg.time = 0
            self.time = globalTime
        else:
            msg.time = globalTime-self.time
            self.time += msg.time


        if msg.type == "control_change":
            if msg.control == 120 or msg.control == 123:
                for note in self.currentNote:
                    self.track.append(Message("note_off", channel=0, note=note, time=msg.time))
                self.currentNote = []
            if msg.control == 64:
                if msg.value <= 63:
                    for note in self.currentNote:
                        self.track.append(Message("note_off", channel=0, note=note, time=msg.time))
                    self.currentNote = []

        if msg.type == "note_off":
            if msg.note in self.currentNote:
                self.track.append(Message("note_off", channel=0, note=msg.note, time=msg.time))
                self.currentNote.remove(msg.note)


        if msg.type == "note_on":
            if msg.velocity != 0:
                if msg.note in self.currentNote:
                    self.track.append(Message("note_off", channel=0, note=msg.note, time=msg.time))
                    self.track.append(Message("note_on", channel=0, note=msg.note, time=0))
                else:
                    self.track.append(Message("note_on", channel=0, note=msg.note, time=msg.time))
                    self.currentNote.append(msg.note)
            else:
                if msg.note in self.currentNote:
                    self.track.append(Message("note_off", channel=0, note=msg.note, time=msg.time))
                    self.currentNote.remove(msg.note)

            if self.firstNote:
                self.firstNote = False

    def save(self, path, startTrack):
        if len(self.track) >= 50:
            if self.program is not None:
                path = os.path.join(path, str(self.program))
                createPath(path)

                midi = MidiFile()
                midi.tracks.append(startTrack)
                midi.tracks.append(self.track)
                midi.save(os.path.join(path, str(len(os.listdir(path))) + ".mid"))


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
                    index = i+1

            for i in range(len(self.tracks)):
                self.tracks[i][0].time -= time

            message = self.tracks[index].pop(0)
            message.time = time
            if len(self.tracks[index]) == 0:
                self.tracks.pop(index)
            return message
        else:
            raise StopIteration



folders = ["Classic", "Pop", "Rock"]
folder = folders[0]
print(folder)

number_file = 0
for root, dirs, files in os.walk(os.path.join("WithoutMetaMessageData/MidiWorld", folder)):
    for file in files:
        if os.path.splitext(file)[1] == ".mid" or os.path.splitext(file)[1] == ".midi":
            number_file += 1
            print(number_file, end="\r")

            midi = MidiFile(os.path.join(root, file))
            path = os.path.join("SortData", pathWithoutFirstFolder(root))
            startTrack = midi.tracks[0]

            instruments = [Instrument() for i in range(16)]  # Разделяем по каналам.
            globalTime = 0
            for msg in IteratorMidi(midi.tracks[1:]):
                globalTime += msg.time
                # Барабаны не рассматриваем.
                if msg.type in ["program_change", "note_on", "note_off", "control_change"]:
                    if msg.channel != 10:
                        if msg.type == "program_change":
                            instruments[msg.channel].save(path, startTrack)

                            instruments[msg.channel] = Instrument()
                            instruments[msg.channel].setProgram(msg.program)
                        else:
                            instruments[msg.channel].addMessage(msg, globalTime)

            for instrument in instruments:
                instrument.save(path, startTrack)



input("Complete!")
