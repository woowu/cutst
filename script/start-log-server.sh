#!/bin/bash

start_port=$1
end_port=$2
for p in `seq $start_port $end_port`; do
	socat -u TCP4-LISTEN:$p,reuseaddr,fork GOPEN:/home/portable1/Q189-test-logs/$p.log,append &
done

