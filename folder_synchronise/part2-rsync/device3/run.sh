#!/bin/sh
while inotifywait -r -e MODIFY,DELETE,CREATE /home/device3/D; do
  rsync -azh /home/device3/D device1@127.0.1.1: --delete --ignore-errors
  rsync -azh /home/device3/D device2@127.0.2.1: --delete --ignore-errors
done
