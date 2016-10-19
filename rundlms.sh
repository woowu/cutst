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
for i in `seq $iterations`; do
    now=`date +%s`
    t=`expr $now / $period \* $period`
    270 -L $com_no $meter_no $baud_idx $t 1
    if [[ $? -eq 0 ]]; then
        sleep 3
    else
        echo "ERR: xdlms error, exit code = $?"
        sleep 200
    fi
done

