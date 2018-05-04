'''Evaluates the emails in Emails, adding them to emails.db if need be.
Creates emails.db if need be.

Make sure the emails in Emails are flattened

v1.0 - coneypylon
'''

import os
import sqlite3
import re

def findcombs(string):
    '''Iterates through a string and returns a list of the combinations with the counts
    
    :param string: a string
    
    :returns: a dict of strings

    >> findcombs("abcdef")
    {'ab':1,'bc':1,'de':1,'ef':1}
    '''
    retdict = {}
    for i in range(0,len(string))
        if i != len(string):
            comb = string[i:i+1]
            try:
                retdict[comb] += 1
            except KeyError:
                retdict[comb] = 1
    return retdict

def clean(email):
    '''returns the last reply in an email (first block of text).
    Doesn't do this yet.

    :param email: A path to an email
    
    :returns: a string with only the body.
    
    >>>clean('lorem ipsum
              >> lorem')
    'lorem ipsum'
    '''
    start = False
    out = []
    with open(email,"r") as f:
        s = f.readline()
        while s != '':
            if start:
                out.append(s)
                s = f.readline()
            elif "X-FileName" in s:
                start = True
                s = f.readline()s
    return email

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

emails = "..\\Emails\\"
emaildirc = os.listdir(emails)

try:
    c.execute("SELECT MAX(EID) FROM EMAILS")
    maxEID = int(c.fetchone()[0])
except:
    maxEID = 1

for email in emaildirc:
    cleanmail = clean(emails + email)
    if not "address" in cleanmail:    
        t = findcombs(cleanmail)
        # time to insert it into the DB!
    else:
        os.remove(emails + email)
    
	