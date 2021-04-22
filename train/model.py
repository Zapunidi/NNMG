import tensorflow as tf


# Model
def createModel():
    inputMessage = tf.keras.Input(shape=(None, 2), name="inputMessage")
    inputValue = tf.keras.Input(shape=(None, 128), name="inputValue")
    inputDT = tf.keras.Input(shape=(None, 21), name="inputDT")

    gruMessage = tf.keras.layers.GRU(32, return_sequences=True, name="gruMessage")(inputMessage)
    gruValue = tf.keras.layers.GRU(32, return_sequences=True, name="gruValue")(inputValue)
    gruDT = tf.keras.layers.GRU(32, return_sequences=True, name="gruDT")(inputDT)

    x = tf.keras.layers.concatenate([gruMessage, gruValue, gruDT], name="concatenate")
    gru = tf.keras.layers.GRU(128, return_sequences=True, name="gruGlobal")(x)

    outputMessage = tf.keras.layers.Dense(2, name="outputMessage")(gru)
    outputValue = tf.keras.layers.Dense(128, name="outputValue")(gru)
    outputDT = tf.keras.layers.Dense(21, name="outputDT")(gru)
    return tf.keras.Model(inputs=[inputMessage, inputValue, inputDT],
                          outputs=[outputMessage, outputValue, outputDT])

