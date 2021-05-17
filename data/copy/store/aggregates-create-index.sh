#!/usr/bin/env sh

# sqlite3 innos.db << EOF
#   PRAGMA temp_store = 1;
#   PRAGMA temp_store_directory = '/home/SAMFYB/repos/diversity-innovation/data/copy/store/tmp';
#
#   PRAGMA temp_store;
#   PRAGMA temp_store_directory;
#
#   CREATE INDEX idx_author ON innovations(author);
# EOF
#
# sqlite3 innos.db << EOF
#   PRAGMA temp_store = 1;
#   PRAGMA temp_store_directory = '/home/SAMFYB/repos/diversity-innovation/data/copy/store/tmp';
#
#   PRAGMA temp_store;
#   PRAGMA temp_store_directory;
#
#   CREATE INDEX idx_project ON innovations(project);
# EOF

sqlite3 innos.db "SELECT MIN(timestamp), MAX(timestamp) FROM innovations;" > aggregates-timestamp-range.log
sqlite3 innos.db "SELECT COUNT(project) FROM innovations;" > aggregates-count-project.log
sqlite3 innos.db "SELECT COUNT(author) FROM innovations;" > aggregates-count-author.log

