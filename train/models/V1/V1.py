import tensorflow as tf


# Model
def createModel(dropout=True):
    inputMessage = tf.keras.Input(shape=(None, 2), name="inputMessage")
    inputValue = tf.keras.Input(shape=(None, 12), name="inputValue")
    inputDT = tf.keras.Input(shape=(None,), name="inputDT")
    embeddingDT = tf.keras.layers.Embedding(21, 1)(inputDT)

    concatenate = tf.keras.layers.concatenate([inputMessage, inputValue , embeddingDT], name="concatenateInput")
    gruMessageInput = tf.keras.layers.GRU(32, return_sequences=True, name="gruMessageInput")(concatenate)
    if dropout:
      gruMessageInput = tf.keras.layers.Dropout(0.2)(gruMessageInput)
    gruValueInput = tf.keras.layers.GRU(64, return_sequences=True, name="gruValueInput")(concatenate)
    if dropout:
      gruValueInput = tf.keras.layers.Dropout(0.2)(gruValueInput)
    gruDTInput = tf.keras.layers.GRU(16, return_sequences=True, name="gruDTInput")(concatenate)
    if dropout:
      gruDTInput = tf.keras.layers.Dropout(0.2)(gruDTInput)

    concatenate = tf.keras.layers.concatenate([gruMessageInput, gruValueInput, gruDTInput], name="concatenate")
    gru = tf.keras.layers.GRU(128, return_sequences=True, name="gruGlobal")(concatenate)
    if dropout:
      gru = tf.keras.layers.Dropout(0.2)(gru)

    gruMessageOutput = tf.keras.layers.GRU(32, return_sequences=True, name="gruMessage")(gru)
    if dropout:
      gruMessageOutput = tf.keras.layers.Dropout(0.2)(gruMessageOutput)
    gruValueOutput = tf.keras.layers.GRU(64, return_sequences=True, name="gruValue")(gru)
    if dropout:
      gruValueOutput = tf.keras.layers.Dropout(0.2)(gruValueOutput)
    gruDTOutput = tf.keras.layers.GRU(16, return_sequences=True, name="gruDT")(gru)
    if dropout:
      gruDTOutput = tf.keras.layers.Dropout(0.2)(gruDTOutput)

    concatenate = tf.keras.layers.concatenate([gruMessageOutput, gruValueOutput, gruDTOutput], name="concatenateOutput")
    outputMessage = tf.keras.layers.Dense(2, activation="softmax", name="outputMessage")(concatenate)
    outputValue = tf.keras.layers.Dense(12, activation="softmax", name="outputValue")(concatenate)
    outputDT = tf.keras.layers.Dense(21, activation="softmax", name="outputDT")(concatenate)
    return tf.keras.Model(inputs=[inputMessage, inputValue, inputDT],
                          outputs=[outputMessage, outputValue, outputDT])

