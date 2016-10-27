#!/bin/bash

echo "stop dlt645tst"
for pid in \
    `ps -Cpython -opid,command |grep dlt645tst.py |sed -n 's/^\s\+\([0-9]\+\)\s\+python.*$/\1/p'`; do
    echo killing $pid
    kill $pid
done

echo "stop dlms tests"
for pid in \
    `ps -eF |grep rundlms |grep -v grep |sed -n 's/^root\s\+\([0-9]\+\)\s\+.*$/\1/p'`; do
    echo killing $pid
    kill $pid
done

echo "kill nc"
killall nc 

