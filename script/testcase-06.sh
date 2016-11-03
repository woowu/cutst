#!/bin/bash

iterations=$1
if [ -z $iterations ] || [ $iterations -le 0 ]; then
    exit 1
fi
[ "$CUTST_LOGSERVER" != "" ] || CUTST_LOGSERVER=10.86.201.53

###
echo "E850 51510664 dlms->cu, dlms->cu"
# xdlms addr 7421
rundlms-gen.sh 4 $iterations 2>&1 | nc $CUTST_LOGSERVER 2090 &
rundlms-gen.sh 5 $iterations 2>&1 | nc $CUTST_LOGSERVER 2091 &

echo "E850 51510663 dlms->cu, dlms->cu"
# xdlms addr 7421
rundlms-gen.sh 6 $iterations 2>&1 | nc $CUTST_LOGSERVER 2092 &
rundlms-gen.sh 2 $iterations 2>&1 | nc $CUTST_LOGSERVER 2093 &

echo "E850 51259462. dlms->cu, dlms->cu"
rundlms-gen.sh 8 $iterations 2>&1 | nc $CUTST_LOGSERVER 2094 &
rundlms-gen.sh 3 $iterations 2>&1 | nc $CUTST_LOGSERVER 2095 &

echo "E850 51500165. dlms->cu, dlms->cu"
rundlms-gen.sh 9 $iterations 2>&1 | nc $CUTST_LOGSERVER 2096 &
rundlms-gen.sh 10 $iterations 2>&1 | nc $CUTST_LOGSERVER 2097 &

