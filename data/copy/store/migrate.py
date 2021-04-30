from __future__ import print_function
import sys
import datetime
import sqlite3

def eprint(*args, **kwargs):
  print(*args, file = sys.stderr, **kwargs)

def insert(c, values):
  c.execute('insert into innovations(packages, project, timestamp, author, impact) values(?,?,?,?,?)', values)

def incre_impact(c, packages, delta_impact):
  c.execute('update innovations set impact = impact + ? where packages = ?', (delta_impact, packages))

if __name__ == '__main__':

  if len(sys.argv) <= 3:
    print('Specify data table and range!')
    sys.exit(-1)

  fn = sys.argv[1]
  lo = int(sys.argv[2])
  hi = int(sys.argv[3])

  f = open(fn, 'r')
  print('Open table ' + fn)
  t = [l.strip().split(';') for l in f]

  print('Table size = ' + str(len(t)))

  connection = sqlite3.connect('innos.db')
  c = connection.cursor()
  print('Connected to database')
  for i in range(lo, hi):
    if i % 1000000 == 0:
      print('[debug] {' + str(datetime.datetime.now()) + '} Migrate ' + str(i) + '.')
    entry = t[i]
    pkgA, pkgB, project, timestamp, author, impact = entry
    packages = pkgA + ';' + pkgB
    try:
      insert(c, (packages, project, timestamp, author, impact))
    except sqlite3.ProgrammingError:
      eprint('ProgrammingError ' + str(i))
    except sqlite3.IntegrityError:
      eprint('IntegrityError ' + str(i) + ' [' + packages + ']')
      try:
        incre_impact(c, packages, impact)
      except:
        print('Error ' + str(i))
  connection.commit()
  print('Committed to database')
  connection.close()

