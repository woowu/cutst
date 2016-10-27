#!/bin/bash

iterations=100000
server=10.86.201.53

###
echo "E850 51510664 dlms->cu, dlms->cu"
# xdlms addr 7421
rundlms-no-save-no-reg.sh 4 $iterations 2>&1 | nc $server 2070 &
rundlms-no-save-no-reg.sh 5 $iterations 2>&1 | nc $server 2071 &

echo "E850 51510663 dlms->cu, dlms->cu"
# xdlms addr 7421
rundlms-no-save-no-reg.sh 6 $iterations 2>&1 | nc $server 2072 &
rundlms-no-save-no-reg.sh 2 $iterations 2>&1 | nc $server 2073 &

echo "E850 51259462. dlms->cu, dlms->cu"
rundlms-no-save-no-reg.sh 8 $iterations 2>&1 | nc $server 2074 &
rundlms-no-save-no-reg.sh 3 $iterations 2>&1 | nc $server 2075 &

echo "E850 51500165. dlms->cu, dlms->cu"
rundlms-no-save-no-reg.sh 9 $iterations 2>&1 | nc $server 2076 &
rundlms-no-save-no-reg.sh 10 $iterations 2>&1 | nc $server 2077 &

