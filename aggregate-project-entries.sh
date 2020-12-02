#!/usr/bin/env sh

while read p; do
  zcat /da0_data/play/JSthruMaps/tPaPkgRJS.s | grep "$p" > data/projects/entries."$p".log
done <&0

