from mido import MidiFile, MidiTrack, Message, tick2second, second2tick
import os
import numpy as np


number_file = 0
delete_file = 0
for root, dirs, files in os.walk("CutData/Classic"):
    for file in files:
        if (os.path.splitext(file)[1] == ".mid" or os.path.splitext(file)[1] == ".midi"):
            number_file += 1
            print("Current file: {}  Delete files: {}".format(number_file, delete_file), end="\r")

            try:
                notes = np.asarray([False]*12)

                midi = MidiFile(os.path.join(root, file))
                for track in midi.tracks[:]:
                    newTrack = MidiTrack()
                    for msg in track:
                        if msg.type == "note_off" or msg.type == "note_on":
                            notes[msg.note%12] = True

                if np.count_nonzero(notes) < 10:
                    delete_file += 1
                    os.remove(os.path.join(root, file))

            except:
                pass

input("Complete!")

