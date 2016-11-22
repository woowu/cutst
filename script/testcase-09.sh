#!/bin/bash

LOG_SERVER=10.86.201.53
N_ITERATIONS=50000

# CU+ZQ(H02): Dl645 + Dlms via CU
#
xdlms2 --allow-event-acq --allow-sync-clock --default-intvl 2 --loops $N_ITERATIONS \
    /dev/tts6 7615 21234567 9600 2 | nc $LOG_SERVER 2120 &
rundlt645.sh /dev/tts7 85786615 weisheng $N_ITERATIONS | nc $LOG_SERVER 2121 &

