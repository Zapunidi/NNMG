import tensorflow as tf


# Model
def createModel():
    inputMessage = tf.keras.Input(shape=(None, 2), name="inputMessage")
    inputValue = tf.keras.Input(shape=(None, 128), name="inputValue")
    inputDT = tf.keras.Input(shape=(None, 21), name="inputDT")

    concatenate = tf.keras.layers.concatenate([inputMessage, inputValue , inputDT], name="concatenateInput")
    gruMessageInput = tf.keras.layers.GRU(128, return_sequences=True, name="gruMessageInput")(concatenate)
    gruValueInput = tf.keras.layers.GRU(256, return_sequences=True, name="gruValueInput")(concatenate)
    gruDTInput = tf.keras.layers.GRU(64, return_sequences=True, name="gruDTInput")(concatenate)

    concatenate = tf.keras.layers.concatenate([gruMessageInput, gruValueInput, gruDTInput], name="concatenate")
    gru = tf.keras.layers.GRU(512, return_sequences=True, name="gruGlobal")(concatenate)

    gruMessageOutput = tf.keras.layers.GRU(128, return_sequences=True, name="gruMessage")(gru)
    gruValueOutput = tf.keras.layers.GRU(256, return_sequences=True, name="gruValue")(gru)
    gruDTOutput = tf.keras.layers.GRU(64, return_sequences=True, name="gruDT")(gru)

    outputMessage = tf.keras.layers.Dense(2, activation="softmax", name="outputMessage")(gruMessageOutput)
    outputValue = tf.keras.layers.Dense(128, activation="softmax", name="outputValue")(gruValueOutput)
    outputDT = tf.keras.layers.Dense(21, activation="softmax", name="outputDT")(gruDTOutput)
    return tf.keras.Model(inputs=[inputMessage, inputValue, inputDT],
                          outputs=[outputMessage, outputValue, outputDT])

