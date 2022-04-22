import argparse
import math
import os
from random import randrange
from tabnanny import verbose

import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import layers

userResponses = []

chunkSize = 5
numFeatures = 1
score = [0, 0]

# Rock 1
# Paper 2
# Scissors 3
decode = {
    '1': 'Rock',
    '2': 'Paper',
    '3': 'Scissors'
}

rules = {
    '1': '2',
    '2': '3',
    '3': '1'
}


def clearScreen():
    # clear console screen
    os.system('cls')


def splitSequence(sequence, chunkSize):
    data = []
    labels = []

    if len(sequence) < chunkSize:
        return data, labels

    for index in range(len(sequence) - chunkSize + 1):
        chunk = sequence[index:index + chunkSize]

        data.append(chunk[:-1])
        labels.append(chunk[-1])

    return np.array(data), np.array(labels)


def menu():
    welcome = """ \t\tRock Paper Scissors\n
    Welcome Player! Select an option to play:\n 
    1) Play :)
    2) Exit :( 
    """

    os.system('cls')
    print(welcome + '\nEnter: ', end="")

    # print welcome and await response
    line = input().strip(' ')
    if line == '1':
        os.system('cls')
        print('Here we gooo!!!')
        return True
    else:
        print('Goodbyeee ;)')
        return False


def generateComputerChoice():
    data, labels = splitSequence(userResponses, chunkSize)

    if (len(data) > 0 and len(labels) > 0):
        data = data.reshape((data.shape[0], data.shape[1], numFeatures))

        model = mediumLSTM(data, labels)
        clearScreen()

        testData = np.array(userResponses[-chunkSize:])
        testData = testData.reshape((1, chunkSize, numFeatures))

        prediction = model.predict(testData, verbose=0)
        # clearScreen()
        # prediction = round(sum(prediction[0])/len(prediction[0]))

        if prediction < 1:
            prediction = 1

        elif prediction > 3:
            prediction = 3

        return rules[f"{prediction}"]

    return str(randrange(1, 4))


# cin -> computer input
# uin -> user input
# rules -> global dictionary
def generate_outcome(cin, uin):
    if rules[uin] == cin:
        score[0] += 1
        print('User WINS! Computer LOSES!')
    elif uin == cin:
        print('TIE!!!')
    else:
        score[1] += 1
        print('Computer WINS! User LOSES!')


# def printPrompt():

    # cin -> computer input
    # uin -> user input


def rps():
    userChoice = ""
    rps_prompt = """
    Make your choice:
      1) Rock
      2) Paper
      3) Scissors

      (Press Q to quit)
    """

    global userResponses
    while userChoice != "Q":
        print("I am deciding what hand I want to play...")

        computerChoice = generateComputerChoice()
        print(f"Computer: {score[1]} | User: {score[0]}")
        print(userResponses)
        print()

        print("Alright. I have decided what hand to play.")

        # reset uin
        userChoice = ""
        # prompt user response
        print(rps_prompt)
        # continue asking for same round if input is invalid
        while userChoice not in decode:
            print('Enter: ', end='')
            # get input
            userChoice = input().strip(' ')
            # check input
            if userChoice in decode:
                # clear console screen
                clearScreen()
                # add user responses to global list
                userResponses.append(int(userChoice))
                # get random computer response
                # print decoded user selection to console
                print(f"User chose {decode[userChoice]}! ", end='')
                # print decoded computer selection
                print(f"Computer chose {decode[computerChoice]}! ", end='')
                # print outcome to console
                generate_outcome(computerChoice, userChoice)
            elif userChoice == 'Q':
                break
            else:
                print("Try again...")


def trainLSTM(trainData, trainLabels):
    model = keras.Sequential()
    # Add an Embedding layer expecting input vocab of size 1000, and
    # output embedding dimension of size 64.
    model.add(layers.Embedding(input_dim=1000, output_dim=64))

    # Add a LSTM layer with 128 internal units.
    model.add(layers.LSTM(128))

    # Add a Dense layer with 10 units.
    model.add(layers.Dense(10))

    model.compile(
        optimizer=tf.keras.optimizers.Adam(0.01),
        loss=tf.keras.losses.MeanSquaredError(),
        metrics=['accuracy']
    )

    model.fit(trainData, trainLabels, epochs=200, verbose=0)

    return model


def mediumLSTM(trainData, trainLabels):
    model = tf.keras.Sequential()
    model.add(layers.LSTM(
        50,
        activation='relu',
        input_shape=(chunkSize, numFeatures))
    )

    model.add(layers.Dense(1))

    model.compile(
        optimizer=tf.keras.optimizers.Adam(0.01),
        loss=tf.keras.losses.MeanSquaredError(),
        metrics=['accuracy']
    )

    model.fit(trainData, trainLabels, epochs=200, verbose=1)


def run():
    play = menu()

    # if user chooses play from menu, game begins
    if play:
        rps()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="This application intends to apply machine learning algorithms to learn a player's rock-paper-scissors strategy, after continuos runs.")

    run()
