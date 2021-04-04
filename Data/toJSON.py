from mido import MidiFile, MidiTrack, Message, tick2second, second2tick
import os
import json


dataArray = []

number_file = 0
for root, dirs, files in os.walk("CutData/Classic"):
    for file in files:
        if (os.path.splitext(file)[1] == ".mid" or os.path.splitext(file)[1] == ".midi"):
            number_file += 1
            print(number_file, end="\r")

            try:
                midi = MidiFile(os.path.join(root, file))
                track = midi.tracks[0]  # В файле всего один трек

                data = []          # message, note, time
                for msg in track:
                    if msg.type == "note_on":
                        data.append([1, msg.note, msg.time])

                    if msg.type == "note_off":
                        data.append([0, msg.note, msg.time])

                dataArray.append(data)
            except:
                print("Corrupt file: "+str(number_file))



file = open("dataArray.json", "w")
file.write(json.dumps(dataArray))
input("Complete!")


