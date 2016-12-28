#!/bin/bash

LOG_SERVER=10.86.201.53
N_ITERATIONS=150000

n=1
xdlms2 --allow-event-acq --allow-sync-clock --default-intvl 2 --loops \
    $N_ITERATIONS --aa-lifetime 30 \
    /dev/tts6 3067 21234567 9600 2 | nc $LOG_SERVER 2200 &
rundlt645.sh /dev/tts7 0 sky $N_ITERATIONS | nc $LOG_SERVER 2201 &

n=2
xdlms2 --allow-event-acq --allow-sync-clock --default-intvl 2 --loops \
    $N_ITERATIONS --aa-lifetime 30 \
    /dev/tts8 3068 21234567 9600 2 | nc $LOG_SERVER 2202 &
rundlt645.sh /dev/tts9 0 sky $N_ITERATIONS | nc $LOG_SERVER 2203 &

n=3
xdlms2 --allow-event-acq --allow-sync-clock --default-intvl 2 --loops \
    $N_ITERATIONS --aa-lifetime 30 \
    /dev/tts10 3069 21234567 9600 2 | nc $LOG_SERVER 2204 &
rundlt645.sh /dev/tts11 0 sky $N_ITERATIONS | nc $LOG_SERVER 2205 &

n=4
xdlms2 --allow-event-acq --allow-sync-clock --default-intvl 2 --loops \
    $N_ITERATIONS --aa-lifetime 30 \
    /dev/tts12 3070 21234567 9600 2 | nc $LOG_SERVER 2206 &
rundlt645.sh /dev/tts13 0 sky $N_ITERATIONS | nc $LOG_SERVER 2207 &

n=5
xdlms2 --allow-event-acq --allow-sync-clock --default-intvl 2 --loops \
    $N_ITERATIONS --aa-lifetime 30 \
    /dev/tts14 3071 21234567 9600 2 | nc $LOG_SERVER 2208 &
rundlt645.sh /dev/tts15 0 sky $N_ITERATIONS | nc $LOG_SERVER 2209 &

n=6
xdlms2 --allow-event-acq --allow-sync-clock --default-intvl 2 --loops \
    $N_ITERATIONS --aa-lifetime 30 \
    /dev/tts16 3072 21234567 9600 2 | nc $LOG_SERVER 2210 &
rundlt645.sh /dev/tts17 0 sky $N_ITERATIONS | nc $LOG_SERVER 2211 &

n=7
xdlms2 --allow-event-acq --allow-sync-clock --default-intvl 2 --loops \
    $N_ITERATIONS --aa-lifetime 30 \
    /dev/tts18 1164 21234567 9600 2 | nc $LOG_SERVER 2212 &
rundlt645.sh /dev/tts19 0 sky $N_ITERATIONS | nc $LOG_SERVER 2213 &

n=8
xdlms2 --allow-event-acq --allow-sync-clock --default-intvl 2 --loops \
    $N_ITERATIONS --aa-lifetime 30 \
    /dev/tts20 1165 21234567 9600 2 | nc $LOG_SERVER 2214 &
rundlt645.sh /dev/tts21 0 sky $N_ITERATIONS | nc $LOG_SERVER 2215 &

n=9
xdlms2 --allow-event-acq --allow-sync-clock --default-intvl 2 --loops \
    $N_ITERATIONS --aa-lifetime 30 \
    /dev/tts22 1166 21234567 9600 2 | nc $LOG_SERVER 2216 &
rundlt645.sh /dev/tts23 0 sky $N_ITERATIONS | nc $LOG_SERVER 2217 &

