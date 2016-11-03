#!/bin/bash

iterations=$1
if [ -z $iterations ] || [ $iterations -le 0 ]; then
    exit 1
fi
[ "$CUTST_LOGSERVER" != "" ] || CUTST_LOGSERVER=10.86.201.53

echo "E850 51510664 dlms->cu, dlms->cu"
rundlms-no-save-no-reg.sh 4 $iterations 2>&1 | nc $CUTST_LOGSERVER 2060 &
rundlms-no-save-no-reg.sh 5 $iterations 2>&1 | nc $CUTST_LOGSERVER 2061 &

