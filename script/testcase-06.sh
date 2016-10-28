#!/bin/bash

iterations=100000
server=10.86.201.53

###
echo "E850 51510664 dlms->cu, dlms->cu"
# xdlms addr 7421
rundlms-gen.sh 4 $iterations 2>&1 | nc $server 2090 &
rundlms-gen.sh 5 $iterations 2>&1 | nc $server 2091 &

echo "E850 51510663 dlms->cu, dlms->cu"
# xdlms addr 7421
rundlms-gen.sh 6 $iterations 2>&1 | nc $server 2092 &
rundlms-gen.sh 2 $iterations 2>&1 | nc $server 2093 &

echo "E850 51259462. dlms->cu, dlms->cu"
rundlms-gen.sh 8 $iterations 2>&1 | nc $server 2094 &
rundlms-gen.sh 3 $iterations 2>&1 | nc $server 2095 &

echo "E850 51500165. dlms->cu, dlms->cu"
rundlms-gen.sh 9 $iterations 2>&1 | nc $server 2096 &
rundlms-gen.sh 10 $iterations 2>&1 | nc $server 2097 &

