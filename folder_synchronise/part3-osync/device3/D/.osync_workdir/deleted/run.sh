#!/bin/sh
loop_rsync_call(){
	while ! ping -q -c 1 -W 1 8.8.8.8 >/dev/null ; do : 
	done
	rsync -azh /home/device2/D device3@127.0.3.1: --delete --ignore-errors
}

loop_rsync_call
while inotifywait -r -e MODIFY,DELETE,CREATE /home/device2/D; do
	loop_rsync_call
done
