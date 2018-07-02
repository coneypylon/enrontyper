'''This is the main typing tutor for the enrontyper program.

It takes no input, and displays to the console.

'''

import os
import time
import sqlite3
import random

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

def login(namey,db="../DB/emails.db"):
    '''Logs in. For right now, it matches the namey in the database, and
    returns the UID for the user.

    :param namey: A string, representing the users name.

    :returns: An integer, the UID.

    >>> login("Bob")
    23
    '''
    if not os.path.exists(db):
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("CREATE TABLE EMAILS (EID INT, USER TEXT, BODY LONGTEXT, DIFFICULTY REAL, COMBS LONGTEXT)")
        c.execute("CREATE TABLE PLAYERS (UID INT, USERNAME TINYTEXT, COMBSCORES LONGTEXT)")
        c.execute("CREATE TABLE COMBS (COMB TINYTEXT, TYPED BIGINT, TYPEDCORRECT BIGINT, DIFFICULTY FLOAT, BESTEMAILS LONGTEXT)")
        conn.commit()
    else:
        conn = sqlite3.connect(db)
        c = conn.cursor()
    try:
        c.execute('SELECT UID FROM PLAYERS WHERE USERNAME =?', (namey,))
        t = c.fetchone()[0]
        conn.close()
        return int(t)
    except TypeError: # not in DB
        try:
            c.execute("SELECT MAX(UID) FROM PLAYERS")
            t = int(c.fetchone()[0]) + 1
            c.execute("INSERT INTO PLAYERS VALUES (?,?, NULL);", (t, namey))
            conn.commit()
            conn.close()
            return t
        except TypeError: # nobody in DB
            t = 1
            c.execute('INSERT INTO PLAYERS VALUES (?,?, NULL);', (t, namey))
            conn.commit()
            conn.close()
            return t

def getrandemail(db="../DB/emails.db"):
    '''Gets a random email from the database and returns a tuple of
    the EID and the body text of the email.

    :param db: The sqlite3 database to connect to.

    :returns: A tuple of the EID and the body of the email.

    >>> getrandemail()
    (1234,"Hey Bob, nice meeting.")
    '''
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()

        findMax = "SELECT * FROM EMAILS"
        c.execute(findMax)

        t = c.fetchone()
        print(t)
        maxEID = int(t)

        EID = random.randint(1,maxEID)

        c.execute('SELECT BODY FROM EMAILS WHERE EID=?;', (EID,))

        body = c.fetchone()[0]

        return (EID,body)
    except Exception as e:
        print(str(e))
        sys.exit()

def main(db="../DB/emails.db"):
    '''The main runtime. Runs the program when called, starts with a login,
    followed by actually doing stuff.

    Returns 0 if exited successfully, and 999999 when unsuccessful.
    '''
    clearscreen()
    print("Welcome to enrontyper!")
    namey = input("Please enter your name: ")
    uid = login(namey,db) # the logging in.
    print("Welcome, User %s" % uid)
    RUNNING = True
    while RUNNING:
        curmode = input("Which mode to play? (Random,Tailored): ")
        if curmode.lower() == "random":
            # test random email.
            curemail = getrandemail(db)
            print(curemail)

        else:
            raise NotImplementedError

if __name__ == "__main__":
    main()
