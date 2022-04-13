import argparse
import os
from random import randrange
import Lib

user_responses = []

# Rock 1
# Paper 2
# Scissors 3
decode = {'1':'Rock', '2':'Paper', '3':'Scissors'}
rules = {'1':'3', '2':'1', '3':'2'}


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


def generate_response():
    random = str(randrange(1, 4))

    # print decoded computer selection
    print(f"Computer chose {decode[random]}! ", end='')

    return random 


# cin -> computer input
# uin -> user input
# rules -> global dictionary
def generate_outcome(cin, uin):
    if rules[uin] == cin:
        print('User WINS! Computer LOSES!')
    elif uin == cin:
        print('TIE!!!')
    else:
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

    global user_responses
    while uin != "Q":
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
                user_responses.append(uin)
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


def run():
    play = menu()

    # if user chooses play from menu, game begins
    if play:
        rps()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="This application intends to apply machine learning algorithms to learn a player's rock-paper-scissors strategy, after continous runs.")

    run()