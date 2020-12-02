import sys
import datetime

def parseline(line):
  """ parse by line from PtaPkgRJS.{0..127}.s tables
  entries format is project, time, author, packages """
  tokens = line.strip().split(';')
  timestamp, project, author, packages = tokens[0], tokens[1], tokens[2], tokens[3:]
  return project, timestamp, author, packages

def write_project_packages_mem_table(table):
  """ to run script on raw data tables one by one (to avoid consuming too much memory)
  we need to memorize most up-to-date project packages table """
  with open('data/ppkgs.mem', 'w') as f:
    for project in table:
      packages = table[project]
      f.write(project + ';' + ';'.join(packages) + '\n')
    print('Written project packages mem table')
    return

def read_project_packages_mem_table():
  """ counterpart to write_project_packages_mem_table,
  read the most up-to-date project packages table as baseline for future innovation """
  with open('data/ppkgs.mem', 'r') as f:
    table = {}
    for line in f:
      tokens = line.strip().split(';')
      if len(tokens) <= 1: # ignore invalid lines
        continue
      project, packages = tokens[0], tokens[1:]
      table[project] = set(packages)
    print('Read project packages mem table with ' + str(len(table)) + ' project entries')
    return table

def write_innovations_mem_table(table):
  """ run script on raw tables one by one produce innovations map each time """
  with open('data/innos.mem', 'w') as f:
    for innovation in table:
      project, timestamp, author, count = table[innovation]
      pkgA, pkgB = innovation
      f.write(';'.join([pkgA, pkgB, project, timestamp, author, str(count)]) + '\n')
    print('Written innovations mem table')
    return

def read_innovations_mem_table():
  """ counterpart to write_innovations_mem_table,
  read innovations seen so far as baseline for future innovation updates """
  with open('data/innos.mem', 'r') as f:
    table = {}
    for line in f:
      tokens = line.strip().split(';')
      if len(tokens) < 6: # ignore invalid lines
        continue
      innovation = (tokens[0], tokens[1])
      project, timestamp, author = tokens[2], tokens[3], tokens[4]
      count = int(tokens[5])
      table[innovation] = (project, timestamp, author, count)
    print('Read innovations mem table with ' + str(len(table)) + ' innovation entries')
    return table

if __name__ == '__main__':

  if len(sys.argv) >= 2 and sys.argv[1] == 'projects':
    projects = {}
    for line in sys.stdin:
      project, _t, _a, _p = parseline(line)
      if project not in projects:
        projects[project] = 1
      else:
        projects[project] = projects[project] + 1
    topkeys = sorted(projects.keys(), key = lambda p: projects[p], reverse = True)
    for project in topkeys:
      print(project)
    sys.exit(0)

  if len(sys.argv) >= 3 and sys.argv[1] == 'in-project-innos':
    project = sys.argv[2]
    current_packages = set()
    innovations = {}
    for line in sys.stdin:
      _p, timestamp, author, packages = parseline(line)
      for new_package in packages: # consider new package with every current package
        if new_package in current_packages:
          continue # ignore package already in current packages
        for current_package in current_packages:
          pair = tuple(sorted([new_package, current_package]))
          # it is not possible for pair to be already in innovations
          innovations[pair] = (project, timestamp, author)
        current_packages.add(new_package)
    for pair in innovations:
      pkgA, pkgB = pair
      print(';'.join([pkgA, pkgB, project, timestamp, author, '1']))
    sys.exit(0)

# project -> seen packages set
  project_packages_map = read_project_packages_mem_table()
# package pair -> (earliest seen) project, timestamp, author, occurance count
  innovations = read_innovations_mem_table()

  print('[debug] {' + str(datetime.datetime.now()) + '} Done read mem tables. Start read from stdin.')
  line_count = 0
  for line in sys.stdin:
    line_count += 1
    if line_count % 500 == 0:
      print('[debug] {' + str(datetime.datetime.now()) + '} Processing stdin line ' + str(line_count) + '.')
    project, timestamp, author, packages = parseline(line)
    if project not in project_packages_map:
      project_packages_map[project] = set() # initialize
    for new_package in packages: # consider new package with every existing package
      if new_package in project_packages_map[project]:
        continue # package is already in current packages
      for current_package in project_packages_map[project]:
        pair = tuple(sorted([new_package, current_package])) # unorder
        if pair not in innovations:
          innovations[pair] = (project, timestamp, author, 1)
        else: # innovation exists, only update count
          current_project, current_timestamp, current_author, current_count = innovations[pair]
          innovations[pair] = (current_project, current_timestamp, current_author, 1 + current_count)
      # after new package innovations are done, put new package into current packages
      project_packages_map[project].add(new_package)

  print('[debug] {' + str(datetime.datetime.now()) + '} Done innovations from stdin. Start write new mem tables.')
  write_project_packages_mem_table(project_packages_map)
  write_innovations_mem_table(innovations)

