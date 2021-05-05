import tensorflow as tf
import numpy as np
import json
import random
from train.models.V1.V1 import createModel

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


def generate_melody(model, num_generate, messages, values, DTs):
    melody = []
    for message, value, DT in zip(messages, values, DTs):
        melody.append((message, value + 60, int(100 * DT)))

    messages = tf.one_hot(messages, depth=2, axis=-1)
    messages = tf.reshape(messages, (1, *messages.shape))
    values = tf.one_hot(np.asarray(values) % 12, depth=12, axis=-1)
    values = tf.reshape(values, (1, *values.shape))
    DTs = np.asarray(DTs)
    DTs = tf.reshape(DTs, (1, *DTs.shape))

    model.reset_states()

    for i in range(num_generate):
        PrMessage, PrValues, PrDT = model((messages, values, DTs))
        PrMessage = PrMessage[0][-1]
        PrValues = PrValues[0][-1]
        PrDT = PrDT[0][-1]

        message = tf.random.categorical(tf.math.log(PrMessage.numpy().reshape(1, 2)), num_samples=1)
        value = tf.random.categorical(tf.math.log(PrValues.numpy().reshape(1, 12)), num_samples=1)
        DT = tf.random.categorical(tf.math.log(PrDT.numpy().reshape(1, 21)), num_samples=1)

        messages = tf.one_hot(message, depth=2, axis=-1)
        values = tf.one_hot(value, depth=12, axis=-1)
        DTs = DT

        melody.append((int(message.numpy()[0][0]),
                       int(value.numpy()[0][0] + 60),
                       int(100 * DT.numpy()[0][0])))

    return melody


print("Create and load model...")
model = createModel(dropout=False)
model.load_weights("V2.h5")

print("Create example...")
dataMessages = json.load(open("dataMessages.json", "r"))
dataValues = json.load(open("dataValues.json", "r"))
dataDTs = json.load(open("dataDTs.json", "r"))
length = 100
r1 = random.randint(0, len(dataMessages))
r2 = random.randint(0, len(dataMessages[r1]) - length - 1)
print("Generate...")
melody = generate_melody(model, 2000,
                         messages=dataMessages[r1][r2:r2 + length],
                         values=dataValues[r1][r2:r2 + length],
                         DTs=np.round(np.asarray(dataDTs[r1][r2:r2 + length]) / 100))

print("Save..")
file = open("melody.json", "w")
file.write(json.dumps(melody))
file.close()
input("Complete!")


