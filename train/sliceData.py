import numpy as np
import json


print("Open...")
dataMessages = json.load(open("processingData/dataMessages.json", "r"))
dataValues = json.load(open("processingData/dataValues.json", "r"))
dataOctaves = json.load(open("processingData/dataOctaves.json", "r"))


slicedDataMessages = []
slicedDataValues = []
slicedDataOctaves = []

print("Slice...")
number = 0
length = 101
for messages, values, octaves in zip(dataMessages, dataValues, dataOctaves):
    if number <= 100000:
        for i in range(len(messages)//length):
            number += 1
            print(number, end="\r")


            slicedDataMessages.append(messages[i*length:(i+1)*length])
            slicedDataValues.append(values[i * length:(i + 1) * length])
            slicedDataOctaves.append(octaves[i * length:(i + 1) * length])


print("Save...")
slicedDataMessages = np.asarray(slicedDataMessages)
slicedDataValues = np.asarray(slicedDataValues)
slicedDataOctaves = np.asarray(slicedDataOctaves)

np.save("processingData/slicedDataMessages.npy", slicedDataMessages)
np.save("processingData/slicedDataValues.npy", slicedDataValues)
np.save("processingData/slicedDataOctaves.npy", slicedDataOctaves)


input("Complete!")


