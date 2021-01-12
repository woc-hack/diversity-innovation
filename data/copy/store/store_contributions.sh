#!/usr/bin/env sh

project=$1
echo "Lookup contributions for project $project"

entries=$(echo $project | ~/lookup/getValues -f P2c | wc -l)
echo "Found $entries commits in project $project"

echo $project | ~/lookup/getValues -f P2c | cut -d\; -f2 | ~/lookup/getValues c2ta | while read -r timestamp_author
do
  timestamp=$(echo $timestamp_author | cut -d\; -f2)
  author=$(echo $timestamp_author | cut -d\; -f3)

  month_year=$(date +"%-m;%Y" -d @$timestamp)
  month=$(echo $month_year | cut -d\; -f1)
  year=$(echo $month_year | cut -d\; -f2)
  window=$(( ($month - 1) / 3 + ($year - 2008) * 4 ))

  sqlite3 -init init.sql contributions.db "insert into contributions (project, author, window) values (\"$project\", \"$author\", $window);"
done

echo $project >> projects-contributions-done.log

