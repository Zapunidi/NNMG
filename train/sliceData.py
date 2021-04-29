import numpy as np
import json


dataMessages = json.load(open("processingData/dataMessages.json", "r"))
dataValues = json.load(open("processingData/dataValues.json", "r"))
dataDTs = json.load(open("processingData/dataDTs.json", "r"))


slicedDataMessages = []
slicedDataValues = []
slicedDataDTs = []

number = 0
length = 101
for messages, values, DTs in zip(dataMessages, dataValues, dataDTs):
    number += 1
    print(number, end="\r")
    for i in range(len(messages)//length):
        slicedDataMessages.append(messages[i*length:(i+1)*length])
        slicedDataValues.append(values[i * length:(i + 1) * length])
        slicedDataDTs.append(DTs[i * length:(i + 1) * length])


file = open("processingData/slicedDataMessages.json", "w")
file.write(json.dumps(slicedDataMessages))
file.close()

file = open("processingData/slicedDataValues.json", "w")
file.write(json.dumps(slicedDataValues))
file.close()

file = open("processingData/slicedDataDTs.json", "w")
file.write(json.dumps(slicedDataDTs))
file.close()

input("Complete!")


