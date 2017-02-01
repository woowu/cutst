#!/bin/bash

rundl645_97() {
    dlt645tst.py -n0 -b1200 -t97sky -d4 -s $1 0 \
        | nc 10.86.201.53 $2
}

rundl645_07() {
    dlt645tst.py -n0 -b2400 -tsky -d4 -s $1 0 \
        | nc 10.86.201.53 $2
}

rundl645_97 /dev/tts4 2232 &
rundl645_07 /dev/tts5 2233 &
rundl645_97 /dev/tts6 2234 &
rundl645_07 /dev/tts7 2235 &
rundl645_97 /dev/tts8 2236 &
rundl645_07 /dev/tts9 2237 &
rundl645_97 /dev/tts10 2238 &
rundl645_07 /dev/tts11 2239 &

