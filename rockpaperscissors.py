import argparse
import math
import os
from random import randrange

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

userResponses = []

chunkSize = 6
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
    '1': '3',
    '2': '1',
    '3': '2'
}


def convertSequenceToData(sequence, chunkSize):
    data = []
    labels = []

    if len(sequence) < chunkSize:
        return data, labels

    for index in range(len(sequence) - chunkSize + 1):
        chunk = sequence[index:index + chunkSize]

        data.append(chunk[:-1])
        labels.append(chunk[-1])

    return data, labels


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
        print('LETS GOOO!!!')
        return True
    else:
        print('Goodbyeee ;)')
        return False


def computerChoice():
    data, labels = convertSequenceToData(userResponses, chunkSize)

    if (len(data) > 0 and len(labels) > 0):
        model = trainLSTM(data, labels)

        # prediction = model.predict(debugTest)
        print(prediction)

    return str(randrange(1, 4))


def generate_response():
    choice = computerChoice()

    # print decoded computer selection
    print(f"Computer chose {decode[choice]}! ", end='')

    return choice


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


# cin -> computer input
# uin -> user input
def rps():
    uin = ""
    rps_prompt = """
        Choose:
        1) Rock
        2) Paper
        3) Scissors

        (Press Q to quit)
    """

    global userResponses
    while uin != "Q":
        print(f"Computer: {score[1]} | User: {score[0]}")
        print(userResponses)
        # reset uin
        uin = ""
        # prompt user response
        print(rps_prompt)
        # continue asking for same round if input is invalid
        while uin != "1" and uin != "2" and uin != "3":
            print('Enter: ', end='')
            # get input
            uin = input().strip(' ')
            # check input
            if uin in decode.keys():
                # clear console screen
                os.system('cls')
                # print decoded user selection to console
                print(f"User chose {decode[uin]}! ", end='')
                # add user responses to global list
                userResponses.append(uin)
                # get random computer response
                cin = generate_response()
                # print outcome to console
                generate_outcome(cin, uin)
            elif uin == 'Q':
                break
            else:
                print("Try again...")

    # end of game
    # loop back to menu
    run()


def predict(model, predictionSequence):
    prediction = model.predict(predictionSequence)
    print(f"{prediction}")
    return prediction


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

    model.fit(trainData, trainLabels, epochs=200, verbose=0)\

    return model


def run():
    play = menu()

    # if user chooses play from menu, game begins
    if play:
        rps()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="This application intends to apply machine learning algorithms to learn a player's rock-paper-scissors strategy, after continuos runs.")

    run()
