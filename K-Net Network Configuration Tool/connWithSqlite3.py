#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3

conn = sqlite3.connect('data/deviceinfo.db')

print("connecting to the deviceinfo.db")

cur = conn.cursor()
cur.execute('''CREATE TABLE deviceinfo
       (id             INTEGER PRIMARY KEY ,
       deviceType     TEXT    NOT NULL,
       hostname       TEXT    NOT NULL,
       ipAddress      TEXT    NOT NULL,
       username       TEXT    NOT NULL,
       password       TEXT    NOT NULL,
       enable         TEXT    NOT NULL);''')

print ("Table created successfully")
conn.commit()
conn.close()
