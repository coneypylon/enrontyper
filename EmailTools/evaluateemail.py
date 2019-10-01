'''Evaluates the emails in Emails, adding them to emails.db if need be.
Creates emails.db if need be.

OK.

Make sure the emails in Emails are flattened using transferemails

Emails are assumed to be from https://www.cs.cmu.edu/~enron/

v1.1 - coneypylon
'''

import os
import sqlite3
import re
import json
import boto3
import decimal


### # # ###
# # # # ##
### ###   #
# # ### ###

#
# The following section is redistributed from the AWS DynamoDB guide. Some modification
# has been made to convert their code to functions for put_stuff_in_DB()
#

#
#  Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
#  This file is licensed under the Apache License, Version 2.0 (the "License").
#  You may not use this file except in compliance with the License. A copy of
#  the License is located at
# 
#  http://aws.amazon.com/apache2.0/
# 
#  This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
#  CONDITIONS OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the License.
#

# Helper class to convert a DynamoDB item to JSON. This class is unmodified.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

# somewhat self-explanatory
# This is a modified version of what is provided in the guide for putting items.
def put_stuff_in_DB(stuff):
    '''Adds an item that is stuff to a DynamoDB.
    
    Assumes stuff is a dictionary.
    '''
    
    #region = input("What region is the DynamoDB in? ")
    #endpoint = input("What is the endpoint-url? ")
    table = input("What is the name of the table? ")
    
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table(table)

    mcw = stuff['mcw'] #gonna change this to actually make sense. stuff will be iterated through
    EID = str(stuff['EID']) #here's the problem - this function should be the one to find the EID, not
    #                # whatever is calling this function.
    response = table.put_item(
       Item={
            'most_common_word': mcw,
            'EID': EID,
            'email': {
                'body':stuff['body'], #hmm maybe a dictionary for each makes sense.
            }
        }
    )

    print("PutItem succeeded:")
    print(json.dumps(response, indent=4, cls=DecimalEncoder))

#
# END OF REDISTRIBUTED CODE
#

def findwords(string):
    '''Iterates through a string and returns a list of the combinations with the counts

    :param string: a string

    :returns: a dict of strings

    >> findwords("abcdef")
    {'ab':1,'bc':1,'de':1,'ef':1}
    '''
    retdict = {}
    words = string.split()
    for i in words:
        try:
            retdict[i] += 1
        except KeyError:
            retdict[i] = 1
    return retdict

def find_mcw(email): #this should be a class method
    t = findwords(email)
    cur_mcw = ''
    cur_num = 0
    forbidden = ['the','of','and','not','to','too','in','for']
    for word in t.keys():
        if not word.lower() in forbidden:
            if t[word] > cur_num:
                cur_num = t[word]
                cur_mcw = word
    return cur_mcw

def clean(email):
    '''returns a tuple of the last reply in an email (first block of text) and
    the user.

    :param email: A path to an email

    :returns: a string with only the body.

    >>>clean('lorem ipsum
              >> lorem')
    'lorem ipsum'
    '''
    start = False
    out = ''
    with open(email,"r") as f:
        s = f.readline()
        while s != '':
            if start and not '---' in s and not 'forwarded by' in s:
                out += s
                s = f.readline()
            elif "X-FileName" in s:
                start = True
                s = f.readline()
            elif not start:
                s = f.readline()
            else:
                break
    return out
if not os.path.exists("../DB/emails.db"):
    conn = sqlite3.connect('../DB/emails.db')
    c = conn.cursor()
    c.execute("CREATE TABLE EMAILS (EID INT, USER TINYTEXT, BODY LONGTEXT, DIFFICULTY FLOAT, words LONGTEXT)")
    c.execute("CREATE TABLE PLAYERS (UID INT, USERNAME TINYTEXT, wordsCORES LONGTEXT)")
    c.execute("CREATE TABLE words (COMB TINYTEXT, TYPED BIGINT, TYPEDCORRECT BIGINT, DIFFICULTY FLOAT, BESTEMAILS LONGTEXT)")
    conn.commit()
else:
    conn = sqlite3.connect('../DB/emails.db')
    c = conn.cursor()

emails = "../Emails/"
emaildirc = os.listdir(emails)

try:
    c.execute("SELECT MAX(EID) FROM EMAILS")
    maxEID = int(c.fetchone()[0]) + 1
except:
    maxEID = 1

toexec = []

for email in emaildirc:
    cleanmail = clean(emails + email)
    # this is new - we're going to print every single email out as we go to check if it violates privacy
    # Since this is going to be a web app at some point, we want to ensure that we are not violating privacy
    # I'm gonna have to filter for names at some point. I figure I'll get it to have me read every
    # word with a capital at the front - maybe use Mechanical Turk for this?
    print(cleanmail)
    print(emails + email) # tell me what email I'm looking at
    response = input("Keep email? [Y/N] ")
    if not "address" in cleanmail and not "account" in cleanmail and len(cleanmail) > 1 and response[0].upper() == "Y":
        ts = str(findwords(cleanmail))
        print(ts)
        # time to insert it into the DB!
        t = [maxEID,cleanmail]
        toexec.append(t)
        maxEID += 1
        os.remove(emails + email)
    else:
        os.remove(emails + email)

#print(toexec)

#this is the sloppy way we add it to DynamoDB and sqlite for now.
#sqlite currently serves to give the EID, but that's gonna have to
#change eventually.
for command in toexec:
    print(command)
    try:
        t = [command[0],command[1]]
        DDB_f = {'mcw':find_mcw(command[1]),'EID':command[0],'body':command[1]}
        put_stuff_in_DB(DDB_f) # this sorta makes sense. I'll re-evaluate maybe.
        c.execute('INSERT INTO EMAILS VALUES (?, NULL, ?, NULL, NULL)', t)
    except DivideByZeroError:
        continue

conn.commit()
