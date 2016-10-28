#!/bin/sh

meter_no=$1
iterations=$2
if [[ ! $meter_no -gt 0 ]]; then
    echo need meter_no
    exit 1
fi
if [[ ! $iterations -gt 0 ]]; then
    echo bad iterations
    exit 1
fi
if [[ ! -f /ffc/cfg/config.db ]]; then
    echo no config
    exit 1
fi

com_no=`sqlite3 /ffc/cfg/config.db "select ncomid from meterunitconfig where nmeterid=$meter_no;"`
baud_idx=`sqlite3 /ffc/cfg/config.db "select nbaudft from meterunitconfig where nmeterid=$meter_no;"`
if [[ ! $com_no -gt 0 ]]; then
    echo bad com_no
    exit 1
fi
if [[ ! $baud_idx -gt 0 ]]; then
    echo bad baud_idx
    exit 1
fi

period=120
i=0
while [[ $i -lt $iterations ]]; do
    now=`date +%s`
    t=`expr $now / $period \* $period`
    echo "iteration $i"
    echo 270 -L --brief --no-save --no-lp --no-last-value \
        $com_no $meter_no $baud_idx \
        $t 1
    270 -L --brief --no-save --no-lp --no-last-value \
        $com_no $meter_no $baud_idx \
        $t 1
    if [[ $? -ne 0 ]]; then
        echo "ERR: xdlms error, exit code = $?"
        sleep 200
    fi
    i=`expr $i + 1`
done

