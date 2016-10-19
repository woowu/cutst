#!/bin/bash

dev=$1
meter_no=$2
policy=$3
iterations=$4
if [[ ! -c $dev ]]; then
    echo no device
    exit 1
fi
if [[ -z $meter_no ]]; then
    echo no meter_no
    exit 1
fi
if [[ ! $iterations -gt 0 ]]; then
    echo bad iterations
    exit 1
fi

if [[ $policy == "weisheng" ]]; then
    dlt645tst.py $dev -n$iterations -tweisheng -d4 -s $meter_no
else
    dlt645tst.py $dev -n$iterations -tkeli -d2 $meter_no
fi

