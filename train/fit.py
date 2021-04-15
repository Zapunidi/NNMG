import tensorflow as tf
import numpy as np
import json
from train.model import createModel


gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
  try:
    # Currently, memory growth needs to be the same across GPUs
    for gpu in gpus:
      tf.config.experimental.set_memory_growth(gpu, True)
    logical_gpus = tf.config.experimental.list_logical_devices('GPU')
    print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
  except RuntimeError as e:
    # Memory growth must be set before GPUs have been initialized
    print(e)


# To one_hot
dataMessages = json.load(open("slicedDataMessages.json", "r"))
dataValues = json.load(open("slicedDataValues.json", "r"))
dataDTs = json.load(open("slicedDataDTs.json", "r"))
XMessages, XValues, XDTs, YMessages, YValues, YDTs = [], [], [], [], [], []
for messages, values, DTs in zip(dataMessages, dataValues, dataDTs):
     XMessages.append(messages[:-1])
     XValues.append(values[:-1])
     XDTs.append(DTs[:-1])
     YMessages.append(messages[1:])
     YValues.append(values[1:])
     YDTs.append(DTs[1:])
XMessages = tf.one_hot(XMessages, depth=2, axis=-1)
XValues = tf.one_hot(XValues, depth=128, axis=-1)
XDTs = tf.one_hot(np.round(np.asarray(XDTs)/100), depth=21, axis=-1)
YMessages = np.asarray(YMessages)
YValues = np.asarray(YValues)
YDTs = np.round(np.asarray(YDTs)/100)


# Model
model = createModel()
model.compile(optimizer='adam', loss={"outputMessage": tf.losses.SparseCategoricalCrossentropy(from_logits=True),
                                      "outputValue": tf.losses.SparseCategoricalCrossentropy(from_logits=True),
                                      "outputDT": tf.losses.SparseCategoricalCrossentropy(from_logits=True)})

# Fit
history = model.fit({"inputMessage": XMessages, "inputValue": XValues, "inputDT": XDTs},
    {"outputMessage": YMessages, "outputValue": YValues, "outputDT": YDTs},
    batch_size=int(len(XDTs)**0.5), epochs=100)
model.save_weights("weights.h5")
