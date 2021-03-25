import pickle
from inno import read_project_packages_mem_table as readtable
pickle.dump(readtable(), open('data/ppkgs.p', 'wb'))
