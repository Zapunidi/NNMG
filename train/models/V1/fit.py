import tensorflow as tf
import numpy as np
import json
import matplotlib.pyplot as plt
from train.models.V1 import createModel


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
dataDTs = np.load("slicedDataDTs.npy")
XMessages, XValues, XDTs, YMessages, YValues, YDTs = [], [], [], [], [], []
for messages, values, DTs in zip(dataMessages, dataValues, dataDTs):
     XMessages.append(messages[:-1])
     XValues.append(values[:-1])
     XDTs.append(DTs[:-1])
     YMessages.append(messages[1:])
     YValues.append(values[1:])
     YDTs.append(DTs[1:])

XMessages = tf.one_hot(XMessages, depth=2, axis=-1)
YMessages = np.asarray(YMessages)
XValues =  tf.one_hot(XValues, depth=12, axis=-1)
YValues = np.asarray(YValues)
XDTs = np.round(np.asarray(XDTs)/100) #tf.one_hot(np.round(np.asarray(XDTs)/100), depth=21, axis=-1)
YDTs = np.round(np.asarray(YDTs)/100)

XMessages, ValXMessages = XMessages[:40000], XMessages[40000:]
YMessages, ValYMessages = YMessages[:40000], YMessages[40000:]
XValues, ValXValues = XValues[:40000], XValues[40000:]
YValues, ValYValues = YValues[:40000], YValues[40000:]
XDTs, ValXDTs = XDTs[:40000], XDTs[40000:]
YDTs, ValYDTs = YDTs[:40000], YDTs[40000:]



# Model
model = createModel()
model.compile(optimizer='adam', loss={"outputMessage": tf.losses.SparseCategoricalCrossentropy(from_logits=True),
                                      "outputValue": tf.losses.SparseCategoricalCrossentropy(from_logits=True),
                                      "outputDT": tf.losses.SparseCategoricalCrossentropy(from_logits=True)})

# Fit
history = model.fit({"inputMessage": XMessages, "inputValue": XValues, "inputDT": XDTs},
    {"outputMessage": YMessages, "outputValue": YValues, "outputDT": YDTs},
    batch_size=int(len(XDTs)**0.5), epochs=5)
model.save_weights("weights/V2.h5")

for key in history.history:
    plt.plot(history.history[key], label=key)
plt.legend()
plt.show()

