import numpy as np
import pandas as pd
import sqlite3
from pandas import *
import pandas.io.sql as sql
import json
import pickle

conn = sqlite3.connect("toolusage.db")
cur = conn.cursor()

def test():
    df = pd.read_sql('select * from users', conn)
    fileop = open("data.json","wb")
    pickle.dump(df,fileop)
    fileop.close()
    return pickle.load(open("data.json","rb"))

print test()

def graph1_data():
#Graph1: Tool usage based on duration of all users
    conn1 = sqlite3.connect("toolusage.db")
    df = pd.read_sql('select toolid, sum(duration) from sessiondata group by toolid', conn1)
    fileop = open("data.json","wb")
    pickle.dump(df.to_json(),fileop)
    fileop.close()
    return pickle.load(open("data.json","rb"))

def graph2_data():
#Graph2: Max tool usage based on no. of users
    conn1 = sqlite3.connect("toolusage.db")
    df = pd.read_sql('select sessiondata.toolid, count(distinct(usersession.userid)) as numOfUsers from sessiondata, usersession where sessiondata.sessionid = usersession.sessionid group by sessiondata.toolid', conn1)
    fileop = open("data.json","wb")
    pickle.dump(df.to_json(),fileop)
    fileop.close()
    return pickle.load(open("data.json","rb"))
print graph2_data()

def graph3_data():
#Graph3: Min used tool
    df = pd.read_sql('select sessiondata.toolid, count(sessiondata.toolid) from sessiondata group by sessiondata.toolid', conn)
    fileop = open("data.json","wb")
    pickle.dump(df.to_json(),fileop)
    fileop.close()
    return pickle.load(open("data.json","rb"))
