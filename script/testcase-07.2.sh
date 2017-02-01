#!/bin/bash

usage="$(basename "$0") iteration_nr com_port meter_no"

if [ "$1" == "-h" ]; then
    echo "$usage"
    exit
fi

iterations=$1
shift
if [ -z $iterations ] || [ $iterations -le 0 ]; then
    exit 1
fi

killall 00
syslog -m start
while [[ $# -gt 0 ]]; do
    rundlt645.sh /dev/tts$(($1 - 1)) $2 weisheng $iterations 2>&1 \
        | cut -d' ' -f3- | logger --id &
    shift
    shift
done

