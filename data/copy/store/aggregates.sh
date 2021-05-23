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

# sqlite3 innos.db "SELECT MIN(timestamp), MAX(timestamp) FROM innovations;" > aggregates-timestamp-range.data
# sqlite3 innos.db "SELECT COUNT(DISTINCT project) FROM innovations;" > aggregates-count-project.data
# sqlite3 innos.db "SELECT COUNT(DISTINCT author) FROM innovations;" > aggregates-count-author.data

# sqlite3 innos.db "SELECT COUNT(*), project FROM innovations WHERE impact >= 2 GROUP BY project;" > aggregates-count-by-project.data
# sqlite3 innos.db "SELECT COUNT(*), author FROM innovations WHERE impact >= 2 GROUP BY author;" > aggregates-count-by-author.data

cat aggregates-count-by-project.data | sort -nr > aggregates-count-by-project.sort.data
cat aggregates-count-by-author.data | sort -nr > aggregates-count-by-author.sort.data

