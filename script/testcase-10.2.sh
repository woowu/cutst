#!/bin/bash

usage="$(basename "$0") iteration_nr com_port meter_no"

if [ "$1" == "-h" ]; then
    echo "$usage"
    exit
fi

syslog -m start
sleep 2

rundlt645.sh /dev/tts$(($2 - 1)) $3 sky $1 \
    2>&1 | cut -d' ' -f3- | logger --id &

