#!/bin/bash

for p in `seq 2030 2035`; do
	socat -u TCP4-LISTEN:$p,reuseaddr,fork GOPEN:/home/woody/work/Q189-F11-logs/$p.log,append &
done

