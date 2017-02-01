#!/bin/bash

usage="$(basename "$0") iteration_nr com_port meter_no"

OUTDIR=/dev/shm
FIFO=$OUTDIR/$(basename "$0").fifo
LOG=$OUTDIR/$(basename "$0").log

iterations=$1
dev=/dev/tts$(($2 - 1))
meter_no=$3

log_monitor_pid=

function on_exit {
    echo exiting
    if [ -n $log_monitor_pid ]; then
        kill $log_monitor_pid
    fi
    rm -f $FIFO
    exit 
}

function monitor_log {
    while true; do
        read line <&3
        echo "$line" >>$LOG
        sz=$(stat -c '%s' $LOG)
        if [ $sz -gt 2097152 ]; then
            rm -f $LOG
        fi
    done
}

function do_test {
    echo "start dlt645tst.py"
    dlt645tst.py $dev -n$iterations -tsky -d4 -s $meter_no \
        >&3 2>&3
}

if [ "$1" == "-h" ]; then
    echo "$usage"
    exit
fi

trap on_exit SIGTERM SIGINT

if [ ! -p $FIFO ]; then
    mkfifo $FIFO
fi

exec 3<>$FIFO

monitor_log &
log_monitor_pid=$!
echo "monitoring log with process $log_monitor_pid"
echo "logs sent to $LOG"
do_test
on_exit

