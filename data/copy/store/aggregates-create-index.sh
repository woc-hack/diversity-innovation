#!/usr/bin/env sh

sqlite3 innos.db "CREATE INDEX idx_author ON innovations(author);"

sqlite3 innos.db "CREATE INDEX idx_project ON innovations(project);"

