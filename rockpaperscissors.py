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

# numSteps = 10
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

winToLose = {
    '1': '3',
    '2': '1',
    '3': '2'
}

loseToWin = {
    '1': '2',
    '2': '3',
    '3': '1'
}


def clearScreen():
    # clear console screen
    os.system('cls')


def splitSequence(sequence, numSteps):
    data = []
    labels = []

    if len(sequence) <= numSteps:
        return np.array(data), np.array(labels)

    for index in range(len(sequence) - (numSteps + 1)):
        chunk = sequence[index:index + numSteps + 1]

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
    numSteps = len(userResponses) - 1
    if(numSteps < 0):
        numSteps = 0
    elif(numSteps > 7):
        numSteps = 7

    data, labels = splitSequence(userResponses, numSteps)

    if (len(data) > 0 and len(labels) > 0):
        data = data.reshape((data.shape[0], data.shape[1], numFeatures))

        model = trainModel(data, labels, numSteps, numFeatures)
        clearScreen()

        testData = np.array(userResponses[-numSteps:])
        testData = testData.reshape((1, numSteps, numFeatures))

        prediction = model.predict(testData, verbose=0)[0][0]
        clearScreen()
        print(f"prediction: {prediction}")
        prediction = round(prediction)

        if prediction < 1:
            prediction = 1

        elif prediction > 3:
            prediction = 3

        return loseToWin[f"{prediction}"]

    return str(randrange(1, 4))


def generate_outcome(computerChoice, userChoice):
    if winToLose[userChoice] == computerChoice:
        score[0] += 1
        print('User WINS! Computer LOSES!')
    elif userChoice == computerChoice:
        print('TIE!!!')
    else:
        score[1] += 1
        print('Computer WINS! User LOSES!')


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


def trainModel(data, labels, numSteps, numFeatures):
    model = tf.keras.Sequential()
    model.add(layers.LSTM(
        50,
        activation='relu',
        input_shape=(numSteps, numFeatures)
    ))

    model.add(layers.Dense(1))

    model.compile(
        optimizer=tf.keras.optimizers.Adam(0.01),
        loss=tf.keras.losses.MeanSquaredError(),
        metrics=['accuracy']
    )

    model.fit(data, labels, epochs=200, verbose=0)

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
