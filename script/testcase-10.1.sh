#!/bin/bash

usage="$(basename "$0") iteration_nr com_port hdlc_addr \
profile_start_time profile_end_time"

OUTDIR=/dev/shm
FIFO=$OUTDIR/$(basename "$0").fifo
LOG=$OUTDIR/$(basename "$0").log

iterations=$1
dev=/dev/tts$(($2 - 1))
hdlc_addr=$3
profile_start="$4"
profile_end="$5"

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
    echo "start xdlms2"
    xdlms2 --brief --no-reg --loops $iterations --aa-lifetime 120 \
        --lp-read-sliding-window \
        --lp-sliding-window-start "$profile_start" \
        --lp-sliding-window-end "$profile_end" \
        --lp-sliding-window-width 1 \
        --lp-sliding-window-step 900 \
        $dev $hdlc_addr 21234567 9600 2 \
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

