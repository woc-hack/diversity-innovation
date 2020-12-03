#!/usr/bin/env python

import sqlite3
import sys
import datetime

# Create database connection
connection = None
try:
  connection = sqlite3.connect('data/innos.db')
  print(sqlite3.version)
except sqlite3.Error as e:
  print(e)
  sys.exit(-1)
if connection is None:
  print('Connection not established.')
  sys.exit(1)
else:
  print('[debug] {' + str(datetime.datetime.now()) + '} Database connected.')

# Create database table for innovations
sql_create_table = """ CREATE TABLE IF NOT EXISTS innovations (
                              pkgA text NOT NULL,
                              pkgB text NOT NULL,
                              project text NOT NULL,
                              timestamp integer NOT NULL,
                              author text NOT NULL,
                              count integer NOT NULL,
                              PRIMARY KEY (pkgA, pkgB)); """
sql_create_index_on_author = """ CREATE INDEX idx_author ON innovations(author); """
try:
  c = connection.cursor()
  c.execute(sql_create_table)
  c.execute(sql_create_index_on_author)
  connection.commit()
except sqlite3.Error as e:
  print(e)
  sys.exit(-1)
print('[debug] {' + str(datetime.datetime.now()) + '} Created innovations table.')

# Read current innovations mem table from file
import inno
innovations = inno.read_innovations_mem_table()
print('[debug] {' + str(datetime.datetime.now()) + '} Done read innovations from mem table.')

# Insert innovations into database
try:
  lc = 0
  for innovation in innovations:
    lc += 1
    if lc % 1000 == 0:
      print('[debug] {' + str(datetime.datetime.now()) + '} Inserting upto ' + str(lc) + ' innovations into database.')
      connection.commit()
    pkgA, pkgB = innovation
    project, timestamp, author, count = innovations[innovation]
    c = connection.cursor()
    c.execute("INSERT INTO innovations(pkgA, pkgB, project, timestamp, author, count) VALUES(?,?,?,?,?,?)",
        (pkgA, pkgB, project, int(timestamp), author, count))
  connection.commit()
  print('[debug] {' + str(datetime.datetime.now()) + '} Done insert everything into database innovations table.')
except sqlite3.Error as e:
  print(e)
  sys.exit(42)

