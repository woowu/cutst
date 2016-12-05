#!/bin/bash

usage="$(basename "$0") iteration_nr com_port hdlc_addr \
profile_start_time profile_end_time"

FIFO=/dev/shm/$(basename "$0").fifo
LOG=/dev/shm/$(basename "$0").log

iterations=$1
dev=/dev/tts$(($2 - 1))
hdlc_addr=$3
profile_start="$4"
profile_end="$5"

test_prg_pid=

function on_exit {
    echo exiting
    if [ -n $test_prg_pid ]; then
        kill $test_prg_pid
    fi
    rm -f $FIFO
    exit 
}

function start_test_prg {
    echo "to start test program"
    xdlms2 --brief --no-reg --loops $iterations --aa-lifetime 120 \
        --lp-read-sliding-window \
        --lp-sliding-window-start "$profile_start" \
        --lp-sliding-window-end "$profile_end" \
        --lp-sliding-window-width 1 \
        --lp-sliding-window-step 900 \
        $dev $hdlc_addr 21234567 9600 2 \
        >&3 2>&3 &
    test_prg_pid=$!
    echo "test process $test_prg_pid started in background"
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
start_test_prg
sleep 1
echo "output is senting to $LOG"

while true; do
    read line <&3
    echo "$line" >>$LOG
    sz=$(stat -c '%s' $LOG)
    if [ $sz -gt 2097152 ]; then
        rm -f $LOG
    fi
done

