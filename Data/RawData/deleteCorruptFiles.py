import os
from mido import MidiFile


index = 0
for dir in os.listdir():
    if os.path.isdir(dir):
        for root, dirs, files in os.walk(dir):
            for file in files:
                if os.path.splitext(file)[1] == ".mid" or os.path.splitext(file)[1] == ".midi":
                    index += 1
                    print(index, end="\r")

                    try:
                        midi = MidiFile(os.path.join(root, file))
                    except:
                        #os.remove(os.path.join(root, file))
                        print("Delete " + os.path.join(root, file))
input()
