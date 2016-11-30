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
    rundlms-gen.sh $1 $iterations 2>&1 | cut -d' ' -f2- | logger --id &
    shift
done

