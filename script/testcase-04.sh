#!/bin/bash

iterations=100000
server=10.86.201.53

echo "E850 51510664 dlms->cu, dlms->cu"
rundlms-no-save-no-reg.sh 4 $iterations 2>&1 | nc $server 2060 &
rundlms-no-save-no-reg.sh 5 $iterations 2>&1 | nc $server 2061 &

