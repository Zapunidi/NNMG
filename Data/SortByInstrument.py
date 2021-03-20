import os
from mido import MidiFile, MidiTrack, Message, tick2second, second2tick


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


# Отдельный класс для инструмента.
class Instrument(object):
    def __init__(self, tempo, ticks_per_beat):
        self.track = MidiTrack()
        self.notes = []
        self.program = None

        # ВременнЫе характеристики
        self.tempo = tempo
        self.ticks_per_beat = ticks_per_beat

        self.currentNote = {}
        self.firstNote = True
        self.time = 0

    # Устновка номера инструмента.
    def setProgram(self, program):
        self.program = program
        self.track.append(Message("program_change", program=program, time=0))

    # Добавляем ноты особым образом
    def addMessage(self, msg, globalTime):
        # Если первая нота, то делаем ее в самом начале
        if self.firstNote:
            msg.time = 0
            self.time = globalTime
        else:
            msg.time = globalTime - self.time
            self.time += msg.time


        for note in self.currentNote.keys():
            self.currentNote[note] += msg.time


        def add_note_on(note, time):
            self.track.append(Message("note_on", channel=0, note=note, time=time))
            self.currentNote.update({note: 0})

        def add_note_off(note, time, permission=True):
            self.track.append(Message("note_off", channel=0, note=note, time=time))
            if permission:
                self.currentNote.pop(note)

        # Нам нужны только сообщения note_on и note_off
        if msg.type == "control_change":
            if msg.control == 120 or msg.control == 123:
                for note in self.currentNote:
                    add_note_off(note, msg.time, False)
                self.currentNote = {}
            if msg.control == 64:
                if msg.value <= 63:
                    for note in self.currentNote:
                        add_note_off(note, msg.time, False)
                    self.currentNote = {}

        if msg.type == "note_off":
            if msg.note in self.currentNote:
                add_note_off(msg.note, msg.time)

        if msg.type == "note_on":
            if msg.velocity != 0:
                if msg.note in self.currentNote:
                    add_note_off(msg.note, msg.time)
                    add_note_on(msg.note, 0)
                else:
                    add_note_on(msg.note, msg.time)
            else:
                if msg.note in self.currentNote:
                    add_note_off(msg.note, msg.time)

            if self.firstNote:
                self.firstNote = False

    # Сохраняем дорожку инструмента в файл
    def save(self, path, startTrack):
        def saveTrack(track):
            midi = MidiFile()
            midi.tracks.append(startTrack)

            while track[1].type != "note_on" and len(track) > 3:
                track.pop(1)
            midi.tracks.append(track)

            if midi.length > 10 and midi.length < 60:
                createPath(path)
                midi.save(os.path.join(path, str(len(os.listdir(path))) + ".mid"))

        if self.program is not None:
            track = MidiTrack()
            track.append(Message("program_change", program=self.program, time=0))
            for msg in self.track:
                # Режем трек, если между командами разница больше, чем 2c
                if tick2second(msg.time, self.ticks_per_beat, self.tempo) > 2:
                    saveTrack(track)

                    track = MidiTrack()
                    track.append(Message("program_change", program=self.program, time=0))
                    msg.time = 0

                track.append(msg)
            saveTrack(track)



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
for root, dirs, files in os.walk("WithoutMetaMessageData/MidiWorld"):
    for file in files:
        if (os.path.splitext(file)[1] == ".mid" or os.path.splitext(file)[1] == ".midi"):
            number_file += 1
            print(number_file, end="\r")
            
            # try:
            path = os.path.join(os.path.join("SortData", pathWithoutFirstFolder(root), os.path.splitext(file)[0]))

            midi = MidiFile(os.path.join(root, file))
            createPath(path)
            midi.save(os.path.join(path, file))

            instruments = [Instrument(midi.tracks[0][0].tempo, midi.ticks_per_beat) for i in range(16)]  # Разделяем по каналам.
            # Цикл по всем сообщениям
            globalTime = 0
            for msg in IteratorMidi(midi.tracks[1:]):
                globalTime += msg.time
                if msg.type in ["program_change", "note_on", "note_off", "control_change"]:
                    if msg.channel != 10:
                        # Барабаны не рассматриваем.
                        if msg.type == "program_change":
                            instruments[msg.channel].save(path, midi.tracks[0])

                            instruments[msg.channel] = Instrument(midi.tracks[0][0].tempo, midi.ticks_per_beat)
                            instruments[msg.channel].setProgram(msg.program)
                        else:
                            instruments[msg.channel].addMessage(msg, globalTime)

            for instrument in instruments:
                instrument.save(path, midi.tracks[0])
            # except:
            #     pass



input("Complete!")
