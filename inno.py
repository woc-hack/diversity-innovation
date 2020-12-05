import sys
import datetime
import gzip

def parseline(line):
  """ parse by line from PtaPkgRJS.{0..127}.s tables
  entries format is project, time, author, packages """
  tokens = line.strip().split(';')
  timestamp, project, author, packages = tokens[0], tokens[1], tokens[2], tokens[3:]
  return project, timestamp, author, packages

###############################################################################

def write_project_packages_mem_table(table):
  """ to run script on raw data tables one by one (to avoid consuming too much memory)
  we need to memorize most up-to-date project packages table """
  with open('data/ppkgs.mem', 'w') as f:
    f.write('\n'.join(project + ';' + ';'.join(table[project]) for project in table))
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

###############################################################################

def write_innovations_mem_table(table):
  """ run script on raw tables one by one produce innovations map each time """
  def mk_entry(innovation):
    pkgA, pkgB = innovation
    project, timestamp, author, count = table[innovation]
    return ';'.join([pkgA, pkgB, project, timestamp, author, str(count)])
  with open('data/innos.mem', 'w') as f:
    f.write('\n'.join(mk_entry(innovation) for innovation in table))
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

###################################################################################################

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

###############################################################################

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

###############################################################################

# project -> seen packages set
  project_packages_map = read_project_packages_mem_table()
# package pair -> (earliest seen) project, timestamp, author, occurance count
  innovations = read_innovations_mem_table()

  print('[debug] {' + str(datetime.datetime.now()) + '} Done read mem tables. Start read from stdin.')
  line_count = 0
  if len(sys.argv) <= 2:
    print('Specify data process range! (lower inclusive, upper exclusive)')
    sys.exit(-1)
  read_data_lower = int(sys.argv[1])
  read_data_upper = int(sys.argv[2])
  print('Read data to process from line >= ' + str(read_data_lower) + ' to < ' + str(read_data_upper))

  with gzip.open('/da0_data/play/JSthruMaps/tPaPkgRJS.s', 'r') as data_f:
    for line in data_f:
      line_count += 1
      if line_count < read_data_lower:
        continue # not yet start process data in range
      if line_count >= read_data_upper:
        print('[debug] {' + str(datetime.datetime.now()) + '} Done entire specified data process range.')
        break # ignore more stdin if limit specified
      if line_count in [3043426, 3050807, 3050808, 3067991, 3067992, 3127315, 4616934, 5225409,
          16876583, 18322303, 18322824, 18322934, 18323512, 18324553, 18326294, 18326757,
          18327082, 18327143, 18327707, 18327849, 18327932, 20699005, 20699163, 20699599,
          20699729, 20832248, 25887024, 38223498]:
        continue # line too long

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

      if line_count % 10000 == 9999:
        print('[debug] {' + str(datetime.datetime.now()) + '} Done processing stdin line ' + str(line_count) + '.')

  print('Processed data upto (in/ex) ' + str(line_count))
  print('[debug] {' + str(datetime.datetime.now()) + '} Done innovations from stdin. Start write new mem tables.')
  write_project_packages_mem_table(project_packages_map)
  write_innovations_mem_table(innovations)

