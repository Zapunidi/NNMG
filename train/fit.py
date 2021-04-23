import tensorflow as tf
import numpy as np
import json
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
dataMessages = json.load(open("processingData/slicedDataMessages.json", "r"))
dataValues = json.load(open("processingData/slicedDataValues.json", "r"))
dataDTs = json.load(open("processingData/slicedDataDTs.json", "r"))
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

XDTs = np.round(np.asarray(XDTs)/100)
XDTs[XDTs > 20] = 20
XDTs = tf.one_hot(XDTs, depth=21, axis=-1)

YMessages = np.asarray(YMessages)
YValues = np.asarray(YValues)
YDTs = np.round(np.asarray(YDTs)/100)
YDTs[YDTs > 20] = 20



# Model
model = createModel()
model.compile(optimizer='adam', loss={"outputMessage": tf.losses.SparseCategoricalCrossentropy(from_logits=True),
                                      "outputValue": tf.losses.SparseCategoricalCrossentropy(from_logits=True),
                                      "outputDT": tf.losses.SparseCategoricalCrossentropy(from_logits=True)})

# Fit
callback = tf.keras.callbacks.ModelCheckpoint(filepath="weights/V2.ckpt", save_weights_only=True, verbose=5)
history = model.fit({"inputMessage": XMessages, "inputValue": XValues, "inputDT": XDTs},
    {"outputMessage": YMessages, "outputValue": YValues, "outputDT": YDTs},
    batch_size=int(len(XDTs)**0.5), epochs=5, callbacks=[callback])


for key in history.history:
    plt.plot(history.history[key], label=key)
plt.legend()
plt.show()

