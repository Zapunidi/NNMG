import tensorflow as tf
import numpy as np
import json
import matplotlib.pyplot as plt
from train.models.V2.V2 import createModel


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
dataMessages = np.load("slicedDataMessages.npy")
dataValues = np.load("slicedDataValues.npy")
dataOctaves = np.load("slicedDataOctaves.npy")
dataDTs = np.load("slicedDataDTs.npy")
XMessages, XValues, XOctaves, XDTs, YMessages, YValues, YOctaves, YDTs = [], [], [], [], [], [], [], []
for messages, values, octaves, DTs in zip(dataMessages, dataValues, dataOctaves, dataDTs):
     XMessages.append(messages[:-1])
     XValues.append(values[:-1])
     XOctaves.append(octaves[:-1])
     XDTs.append(DTs[:-1])

     YMessages.append(messages[1:])
     YValues.append(values[1:])
     YOctaves.append(octaves[1:])
     YDTs.append(DTs[1:])

XMessages = tf.one_hot(XMessages, depth=2, axis=-1)
YMessages = np.asarray(YMessages)
XValues = tf.one_hot(XValues, depth=12, axis=-1)
YValues = np.asarray(YValues)
XOctaves = tf.one_hot(XOctaves, depth=8, axis=-1)
YOctaves = np.asarray(YOctaves)
XDTs = tf.one_hot(np.round(np.asarray(XDTs)/10), depth=21, axis=-1)
YDTs = np.round(np.asarray(YDTs)/10)

N = int(len(XMessages)*0.8)
XMessages, ValXMessages = XMessages[:N], XMessages[N:]
YMessages, ValYMessages = YMessages[:N], YMessages[N:]
XValues, ValXValues = XValues[:N], XValues[N:]
YValues, ValYValues = YValues[:N], YValues[N:]
XOctaves, ValXOctaves = XOctaves[:N], XOctaves[N:]
YOctaves, ValYOctaves = YOctaves[:N], YOctaves[N:]
XDTs, ValXDTs = XDTs[:N], XDTs[N:]
YDTs, ValYDTs = YDTs[:N], YDTs[N:]



# Model
model = createModel()
model.compile(optimizer='adam', loss={"outputMessage": tf.losses.SparseCategoricalCrossentropy(from_logits=True),
                                      "outputValue": tf.losses.SparseCategoricalCrossentropy(from_logits=True),
                                      "outputOctave": tf.losses.SparseCategoricalCrossentropy(from_logits=True),
                                      "outputDT": tf.losses.SparseCategoricalCrossentropy(from_logits=True)},
              metrics=['accuracy'])

# Fit
history = model.fit({"inputMessage": XMessages, "inputValue": XValues, "inputOctave": XOctaves, "inputDT": XDTs},
    {"outputMessage": YMessages, "outputValue": YValues, "outputOctave": YOctaves, "outputDT": YDTs},
    batch_size=int(len(XDTs)**0.5), epochs=5,
    validation_data = ({"inputMessage": ValXMessages, "inputValue": ValXValues, "inputOctave": ValXOctaves, "inputDT": ValXDTs},
                   {"outputMessage": ValYMessages, "outputValue": ValYValues, "outputOctave": ValYOctaves,"outputDT": ValYDTs}))
model.save_weights("weights/V2.h5")

for key in history.history:
    plt.plot(history.history[key], label=key)
plt.legend()
plt.show()

