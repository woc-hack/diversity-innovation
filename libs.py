import sys
import csv

proj_libs_map = {}

def parseline(line):
  tokens = line.strip().split(';')
  return tokens[0], tokens[1], tokens[2], tokens[3], tokens[4], tokens[5:]

for line in sys.stdin:
  _b, _c, proj, t, a, libs = parseline(line)
  if proj not in proj_libs_map:
    proj_libs_map[proj] = []
  proj_libs_map[proj].append((t, a, libs))

co_occ_map = {} # map from a pair of co-occurrance libs to list of timed edges

for proj in proj_libs_map:
  entries = sorted(proj_libs_map[proj], key = lambda t: t[0])
  proj_libs = set() # seen proj libs up to some timestamp
  for t, a, libs in entries:
    for new_lib in libs:
      if new_lib not in proj_libs:
        for current_proj_lib in proj_libs:
          # add edge {new_lib, current_proj_lib} to co-occ map
          pair = tuple(sorted([new_lib, current_proj_lib]))
          if pair not in co_occ_map:
            co_occ_map[pair] = []
          co_occ_map[pair].append((t, a, proj))
        proj_libs.add(new_lib)

innovation_map = {}

for pair in co_occ_map:
  sorted_entries = sorted(co_occ_map[pair], key = lambda t: t[0])
  t, a, p = sorted_entries[0]
  innovation_map[pair] = (t, a, p)

f = 'innovations.js.csv'
with open(f, 'w') as csvf:
  writer = csv.writer(csvf)
  writer.writerow(('innovation', 'time', 'author', 'project'))
  for pair in innovation_map:
    t, a, p = innovation_map[pair]
    writer.writerow((str(pair), t, a, p))

