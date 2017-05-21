#!/bin/bash

##
# $1: dev
# $2: addr
# $3: port
rundlms() {
    for i in `seq 1000`; do
        xdlms2 --allow-event-acq --allow-sync-clock --default-intvl 2 \
            --loops 200 --aa-lifetime 60 $1 $2 21234567 9600 2 \
            | socat - TCP4:10.86.201.53:$3
    done
}

rundl645() {
    dlt645tst.py -n0 -tsky -d4 -s --read-counters $1 0 \
        | socat - TCP4:10.86.201.53:$2
}

rundlms /dev/tts12 7421 2220 &
rundlms /dev/tts14 5371 2221 &
rundlms /dev/tts16 4393 2222 &
rundlms /dev/tts18 1164 2223 &
rundlms /dev/tts20 1165 2224 &
rundlms /dev/tts22 1166 2225 &

rundl645 /dev/tts13 2226 &
rundl645 /dev/tts15 2227 &
rundl645 /dev/tts17 2228 &
rundl645 /dev/tts19 2229 &
rundl645 /dev/tts21 2230 &
rundl645 /dev/tts23 2231 &

