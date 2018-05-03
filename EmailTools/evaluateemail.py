'''Evaluates the emails in Emails, adding them to emails.db if need be.
Creates emails.db if need be.

Make sure the emails in Emails are flattened

v1.0 - coneypylon
'''

import os
import sqlite3

if not os.path.exists("..\\DB\\emails.db"):
	conn = sqlite3.connect('..\\DB\\emails.db')
	c = conn.cursor()
	c.execute("CREATE TABLE EMAILS (EID INT, USER TINYTEXT, BODY LONGTEXT, DIFFICULTY FLOAT, COMBS LONGTEXT)")
	c.execute("CREATE TABLE PLAYERS (UID INT, USERNAME TINYTEXT, COMBSCORES LONGTEXT)")
	c.execute("CREATE TABLE COMBS (COMB TINYTEXT, TYPED BIGINT, TYPEDCORRECT BIGINT, DIFFICULTY FLOAT, BESTEMAILS LONGTEXT)")
	conn.commit()

emails = "..\\Emails\\"
emaildirc = os.listdir(emails)

for email in emaildirc:
	print(email)