#!/usr/bin/env sh

while read p; do
  cat data/projects/entries."$p".log | python inno.py in-project-innos "$p" > data/innos/innos."$p".log
done <&0

