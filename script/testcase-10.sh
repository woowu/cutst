#!/bin/bash

syslog -m start
sleep 2

xdlms2 --brief --no-reg --loops 100000 --aa-lifetime 120 \
    --lp-read-sliding-window \
    --lp-sliding-window-start "2016-11-29 00:00:00" \
    --lp-sliding-window-end "2016-11-30 23:59:59" \
    --lp-sliding-window-width 1 \
    --lp-sliding-window-step 900 \
    /dev/tts8 1 21234567 9600 2 \
    2>&1 | cut -d' ' -f2- | logger --id &

rundlt645.sh /dev/tts9 50164416 sky 100000 \
    2>&1 | cut -d' ' -f3- | logger --id &

