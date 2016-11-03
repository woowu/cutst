#!/bin/bash

iterations=$1
if [ -z $iterations ] || [ $iterations -le 0 ]; then
    exit 1
fi
[ "$CUTST_LOGSERVER" != "" ] || CUTST_LOGSERVER=10.86.201.53

echo "E850 51510664 dlms->cu, dlms->cu"
# xdlms addr 7421
rundlms-no-save-no-reg.sh 4 $iterations 2>&1 | nc $CUTST_LOGSERVER 2070 &
rundlms-no-save-no-reg.sh 5 $iterations 2>&1 | nc $CUTST_LOGSERVER 2071 &

echo "E850 51510663 dlms->cu, dlms->cu"
# xdlms addr 7421
rundlms-no-save-no-reg.sh 6 $iterations 2>&1 | nc $CUTST_LOGSERVER 2072 &
rundlms-no-save-no-reg.sh 2 $iterations 2>&1 | nc $CUTST_LOGSERVER 2073 &

echo "E850 51259462. dlms->cu, dlms->cu"
rundlms-no-save-no-reg.sh 8 $iterations 2>&1 | nc $CUTST_LOGSERVER 2074 &
rundlms-no-save-no-reg.sh 3 $iterations 2>&1 | nc $CUTST_LOGSERVER 2075 &

echo "E850 51500165. dlms->cu, dlms->cu"
rundlms-no-save-no-reg.sh 9 $iterations 2>&1 | nc $CUTST_LOGSERVER 2076 &
rundlms-no-save-no-reg.sh 10 $iterations 2>&1 | nc $CUTST_LOGSERVER 2077 &

