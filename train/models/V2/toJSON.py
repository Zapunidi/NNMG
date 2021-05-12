from mido import MidiFile, MidiTrack, Message, tick2second, second2tick
import os
import json


dataMessages = []
dataValues = []
dataOctaves = []
dataDTs = []

number_file = 0
for root, dirs, files in os.walk("OneTrackOneChannelData/maestro"):
    for file in files:
        if (os.path.splitext(file)[1] == ".mid" or os.path.splitext(file)[1] == ".midi"):
            number_file += 1
            print(number_file, end="\r")

            try:
                midi = MidiFile(os.path.join(root, file))
                track = midi.tracks[0]  # В файле всего один трек

                messages = []
                values = []
                octaves = []
                DTs = []

                for msg in track:
                    if msg.time > 200:
                        dataMessages.append(messages)
                        dataValues.append(values)
                        dataOctaves.append(octaves)
                        dataDTs.append(DTs)
                        messages = []
                        values = []
                        octaves = []
                        DTs = []

                        msg.time = 0

                    if msg.type == "note_off":
                        if 24 <= msg.note <= 119:
                            messages.append(0)
                            values.append(msg.note%12)
                            octaves.append(msg.note//12-2)
                            DTs.append(msg.time)

                    if msg.type == "note_on":
                        if 24 <= msg.note <= 119:
                            messages.append(1)
                            values.append(msg.note%12)
                            octaves.append(msg.note//12-2)
                            DTs.append(msg.time)

                dataMessages.append(messages)
                dataValues.append(values)
                dataOctaves.append(octaves)
                dataDTs.append(DTs)
            except:
                print("Corrupt file: "+str(number_file))



file = open("dataMessages.json", "w")
file.write(json.dumps(dataMessages))
file.close()

file = open("dataValues.json", "w")
file.write(json.dumps(dataValues))
file.close()

file = open("dataOctaves.json", "w")
file.write(json.dumps(dataOctaves))
file.close()

file = open("dataDTs.json", "w")
file.write(json.dumps(dataDTs))
file.close()

input("Complete!")


