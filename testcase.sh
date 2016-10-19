#!/bin/bash

iterations=100000
server=10.86.201.53

echo "E850 51259462. dlt645->cu, dlms->meter"
rundlt645.sh /dev/tts8 51259462 weisheng $iterations 2>&1 | nc $server 2030 &
rundlms.sh 3 $iterations 2>&1 | nc $server 2031 &

echo "E850 51510663 dlt645->cu, dlms->cu"
rundlt645.sh /dev/tts6 51510663 weisheng $iterations 2>&1 | nc $server 2032 &
rundlms.sh 2 $iterations 2>&1 | nc $server 2033 &

echo "E650 37102084 dlt645->cu, dlms->cu"
rundlt645.sh /dev/tts4 37102084 weisheng $iterations 2>&1 | nc $server 2034 &
rundlms.sh 1 $iterations 2>&1 | nc $server 2035 &

