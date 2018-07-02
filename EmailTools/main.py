'''This is the main typing tutor for the enrontyper program.

It takes no input, and displays to the console.

'''

import os
import time
import sqlite3

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

def login(namey):
    '''Logs in. For right now, it matches the namey in the database, and
    returns the UID for the user.

    :param namey: A string, representing the users name.

    :returns: An integer, the UID.

    >>> login("Bob")
    23
    '''
    if not os.path.exists("..\\DB\\emails.db"):
        conn = sqlite3.connect('..\\DB\\emails.db')
        c = conn.cursor()
        c.execute("CREATE TABLE EMAILS (EID INT, USER TINYTEXT, BODY LONGTEXT, DIFFICULTY FLOAT, COMBS LONGTEXT)")
        c.execute("CREATE TABLE PLAYERS (UID INT, USERNAME TINYTEXT, COMBSCORES LONGTEXT)")
        c.execute("CREATE TABLE COMBS (COMB TINYTEXT, TYPED BIGINT, TYPEDCORRECT BIGINT, DIFFICULTY FLOAT, BESTEMAILS LONGTEXT)")
        conn.commit()
    else:
        conn = sqlite3.connect('..\\DB\\emails.db')
        c = conn.cursor()
    try:
        c.execute('SELECT UID FROM PLAYERS WHERE USERNAME =?', (namey,))
        t = c.fetchone()[0]
        return int(t)
    except TypeError: # not in DB
        try:
            c.execute("SELECT MAX(UID) FROM PLAYERS")
            t = int(c.fetchone()[0]) + 1
            c.execute("INSERT INTO PLAYERS VALUES (?,?, NULL);", (t, namey))
            conn.commit()
            return t
        except TypeError: # nobody in DB
            t = 1
            c.execute('INSERT INTO PLAYERS VALUES (?,?, NULL);', (t, namey))
            conn.commit()
            return t



def main():
    '''The main runtime. Runs the program when called, starts with a login,
    followed by actually doing stuff.

    Returns 0 if exited successfully, and 999999 when unsuccessful.
    '''
    clearscreen()
    print("Welcome to enrontyper!")
    namey = input("Please enter your namey: ")
    uid = login(namey) # the logging in.
    print("Welcome, User %s" % uid)

if __name__ == "__main__":
    main()
