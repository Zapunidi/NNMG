import numpy as np
import json


print("Open...")
dataMessages = json.load(open("processingData/dataMessages.json", "r"))
dataValues = json.load(open("processingData/dataValues.json", "r"))
dataOctaves = json.load(open("processingData/dataOctaves.json", "r"))
dataDTs = json.load(open("processingData/dataDTs.json", "r"))


slicedDataMessages = []
slicedDataValues = []
slicedDataOctaves = []
slicedDataDTs = []

print("Slice...")
number = 0
length = 101
for messages, values, octaves, DTs in zip(dataMessages, dataValues, dataOctaves, dataDTs):
    for i in range(len(messages)//length):
        number += 1
        print(number, end="\r")


        slicedDataMessages.append(messages[i*length:(i+1)*length])
        slicedDataValues.append(values[i * length:(i + 1) * length])
        slicedDataOctaves.append(octaves[i * length:(i + 1) * length])
        slicedDataDTs.append(DTs[i * length:(i + 1) * length])


print("Save...")
slicedDataMessages = np.asarray(slicedDataMessages)
slicedDataValues = np.asarray(slicedDataValues)
slicedDataOctaves = np.asarray(slicedDataOctaves)
slicedDataDTs = np.asarray(slicedDataDTs)

np.save("processingData/slicedDataMessages.npy", slicedDataMessages)
np.save("processingData/slicedDataValues.npy", slicedDataValues)
np.save("processingData/slicedDataOctaves.npy", slicedDataOctaves)
np.save("processingData/slicedDataDTs.npy", slicedDataDTs)


input("Complete!")


