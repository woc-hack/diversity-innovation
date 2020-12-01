#!/usr/bin/env sh

while read p; do
  zcat /da0_data/play/JSthruMaps/PtaPkgRJS.*.s | grep "$p" | sort > data/projects/entries."$p".log
done < data/project-finder.log

