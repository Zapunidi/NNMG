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
# To one_hot
dataMessages = np.load("slicedDataMessages.npy")
dataValues = np.load("slicedDataValues.npy")
dataOctaves = np.load("slicedDataOctaves.npy")
dataDTs = np.load("slicedDataDTs.npy")

# mask = np.sum(dataDTs, axis=-1)/960 > 5
# dataMessages = dataMessages[mask]
# dataValues = dataValues[mask]
# dataOctaves = dataOctaves[mask]
# dataDTs = dataDTs[mask]

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
XOctaves = tf.one_hot(XOctaves, depth=7, axis=-1)
YOctaves = np.asarray(YOctaves)
XDTs = tf.one_hot(np.round(np.asarray(XDTs)/20), depth=49, axis=-1)
YDTs = np.round(np.asarray(YDTs)/20).astype(int)


N = int(len(XMessages)*0.8)
XMessages, ValXMessages = XMessages[:N], XMessages[N:]
YMessages, ValYMessages = YMessages[:N], YMessages[N:]
XValues, ValXValues = XValues[:N], XValues[N:]
YValues, ValYValues = YValues[:N], YValues[N:]
XOctaves, ValXOctaves = XOctaves[:N], XOctaves[N:]
YOctaves, ValYOctaves = YOctaves[:N], YOctaves[N:]
XDTs, ValXDTs = XDTs[:N], XDTs[N:]
YDTs, ValYDTs = YDTs[:N], YDTs[N:]


weightOctaves = np.unique(YOctaves, return_counts=True)[1]
weightOctaves = np.sum(weightOctaves)/(len(weightOctaves)*weightOctaves)
weightOctaves = tf.constant([weightOctaves], dtype="float32")

weightDTs = np.unique(YDTs, return_counts=True)[1]
weightDTs = np.sum(weightDTs)/(len(weightDTs)*weightDTs)
weightDTs = tf.constant([weightDTs], dtype="float32")



# Model
def DTs_loss(y_true, y_pred):
    weights = tf.reduce_sum(weightDTs * tf.one_hot(y_true, depth=49, axis=-1, dtype="float32"), axis=-1)
    loss = tf.losses.sparse_categorical_crossentropy(y_true, y_pred) * weights
    return loss

def Octaves_loss(y_true, y_pred):
    weights = tf.reduce_sum(weightOctaves * tf.one_hot(y_true, depth=7, axis=-1, dtype="float32"), axis=-1)
    loss = tf.losses.sparse_categorical_crossentropy(y_true, y_pred) * weights
    return loss


model = createModel()
model.compile(optimizer='adam', loss={"outputMessage": tf.losses.SparseCategoricalCrossentropy(),
                                      "outputValue": tf.losses.SparseCategoricalCrossentropy(),
                                      "outputOctave": tf.losses.SparseCategoricalCrossentropy(), #Octaves_loss,
                                      "outputDT": tf.losses.SparseCategoricalCrossentropy()}, # DTs_loss},
              metrics=['accuracy'])

# Fit
history = model.fit({"inputMessage": XMessages, "inputValue": XValues, "inputOctave": XOctaves, "inputDT": XDTs},
    {"outputMessage": YMessages, "outputValue": YValues, "outputOctave": YOctaves, "outputDT": YDTs},
    batch_size=int(len(XDTs)**0.5), epochs=25,
    validation_data = ({"inputMessage": ValXMessages, "inputValue": ValXValues, "inputOctave": ValXOctaves, "inputDT": ValXDTs},
                   {"outputMessage": ValYMessages, "outputValue": ValYValues, "outputOctave": ValYOctaves,"outputDT": ValYDTs}))
model.save_weights("V.h5")


# Loss
outputMessage_accuracy = history.history["outputMessage_accuracy"]
outputValue_accuracy = history.history["outputValue_accuracy"]
outputOctave_accuracy = history.history["outputOctave_accuracy"]
outputDT_accuracy = history.history["outputDT_accuracy"]
val_outputMessage_accuracy = history.history["val_outputMessage_accuracy"]
val_outputValue_accuracy = history.history["val_outputValue_accuracy"]
val_outputOctave_accuracy = history.history["val_outputOctave_accuracy"]
val_outputDT_accuracy = history.history["val_outputDT_accuracy"]

plt.plot(outputMessage_accuracy, label="message")
plt.plot(outputValue_accuracy, label="value")
plt.plot(outputOctave_accuracy, label="Octave")
plt.plot(outputDT_accuracy, label="dT")
plt.legend()
plt.xlabel("epochs")
plt.ylabel("accuracy")
plt.savefig("accuracy.png")

plt.plot(val_outputMessage_accuracy, label="message")
plt.plot(val_outputValue_accuracy, label="value")
plt.plot(val_outputOctave_accuracy, label="Octave")
plt.plot(val_outputDT_accuracy, label="dT")
plt.legend()
plt.xlabel("epochs")
plt.ylabel("val_accuracy")
plt.savefig("val_accuracy.png")