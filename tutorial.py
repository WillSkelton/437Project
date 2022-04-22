import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


def mySplitSequence(sequence, numSteps):
    data = []
    labels = []

    if len(sequence) <= numSteps:
        return np.array(data), np.array(labels)

    for index in range(len(sequence) - (numSteps + 1)):
        chunk = sequence[index:index + numSteps + 1]

        data.append(chunk[:-1])
        labels.append(chunk[-1])

    return np.array(data), np.array(labels)


def splitSequence(sequence, numSteps):

    # Declare X and y as empty list
    data = []
    labels = []

    for index in range(len(sequence)):
        # get the last index
        lastIndex = index + numSteps

        # if lastIndex is greater than length of sequence then break
        if lastIndex > len(sequence) - 1:
            break

        # Create input and output sequence
        seq_X, seq_y = sequence[index:lastIndex], sequence[lastIndex]

        # append seq_X, seq_y in X and y list
        data.append(seq_X)
        labels.append(seq_y)
        pass
    # Convert X and y into numpy array
    data = np.array(data)
    labels = np.array(labels)

    return data, labels


def trainModel(data, labels, numSteps, numFeatures):
    model = tf.keras.Sequential()
    model.add(layers.LSTM(
        50,
        activation='relu',
        input_shape=(numSteps, numFeatures)
    ))

    model.add(layers.Dense(1))

    model.summary()

    model.compile(
        optimizer=tf.keras.optimizers.Adam(0.01),
        loss=tf.keras.losses.MeanSquaredError(),
        metrics=['accuracy']
    )

    model.fit(data, labels, epochs=200, verbose=0)

    return model


def main():
    numSteps = 5
    numFeatures = 1

    userData = [
        10, 20, 30, 40, 50,
        60, 70, 80, 90, 100,
        110, 120, 130, 140, 150,
        160, 170, 180, 190, 200
    ]

    userData = [
        10, 20, 30, 40, 50,
        60, 70, 80, 90, 100,
        # 110, 120, 130, 140, 150,
        # 160, 170, 180, 190, 200
    ]

    # trainData, trainLabels = splitSequence(userData, numSteps)
    trainData, trainLabels = mySplitSequence(userData, numSteps)
    print(trainData)

    if len(trainData) == 0:
        return

    trainData = trainData.reshape((trainData.shape[0], trainData.shape[1], numFeatures))

    # print(trainData[:2])

    model = trainModel(trainData, trainLabels, numSteps, numFeatures)

    test_data = np.array([90, 100, 110, 120, 130])
    test_data = test_data.reshape((1, numSteps, numFeatures))

    predictNextNumber = model.predict(test_data, verbose=0)[0][0]
    print(round(predictNextNumber))


main()
