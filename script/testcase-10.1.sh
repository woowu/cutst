#!/bin/bash

usage="$(basename "$0") iteration_nr com_port hdlc_addr \
profile_start_time profile_end_time"

if [ "$1" == "-h" ]; then
    echo "$usage"
    exit
fi

syslog -m start
sleep 2

xdlms2 --brief --no-reg --loops $1 --aa-lifetime 120 \
    --lp-read-sliding-window \
    --lp-sliding-window-start "$4" \
    --lp-sliding-window-end "$5" \
    --lp-sliding-window-width 1 \
    --lp-sliding-window-step 900 \
    /dev/tts$(($2 - 1)) $3 21234567 9600 2 \
    2>&1 | cut -d' ' -f2- | logger --id &

