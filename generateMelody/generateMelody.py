import tensorflow as tf
import numpy as np
import json
from train.models.V import createModel

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


def generate_melody(model, num_generate, messages, values, octaves):
    melody = []
    for message, value, octave in zip(messages, values, octaves):
        melody.append((message, value, octave))

    messages = tf.one_hot(messages, depth=2, axis=-1)
    messages = tf.reshape(messages, (1, *messages.shape))
    values = tf.one_hot(np.asarray(values), depth=12, axis=-1)
    values = tf.reshape(values, (1, *values.shape))
    octaves = tf.one_hot(np.asarray(octaves), depth=8, axis=-1)
    octaves = tf.reshape(octaves, (1, *octaves.shape))

    model.reset_states()

    for i in range(num_generate):
        PrMessage, PrValues, PrOctaves = model((messages, values, octaves))
        PrMessage = PrMessage[0][-1]
        PrValues = PrValues[0][-1]
        PrOctaves = PrOctaves[0][-1]

        message = tf.random.categorical(tf.math.log(PrMessage.numpy().reshape(1, 2)), num_samples=1)
        value = tf.random.categorical(tf.math.log(PrValues.numpy().reshape(1, 12)), num_samples=1)
        octave = tf.random.categorical(tf.math.log(PrOctaves.numpy().reshape(1, 8)), num_samples=1)

        messages = tf.one_hot(message, depth=2, axis=-1)
        values = tf.one_hot(value, depth=12, axis=-1)
        octaves = tf.one_hot(octave, depth=8, axis=-1)

        melody.append((int(message.numpy()[0][0]),
                       int(value.numpy()[0][0]),
                       int(octave.numpy()[0][0])))

    return melody


print("Create and load model...")
model = createModel(dropout=False)
# model.load_weights("V.h5")


print("Generate...")
melody = generate_melody(model, 1000,
                         messages=[1],
                         values=[0],
                         octaves=[4])
print("Save..")
file = open("melody.json", "w")
file.write(json.dumps(melody))
file.close()
input("Complete!")


