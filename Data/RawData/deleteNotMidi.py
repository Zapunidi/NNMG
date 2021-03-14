import os


for dir in os.listdir():
    if os.path.isdir(dir):
        for root, dirs, files in os.walk(dir):
            for file in files:
                if os.path.splitext(file)[1] != ".mid" and os.path.splitext(file)[1] != ".midi":
                    # os.remove(os.path.join(root, file))
                    print("Delete "+os.path.join(root, file))
input()