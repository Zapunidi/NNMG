import tensorflow as tf


# Model
def createModel():
    inputMessage = tf.keras.Input(shape=(None, 2), name="inputMessage")
    inputValue = tf.keras.Input(shape=(None, 128), name="inputValue")
    inputDT = tf.keras.Input(shape=(None, 21), name="inputDT")

    x = tf.keras.layers.concatenate([inputDT, inputMessage, inputValue], name="concatenateDT")
    gruDT = tf.keras.layers.GRU(32, return_sequences=True)(x)
    gruDT = tf.keras.layers.GRU(32, return_sequences=True)(gruDT)
    outputDT = tf.keras.layers.Dense(21, activation="softmax", name="outputDT")(gruDT)

    x = tf.keras.layers.concatenate([inputDT, inputMessage, inputValue, outputDT], name="concatenateMessage")
    gruMessage = tf.keras.layers.GRU(32, return_sequences=True)(x)
    gruMessage = tf.keras.layers.GRU(32, return_sequences=True)(gruMessage)
    outputMessage = tf.keras.layers.Dense(2, activation="softmax", name="outputMessage")(gruMessage)

    x = tf.keras.layers.concatenate([inputDT, inputMessage, inputValue, outputDT, outputMessage], name="concatenateValue")
    gruValue = tf.keras.layers.GRU(128, return_sequences=True)(x)
    gruValue = tf.keras.layers.GRU(128, return_sequences=True)(gruValue)
    gruValue = tf.keras.layers.GRU(128, return_sequences=True)(gruValue)
    outputValue = tf.keras.layers.Dense(128, activation="softmax", name="outputValue")(gruValue)

    return tf.keras.Model(inputs=[inputMessage, inputValue, inputDT],
                          outputs=[outputMessage, outputValue, outputDT])

