import numpy as np
import json


dataMessages = json.load(open("processingData/dataMessages.json", "r"))
dataValues = json.load(open("processingData/dataValues.json", "r"))
dataDTs = json.load(open("processingData/dataDTs.json", "r"))


slicedDataMessages = []
slicedDataValues = []
slicedDataDTs = []

number = 0
length = 50
for messages, values, DTs in zip(dataMessages, dataValues, dataDTs):
    if number <= 100000:
        for i in range(len(messages)//length):
            number += 1
            print(number, end="\r")
            
            slicedDataMessages.append(messages[i*length:(i+1)*length])
            slicedDataValues.append(values[i * length:(i + 1) * length])
            slicedDataDTs.append(DTs[i * length:(i + 1) * length])


slicedDataMessages = np.asarray(slicedDataMessages)
slicedDataValues = np.asarray(slicedDataValues)
slicedDataDTs = np.asarray(slicedDataDTs)

np.save("processingData/slicedDataMessages.npy", slicedDataMessages)
np.save("processingData/slicedDataValues.npy", slicedDataValues)
np.save("processingData/slicedDataDTs.npy", slicedDataDTs)


input("Complete!")


