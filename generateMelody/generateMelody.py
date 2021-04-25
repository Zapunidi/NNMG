import tensorflow as tf
import numpy as np
import json
from V2 import createModel

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
        melody.append((message, value, DT))

    messages = tf.one_hot(messages, depth=2, axis=-1)
    messages = tf.reshape(messages, (1, *messages.shape))
    values = tf.one_hot(values, depth=128, axis=-1)
    values = tf.reshape(values, (1, *values.shape))
    DTs = tf.one_hot(np.round(np.asarray(DTs) / 100), depth=21, axis=-1)
    DTs = tf.reshape(DTs, (1, *DTs.shape))

    model.reset_states()

    for i in range(num_generate):
        PrMessage, PrValues, PrDT = model((messages, values, DTs))
        PrMessage = PrMessage[0][-1]
        PrValues = PrValues[0][-1]
        PrDT = PrDT[0][-1]
        
        message = tf.random.categorical(tf.math.log(PrMessage.numpy().reshape(1, 2)), num_samples=1)
        value = tf.random.categorical(tf.math.log(PrValues.numpy().reshape(1, 128)), num_samples=1)
        DT = tf.random.categorical(tf.math.log(PrDT.numpy().reshape(1, 21)), num_samples=1)

        messages = tf.one_hot(message, depth=2, axis=-1)
        values = tf.one_hot(value, depth=128, axis=-1)
        DTs = tf.one_hot(DT, depth=21, axis=-1)

        melody.append((int(message.numpy()[0][0]),
                       int(value.numpy()[0][0]),
                       int(100 * DT.numpy()[0][0])))

    return melody




model = createModel()
#model.load_weights("V2.h5")
melody = generate_melody(model, 500,
                         messages=[1],
                         values=[60],
                         DTs=[0])

file = open("melody.json", "w")
file.write(json.dumps(melody))
file.close()
input("Complete!")


