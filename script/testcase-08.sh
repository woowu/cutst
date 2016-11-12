#!/bin/bash

LOG_SERVER=10.86.201.53
N_ITERATIONS=50000

# CU+ZQ: Dual Dlms via CU
#
xdlms --allow-event-acq --allow-sync-clock --default-intvl 2 --loops $N_ITERATIONS \
    /dev/tts8 10462 21234567 9600 2 | nc $LOG_SERVER 2100 &
xdlms --allow-event-acq --allow-sync-clock --default-intvl 2 --loops $N_ITERATIONS \
    /dev/tts9 10462 21234567 9600 2 | nc $LOG_SERVER 2101 &

# CU+ZQ: CU dlms (tts10) + meter dlms (tts11)
#
xdlms --allow-event-acq --allow-sync-clock --default-intvl 2 --loops $N_ITERATIONS \
    /dev/tts10 1165 21234567 9600 2 | nc $LOG_SERVER 2102 &
xdlms --allow-event-acq --allow-sync-clock --default-intvl 2 --loops $N_ITERATIONS \
    /dev/tts11 1165 21234567 9600 2 | nc $LOG_SERVER 2103 &

# CU+ZQ: Dl645 + Dlms via CU
#
xdlms --allow-event-acq --allow-sync-clock --default-intvl 2 --loops $N_ITERATIONS \
    /dev/tts6 7421 21234567 9600 2 | nc $LOG_SERVER 2104 &
rundlt645.sh /dev/tts7 51510663 weisheng $N_ITERATIONS | nc $LOG_SERVER 2105 &

