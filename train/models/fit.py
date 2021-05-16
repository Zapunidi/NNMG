import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from train.models.V2 import createModel


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
dataValues = np.load("slicedDataValues.npy") - 36
dataDTs = np.load("slicedDataDTs.npy")

XMessages, XValues, XDTs, YMessages, YValues, YDTs = [], [], [], [], [], []
for messages, values, DTs in zip(dataMessages, dataValues, dataDTs):
    for octave in range(0 - min(values) // 12, 4 - max(values) // 12 + 1):
        XMessages.append(messages[:-1])
        XValues.append(values[:-1] + octave * 12)
        XDTs.append(DTs[:-1])

        YMessages.append(messages[1:])
        YValues.append(values[1:] + octave * 12)
        YDTs.append(DTs[1:])

XMessages = tf.one_hot(XMessages, depth=2, axis=-1)
YMessages = np.asarray(YMessages)
XValues = tf.one_hot(XValues, depth=60, axis=-1)
YValues = np.asarray(YValues)
XDTs = tf.one_hot(np.round(np.asarray(XDTs) / 60), depth=17, axis=-1)
YDTs = np.round(np.asarray(YDTs) / 60).astype(int)

N = int(len(XMessages) * 0.8)
XMessages, ValXMessages = XMessages[:N], XMessages[N:]
YMessages, ValYMessages = YMessages[:N], YMessages[N:]
XValues, ValXValues = XValues[:N], XValues[N:]
YValues, ValYValues = YValues[:N], YValues[N:]
XDTs, ValXDTs = XDTs[:N], XDTs[N:]
YDTs, ValYDTs = YDTs[:N], YDTs[N:]


# Model
model = createModel()
model.compile(optimizer='adam', loss={"outputMessage": tf.losses.SparseCategoricalCrossentropy(),
                                      "outputValue": tf.losses.SparseCategoricalCrossentropy(),
                                      "outputDT": tf.losses.SparseCategoricalCrossentropy()},
              metrics=['accuracy'])

# Fit
history = model.fit({"inputMessage": XMessages, "inputValue": XValues, "inputDT": XDTs},
    {"outputMessage": YMessages, "outputValue": YValues, "outputDT": YDTs},
    batch_size=int(len(XDTs)**0.5), epochs=100,
    validation_data = ({"inputMessage": ValXMessages, "inputValue": ValXValues, "inputDT": ValXDTs},
                   {"outputMessage": ValYMessages, "outputValue": ValYValues, "outputDT": ValYDTs}))
model.save_weights("V.h5")


# Loss
outputMessage_accuracy = history.history["outputMessage_accuracy"]
outputValue_accuracy = history.history["outputValue_accuracy"]
outputDT_accuracy = history.history["outputDT_accuracy"]
val_outputMessage_accuracy = history.history["val_outputMessage_accuracy"]
val_outputValue_accuracy = history.history["val_outputValue_accuracy"]
val_outputDT_accuracy = history.history["val_outputDT_accuracy"]

plt.plot(outputMessage_accuracy, label="message")
plt.plot(outputValue_accuracy, label="value")
plt.plot(outputDT_accuracy, label="dT")
plt.legend()
plt.xlabel("epochs")
plt.ylabel("accuracy")
plt.savefig("accuracy.png")

plt.plot(val_outputMessage_accuracy, label="message")
plt.plot(val_outputValue_accuracy, label="value")
plt.plot(val_outputDT_accuracy, label="dT")
plt.legend()
plt.xlabel("epochs")
plt.ylabel("val_accuracy")
plt.savefig("val_accuracy.png")