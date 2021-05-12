import tensorflow as tf


# Model
def createModel(dropout=True):
    inputMessage = tf.keras.Input(shape=(None, 2), name="inputMessage")
    inputValue = tf.keras.Input(shape=(None, 12), name="inputValue")
    inputDT = tf.keras.Input(shape=(None, 21), name="inputDT")

    concatenateInputDT = tf.keras.layers.concatenate([inputMessage, inputValue, inputDT], name="concatenateInputDT")
    gruDT1 = tf.keras.layers.GRU(64, return_sequences=True, name="gruDT1")(concatenateInputDT)
    if dropout:
        gruDT1 = tf.keras.layers.Dropout(0.05)(gruDT1)
    gruDT2 = tf.keras.layers.GRU(64, return_sequences=True, name="gruDT2")(gruDT1)
    if dropout:
        gruDT2 = tf.keras.layers.Dropout(0.05)(gruDT2)
    concatenateOutputDT = tf.keras.layers.concatenate([gruDT1, gruDT2], name="concatenateOutputDT")
    outputDT = tf.keras.layers.Dense(21, activation="softmax", name="outputDT")(concatenateOutputDT)

    concatenateInputMessage = tf.keras.layers.concatenate([inputMessage, inputValue, inputDT, outputDT],
                                                          name="concatenateInputMessage")
    gruMessage1 = tf.keras.layers.GRU(64, return_sequences=True, name="gruMessage1")(concatenateInputMessage)
    if dropout:
        gruMessage1 = tf.keras.layers.Dropout(0.05)(gruMessage1)
    gruMessage2 = tf.keras.layers.GRU(64, return_sequences=True, name="gruMessage2")(gruMessage1)
    if dropout:
        gruMessage2 = tf.keras.layers.Dropout(0.05)(gruMessage2)
    concatenateOutputMessage = tf.keras.layers.concatenate([gruMessage1, gruMessage2], name="concatenateOutputMessage")
    outputMessage = tf.keras.layers.Dense(2, activation="softmax", name="outputMessage")(concatenateOutputMessage)

    concatenateInputValue = tf.keras.layers.concatenate([inputMessage, inputValue, inputDT, outputDT, outputMessage],
                                                        name="concatenateInputValue")
    gruValue1 = tf.keras.layers.GRU(64, return_sequences=True, name="gruValue1")(concatenateInputValue)
    if dropout:
        gruValue1 = tf.keras.layers.Dropout(0.05)(gruValue1)
    gruValue2 = tf.keras.layers.GRU(64, return_sequences=True, name="gruValue2")(gruValue1)
    if dropout:
        gruValue2 = tf.keras.layers.Dropout(0.05)(gruValue2)
    gruValue3 = tf.keras.layers.GRU(64, return_sequences=True, name="gruValue3")(gruValue2)
    if dropout:
        gruValue3 = tf.keras.layers.Dropout(0.05)(gruValue3)
    concatenateOutputValue = tf.keras.layers.concatenate([gruValue1, gruValue2, gruValue3],
                                                         name="concatenateOutputValue")
    outputValue = tf.keras.layers.Dense(12, activation="softmax", name="outputValue")(concatenateOutputValue)

    return tf.keras.Model(inputs=[inputMessage, inputValue, inputDT],
                          outputs=[outputMessage, outputValue, outputDT])

