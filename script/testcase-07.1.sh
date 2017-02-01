#!/bin/bash

usage="$(basename "$0") iteration_nr meter_id"

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
    rundlms-gen.sh $1 $iterations 2>&1 | cut -d' ' -f2- | logger --id &
    shift
done

