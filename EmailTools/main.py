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

def test(string,FIRSTLINE=False,line=-1):
    '''displays the string, and waits for input. If the input is shorter than
    the string, keeps receiving input.

    In the future, it might be changed to take a character at a time

    :param str: The string to be tested against

    :returns: A tuple of the number of nonmatching characters and the
    time in seconds for the string.
    '''
    if FIRSTLINE:
        print("Type the following. Press Enter at the end of each line.\n")
    if line >= 0:
        print("%s lines remain" % line)

    start = time.time()

    test = input(string + "\n")

    while len(test) < len(string):
        test += input()

    end = time.time()
    incorrect = 0
    # check the results
    for character in range(0,len(string)):
        if test[character] != string[character]:
            incorrect += 1
    return (incorrect,end - start)


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

        findMax = "SELECT MAX(EID) FROM EMAILS"
        c.execute(findMax)

        t = c.fetchone()[0]
        maxEID = int(t)

        EID = random.randint(1,maxEID)

        c.execute('SELECT BODY FROM EMAILS WHERE EID=?;', (EID,))

        body = c.fetchone()[0]

        return (EID,body)
    except Exception as e:
        print(str(e))
        sys.exit()

def score(ttime,tmistakes,tchars):
    '''Processes the total time, total mistakes, and total characters into
    a score that amounts to your characters per minute minus your mistakes,
    which are divided by the total number of characters.
    '''
    cpm = tchars/ttime * 60
    acpm = cpm - tmistakes/tchars
    return acpm

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
            lines = len(curemail[1].split("\n"))
            totaltime = 0
            totalmistakes = 0
            totalchars = 0
            first = True
            for line in curemail[1].split("\n"):
                if not line == "":
                    line = line.strip()
                    t = test(line,first,lines)
                    first = False
                    totaltime += t[1]
                    totalmistakes += t[0]
                    totalchars += len(line)
                    lines -= 1
            t = score(totaltime,totalmistakes,totalchars)
            print("Your score was %s!" % t) # say more about thsi

        else:
            RUNNING = False

if __name__ == "__main__":
    main()
