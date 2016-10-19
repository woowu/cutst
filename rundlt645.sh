#!/bin/bash

dev=$1
meter_no=$2

if [[ ! -c $dev ]]; then
    echo no device
    exit 1
fi

if [[ -z $meter_no ]]; then
    echo no meter_no
    exit 1
fi

dlt645tst.py $dev -n100000 -tweisheng -d4 -s $meter_no

