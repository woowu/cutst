#!/bin/bash

iterations=$1
shift
if [ -z $iterations ] || [ $iterations -le 0 ]; then
    exit 1
fi
[ "$CUTST_LOGSERVER" != "" ] || CUTST_LOGSERVER=10.86.201.53

killall 00
syslog -m start
sleep 5
while [[ $# -gt 0 ]]; do
    rundlt645.sh /dev/tts$(($1 - 1)) $2 weisheng $iterations 2>&1 | cut -d' ' -f3- | logger --id &
    shift
    shift
done

