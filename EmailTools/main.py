'''This is the main typing tutor for the enrontyper program.

It takes no input, and displays to the console.

'''

import os
import time

def clearscreen():
    try:
        os.system('clear')
    except:
        os.system('clr')

def test(str,FIRSTLINE=False):
    '''displays the string, and waits for input. If the input is shorter than
    the string, keeps receiving input.

    In the future, it might be changed to take a character at a time

    :param str: The string to be tested against

    :returns: A tuple of the number of nonmatching characters and the
    time in seconds for the string.
    '''
    if FIRSTLINE:
        print("Type the following. Press Enter at the end of each line.")

    start = time.time()

    test = input(str)

    while len(test) < len(str):
        test += input()
    end = time.time()

    

def main():
