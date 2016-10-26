#!/bin/bash

iterations=100000
server=10.86.201.53

echo "E850 51259462. dlt645->cu, dlms->cu"
rundlt645.sh /dev/tts8 51259462 simple $iterations 2>&1 | nc $server 2050 &
rundlms-no-save-no-reg.sh 3 $iterations 2>&1 | nc $server 2051 &

echo "E850 51510663 dlt645->cu, dlms->cu"
rundlt645.sh /dev/tts6 51510663 weisheng $iterations 2>&1 | nc $server 2052 &
rundlms-no-save-no-lp.sh 2 $iterations 2>&1 | nc $server 2053 &
# xdlms addr 7421

echo "E650 37102084 dlt645->cu, dlms->cu"
rundlt645.sh /dev/tts4 37102084 simple $iterations 2>&1 | nc $server 2054 &
rundlms.sh 1 $iterations 2>&1 | nc $server 2055 &

