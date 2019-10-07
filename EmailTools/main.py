'''This is the main typing tutor for the enrontyper program.

It takes no input, and displays to the console.

'''

import os
import time
import sqlite3
import random
import evaluateemail

def clearscreen():
    try:
        os.system('clear')
    except:
        os.system('clr')

def test(string,EID,COMBS,FIRSTLINE=False,line=-1):
    '''displays the string, and waits for input. If the input is shorter than
    the string, keeps receiving input.

    In the future, it might be changed to take a character at a time

    :param str: The string to be tested against
    :param FIRSTLINE: A boolean switch indicating whether this is the first
    line of the email.
    :param line: The number of lines remaining.
    :param EID: The Email ID
    :param COMBS: The two letter combinations in this line.

    :returns: A tuple of a tuple of the number of nonmatching characters and
    incorrect combinations, and the time in seconds for the string.
    '''
    if FIRSTLINE:
        print("EID:%s\nType the following. Press Enter at the end of each line.\n" % EID)
    if line >= 0:
        print("%s lines remain" % line)

    start = time.time()

    test = input(string + "\n")

    while len(test) < len(string):
        test += input()

    end = time.time()
    incorrect = 0
    # check the results
    t = linescore(string,test,COMBS)
    return (t,end - start)

def linescore(string,attempt,COMBS):
    '''Consumes a string, the player's attempt at the string, and a list of
    the combinations of letters in the string. Returns a tuple of the number of
    inccorect characters and a list of the combinations that were incorrect.

    :param string: The correct string
    :param attempt: The player's attempt at the string.
    :param COMBS: A list of the combinations of letters in string.

    :returns: (# of incorrect characters,list of incorrect combinations)
    '''
    incorrect = 0
    inccombs = []
    for char in range(0,len(string)):
        #double minus 1 and double
        if attempt[char] != string[char]:
            incorrect += 1
            if char - 1 >= 0:
                inccombs.append(COMBS[char - 1])
            if char <= len(COMBS) -1:
                inccombs.append(COMBS[char])
    return (incorrect,inccombs)

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
        c.execute("CREATE TABLE PLAYERS (UID INT, USERNAME TINYTEXT, COMBSCORES LONGTEXT, MAXLEN INT)")
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
            c.execute("INSERT INTO PLAYERS VALUES (?,?, NULL, 30);", (t, namey))
            conn.commit()
            conn.close()
            return t
        except TypeError: # nobody in DB
            t = 1
            c.execute('INSERT INTO PLAYERS VALUES (?,?, NULL, 30);', (t, namey))
            conn.commit()
            conn.close()
            return t

def getfromdb(word):
    '''gets something from dynamoDB
    '''
    t = evaluateemail.fetch(word)
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

def findcombs(LINES):
    '''combs through a list of strings, returns a list of the same length of
    the two letter combinations in those strings.

    :param LINES: A list of strings

    :returns: A list of lists of two letter combinations for that
    same list of strings.

    >>> findcombs(["abc,defg"])
    [["ab","bc"],["de","ef","fg"]]
    '''
    outlst = []
    for line in range(0,len(LINES)):
        outlst.append([])
        for char in range(0,len(LINES[line])):
            if char != len(LINES[line]) -1 : # it's not the last character
                outlst[line].append(LINES[line][char:char + 2])
    return outlst

def preplines(MAXL,TYP):
    '''Consumes a maximum number of lines, and a string indicating the type
    of lines to give (random or tailored.)

    :param MAXL: An integer, giving the max number of lines.
    :param TYP: The word that we want as the most common word.

    :returns: A tuple of a list of lines, the number of words in the lines,
    the EID, and a list of the combinations of letters present in the lines.
    '''
    curemail = getfromdb(TYP)
    lines = curemail[1].split("\n")

    while len(lines) > MAXL:
        curemail = getrandemail(db)
        lines = curemail[1].split("\n")

    WORDCOUNT = len(curemail[1].split(' '))
    outlines = []
    for line in lines:
        tline = line.strip()
        if len(tline) > 1:
            outlines.append(tline)
    combs = findcombs(outlines)
    return (outlines,WORDCOUNT,curemail[0],combs)


def main(db="../DB/emails.db"):
    '''The main runtime. Runs the program when called, starts with a login,
    followed by actually doing stuff.

    Returns 0 if exited successfully, and 999999 when unsuccessful.
    '''
    clearscreen()
    print("Welcome to enrontyper!")
    namey = input("Please enter your name: ")
    uid = login(namey,db) # the logging in.
    MAXLEN = int(getfromdb("SELECT MAXLEN FROM PLAYERS WHERE UID=%s" % uid, db)[0][0])
    print("Welcome, User %s" % uid)
    RUNNING = True
    while RUNNING:
        curmode = input("Which mode to play? (Random,Tailored): ")
        if curmode.lower() == "random":
            # test random email.
            linestup = preplines(MAXLEN,"_random")
            lines = linestup[0]
            totallines = len(lines)
            totaltime = 0
            totalmistakes = 0
            totalchars = 0
            badcombs = []
            first = True
            for line in range(0,len(lines)):
                t = test(lines[line],linestup[2],linestup[3][line],first,len(lines) - line)
                first = False
                totaltime += t[1]
                totalmistakes += t[0][0]
                totalchars += len(lines[line])
                badcombs.extend(t[0][1])
            t = score(totaltime,totalmistakes,totalchars)
            print("Your weighted CPM was %s, and your raw CPM was %s!" % (t,totalchars/totaltime*60)) # say more about thsi
            print("You typed %s WPM!" % ((linestup[1]/totaltime)*60))
            print("Your mistaken character combinations were %s" % badcombs)

        else:
            RUNNING = False

if __name__ == "__main__":
    main()
