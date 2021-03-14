import os
from mido import MidiFile


UniqueMessages = []

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
                        for track in midi.tracks:
                            for msg in track:
                                if not msg.is_meta:
                                    if UniqueMessages.count(msg.type) == 0:
                                        UniqueMessages.append(msg.type)
                                        print("New unique message '"+msg.type+"' in "+os.path.join(root, file))
                    except:
                        pass

print(UniqueMessages)
input()
        

