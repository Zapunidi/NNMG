import tensorflow as tf


# Model
def createModel():
    inputMessage = tf.keras.Input(shape=(None, 2), name="inputMessage")
    inputValue = tf.keras.Input(shape=(None,), name="inputValue")
    embeddingValue = tf.keras.layers.Embedding(128, 16)(inputValue)
    inputDT = tf.keras.Input(shape=(None, 21), name="inputDT")


    concatenateInputDT = tf.keras.layers.concatenate([inputDT, inputMessage, embeddingValue], name="concatenateInputDT")
    gruDT1 = tf.keras.layers.GRU(64, return_sequences=True, name="gruDT1")(concatenateInputDT)
    gruDT2 = tf.keras.layers.GRU(64, return_sequences=True, name="gruDT2")(gruDT1)
    concatenateOutputDT = tf.keras.layers.concatenate([gruDT1, gruDT2], name="concatenateOutputDT")
    outputDT = tf.keras.layers.Dense(21, activation="softmax", name="outputDT")(concatenateOutputDT)


    concatenateInputMessage = tf.keras.layers.concatenate([inputDT, inputMessage, embeddingValue, outputDT], name="concatenateInputMessage")
    gruMessage1 = tf.keras.layers.GRU(64, return_sequences=True, name="gruMessage1")(concatenateInputMessage)
    gruMessage2 = tf.keras.layers.GRU(64, return_sequences=True, name="gruMessage2")(gruMessage1)
    concatenateOutputMessage = tf.keras.layers.concatenate([gruMessage1, gruMessage2], name="concatenateOutputMessage")
    outputMessage = tf.keras.layers.Dense(21, activation="softmax", name="outputMessage")(concatenateOutputMessage)


    concatenateInputValue = tf.keras.layers.concatenate([inputDT, inputMessage, embeddingValue, outputDT, outputMessage], name="concatenateInputValue")
    gruValue1 = tf.keras.layers.GRU(128, return_sequences=True, name="gruValue1")(concatenateInputValue)
    gruValue2 = tf.keras.layers.GRU(128, return_sequences=True, name="gruValue2")(gruValue1)
    gruValue3 = tf.keras.layers.GRU(128, return_sequences=True, name="gruValue3")(gruValue2)
    concatenateOutputValue = tf.keras.layers.concatenate([gruValue1, gruValue2, gruValue3], name="concatenateOutputValue")
    outputValue = tf.keras.layers.Dense(21, activation="softmax", name="outputValue")(concatenateOutputValue)

    return tf.keras.Model(inputs=[inputMessage, inputValue, inputDT],
                          outputs=[outputMessage, outputValue, outputDT])

